"""
===========================================
ShowBiz Homepage Ranker
Version 2.1
===========================================

Purpose:
    Rank today's approved entertainment
    stories for the ShowBiz homepage.

Author:
    ShowBiz Automation
"""

from engine.openai_helper import (
    client,
    create_response,
    ai_available,
)

from engine.homepage_prompt import (
    build_homepage_prompt,
)
from engine.homepage_validator import (
    validate_homepage_ranking,
)


def rank_homepage(stories):
    """
    Rank all approved stories.

    Every returned story receives:

        homepage_rank

    Returns:

        ranked_stories
    """

    if not stories:
        return []

    #
    # Skip immediately if AI has already
    # been disabled for this run.
    #

    if not ai_available():
        return []

    #
    # Build simplified list.
    #

    choices = []

    for index, story in enumerate(stories):

        choices.append(
            {
                "index": index,
                "headline": story.get(
                    "headline",
                    "",
                ),
                "summary": story.get(
                    "summary",
                    "",
                ),
                "category": story.get(
                    "category",
                    "",
                ),
                "score": story.get(
                    "score",
                    0,
                ),
            }
        )

    #
    # Build GPT prompt.
    #

    prompt = build_homepage_prompt(
        choices
    )

    #
    # Ask GPT.
    #

    response = create_response(
        model="gpt-5.5",
        input=prompt,
    )

    #
    # If AI became unavailable while
    # processing the request, return an
    # empty ranking so the caller can
    # fall back naturally.
    #

    if response is None:
        return []

    result = response.output_text.strip()

    #
    # Validate AI response.
    #

    ranking = validate_homepage_ranking(
        result,
        len(stories),
    )

    #
    # Build ranked list.
    #

    ranked = []

    for rank, index in enumerate(
        ranking,
        start=1,
    ):

        story = stories[index]

        story["homepage_rank"] = rank

        ranked.append(story)

    return ranked


if __name__ == "__main__":

    from engine.ai_news import get_top_stories

    print("=" * 60)
    print("SHOWBIZ HOMEPAGE RANKER")
    print("=" * 60)

    stories = get_top_stories()

    if not stories:

        print("\nNo approved stories.\n")
        raise SystemExit(0)

    ranked = rank_homepage(stories)

    print()
    print("=" * 60)
    print("HOMEPAGE RANKING")
    print("=" * 60)

    for story in ranked:

        print(
            f"#{story['homepage_rank']:>2} "
            f"[{story['category']}] "
            f"{story['headline']}"
        )