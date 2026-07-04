import json
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def generate_featured_entertainer(stories):
    """
    Generates the ShowBiz Featured Entertainer of the Week.

    Returns a Python dictionary, or None if generation fails.
    """

    stories_json = json.dumps(stories, indent=2)

    current_date = datetime.now()
    week_label = (
        f"Week of {current_date.strftime('%B')} "
        f"{current_date.day}, {current_date.year}"
    )

    prompt = f"""
You are the senior editorial team for ShowBiz.com.

Analyze this week's entertainment news.

Return ONLY valid JSON.

Select the ONE entertainer who most deserves to be named
Featured Entertainer of the Week.

The entertainer may be an actor, actress, musician, singer,
director, producer, comedian, television personality, athlete
working in entertainment, or any other entertainment figure.

Choose based ONLY on the supplied news.

Do not invent facts.

Do not speculate.

If multiple people qualify, choose the one with the greatest
overall impact across the week's news.

Return this structure exactly:

{{
  "name": "",
  "profession": "",
  "headline": "",
  "summary": "",
  "why_selected": "",
  "career_highlights": [
    "",
    "",
    ""
  ],
  "recent_projects": [
    "",
    "",
    ""
  ],
  "fun_fact": "",
  "quote": "",
  "watch_next": [
    "",
    "",
    ""
  ]
}}

Editorial Rules

• Base every decision ONLY on the supplied news.
• Keep summary factual.
• Keep why_selected focused on this week's news.
• Career highlights should be concise.
• Recent projects should be real projects when available.
• If no verified quote is supported by widely known public information,
  return an empty string.
• Never fabricate information.
• Return ONLY valid JSON.

Entertainment News:

{stories_json}
"""

    try:

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        entertainer = json.loads(response.output_text)

        if not isinstance(entertainer, dict):
            raise ValueError("Response is not a JSON object.")

        required_fields = [
            "name",
            "profession",
            "headline",
            "summary",
            "why_selected",
            "career_highlights",
            "recent_projects",
            "fun_fact",
            "quote",
            "watch_next",
        ]

        for field in required_fields:
            if field not in entertainer:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(entertainer["career_highlights"], list):
            raise ValueError("career_highlights must be a list.")

        if not isinstance(entertainer["recent_projects"], list):
            raise ValueError("recent_projects must be a list.")

        if not isinstance(entertainer["watch_next"], list):
            raise ValueError("watch_next must be a list.")

    except Exception as e:

        print("\n========================================")
        print("FEATURED ENTERTAINER")
        print("========================================")
        print("Unable to generate Featured Entertainer:")
        print(e)
        print("Skipping Featured Entertainer generation.\n")

        return None

    entertainer["week"] = week_label
    entertainer["generated_date"] = current_date.strftime("%B %d, %Y").replace(
        " 0", " "
    )

    return entertainer


if __name__ == "__main__":

    sample = [
        {
            "headline": "Christopher Nolan announces new film",
            "summary": "Major studio announcement.",
            "category": "Movies"
        },
        {
            "headline": "Taylor Swift announces surprise tour dates",
            "summary": "Fans react to new stadium tour.",
            "category": "Music"
        },
        {
            "headline": "Zendaya signs new starring role",
            "summary": "Upcoming feature film announced.",
            "category": "Movies"
        }
    ]

    report = generate_featured_entertainer(sample)

    if report is not None:
        print(json.dumps(report, indent=4))