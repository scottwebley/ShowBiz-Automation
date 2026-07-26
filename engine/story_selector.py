import json

from engine.openai_helper import (
    client,
    create_response,
)


def select_top_story(stories):
    """
    Select the single best entertainment story
    for the ShowBiz homepage.

    Returns the ORIGINAL story object so that
    score, URL, source, published date and all
    metadata are preserved.
    """

    if not stories:
        return None

    #
    # Build a simplified list for the AI.
    # The AI only needs enough information
    # to choose the winning story.
    #

    choices = []

    for i, story in enumerate(stories):

        choices.append({
            "index": i,
            "headline": story.get("headline", ""),
            "summary": story.get("summary", ""),
            "category": story.get("category", ""),
            "source": story.get("source", ""),
            "score": story.get("score", 0)
        })

    prompt = f"""
You are the Editor-in-Chief of ShowBiz.com.

Below is today's approved entertainment news.

Choose the ONE story that deserves to become
the homepage Top Story.

Prioritize:

• Breaking entertainment news
• Major movie announcements
• Streaming news
• Casting news
• Major celebrities
• New trailers
• Box office
• Awards
• Major television news

Avoid:

• Duplicate stories
• Minor updates
• Opinion pieces
• Evergreen stories
• Generic listicles

If multiple stories describe the same entertainment event, select only one.

Prefer the version from the most authoritative entertainment news source.

Examples of authoritative sources include Deadline, Variety, The Hollywood Reporter, Reuters, Associated Press, and official studio announcements.

Do not select two different headlines covering the same announcement, trailer, casting, premiere, or event.

Return ONLY valid JSON.

Example:

{{
    "selected_index": 7
}}

Stories:

{json.dumps(choices, indent=2)}
"""

    response = create_response(
        model="gpt-5.5",
        input=prompt,
    )

    result = response.output_text.strip()

    #
    # Remove markdown fences if present
    #

    if result.startswith("```"):

        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    data = json.loads(result)

    index = data["selected_index"]

    if index < 0 or index >= len(stories):
        raise ValueError(
            f"AI returned invalid story index: {index}"
        )

    #
    # Return the ORIGINAL story.
    #

    return stories[index]


if __name__ == "__main__":

    from engine.ai_news import get_top_stories

    stories = get_top_stories()

    winner = select_top_story(stories)

    print("\nTOP STORY\n")

    print(json.dumps(winner, indent=4))