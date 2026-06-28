from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


def select_top_story(stories):
    """
    Select the single best entertainment story for the ShowBiz homepage.
    """

    prompt = f"""
You are the Editor-in-Chief of ShowBiz.com.

Below is a list of today's entertainment headlines.

Your job is NOT to summarize them.

Your job is to choose the ONE story that deserves the homepage lead.

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

Reject:

• Sports
• Crime
• Politics
• Generic listicles
• Opinion pieces
• Evergreen articles
• Old stories
• Stories that are not primarily about entertainment

Return ONLY valid JSON.

Format:

{{
    "headline":"",
    "summary":"",
    "category":""
}}

Categories must be exactly one of:

Movies
TV & Streaming
Music
Celebrity News
Gaming
Entertainment Industry
Style
ShowBiz Originals

Stories:

{json.dumps(stories, indent=2)}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    result = response.output_text.strip()

    # Remove accidental markdown fences if the model adds them
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    return json.loads(result)


if __name__ == "__main__":

    from ai_news import get_top_stories

    stories = get_top_stories()

    winner = select_top_story(stories)

    print("\nTOP STORY\n")
    print(json.dumps(winner, indent=4))