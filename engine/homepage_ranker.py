"""
===========================================
ShowBiz Homepage Ranker
Version 1.0
===========================================

Purpose:
    Rank today's approved entertainment
    stories for the ShowBiz homepage.

Responsibilities:

    • Receive approved stories
    • Ask GPT to rank every story
    • Validate the returned ranking
    • Assign homepage_rank
    • Return ranked stories

Author:
    ShowBiz Automation
"""

import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


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
    # Build simplified list
    #

    choices = []

    for index, story in enumerate(stories):

        choices.append({

            "index": index,

            "headline":
                story.get("headline", ""),

            "summary":
                story.get("summary", ""),

            "category":
                story.get("category", ""),

            "score":
                story.get("score", 0)

        })

    #
    # GPT Prompt
    #

    prompt = f"""
You are the Editor-in-Chief of ShowBiz.com.

Below is today's approved entertainment news.

Your job is to rank EVERY story in the
order it should appear on the homepage.

Rank #1 should be the single most
important entertainment story.

Rank the remaining stories in descending
editorial importance.

Prioritize:

• Breaking entertainment news
• Major celebrities
• Movie announcements
• Television
• Streaming
• Box office
• Awards
• Music
• Broadway
• Gaming

Avoid promoting:

• Roundups
• SummaryBrief articles
• Tag pages
• Archive pages
• Evergreen articles
• Generic listicles
• Minor updates

Return ONLY valid JSON.

Example:

{{
    "homepage_ranking":
    [
        4,
        7,
        2,
        1,
        5,
        0,
        3,
        6
    ]
}}

Stories:

{json.dumps(choices, indent=2)}
"""

    response = client.responses.create(

        model="gpt-5.5",

        input=prompt

    )

    result = response.output_text.strip()

    #
    # Remove markdown fences
    #

    if result.startswith("```"):

        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]
            #
    # Parse JSON
    #

    data = json.loads(result)

    if "homepage_ranking" not in data:

        raise ValueError(
            "AI response missing 'homepage_ranking'"
        )

    ranking = data["homepage_ranking"]

    if not isinstance(ranking, list):

        raise ValueError(
            "'homepage_ranking' must be a list."
        )

    #
    # Validate size
    #

    if len(ranking) != len(stories):

        raise ValueError(
            f"Expected {len(stories)} ranked stories, "
            f"received {len(ranking)}."
        )

    #
    # Validate indices
    #

    seen = set()

    for index in ranking:

        if not isinstance(index, int):

            raise ValueError(
                f"Invalid index type: {index}"
            )

        if index < 0 or index >= len(stories):

            raise ValueError(
                f"Invalid story index: {index}"
            )

        if index in seen:

            raise ValueError(
                f"Duplicate story index: {index}"
            )

        seen.add(index)

    #
    # Check for missing stories
    #

    expected = set(range(len(stories)))

    missing = expected - seen

    if missing:

        raise ValueError(
            f"Missing story indices: "
            f"{sorted(missing)}"
        )

    #
    # Build ranked list
    #

    ranked = []

    for rank, index in enumerate(
        ranking,
        start=1
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