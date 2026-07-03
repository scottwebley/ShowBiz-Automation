import json
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def generate_daily_report(stories):
    """
    Generates the ShowBiz Entertainment Winners & Losers report.

    Returns a Python dictionary, or None if generation fails.
    """

    stories_json = json.dumps(stories, indent=2)

    prompt = f"""
You are the senior editorial team for ShowBiz.com.

Analyze today's entertainment news.

Return ONLY valid JSON.

Choose the most newsworthy items from TODAY'S entertainment news.

Return this structure exactly:

{{
  "winner": {{
    "name": "",
    "reason": ""
  }},
  "loser": {{
    "name": "",
    "reason": ""
  }},
  "trending_movie": {{
    "title": "",
    "reason": ""
  }},
  "trending_artist": {{
    "name": "",
    "reason": ""
  }},
  "trend_to_watch": {{
    "title": "",
    "description": ""
  }},
  "showbiz_take": "",
  "watch_list": [
    "",
    "",
    "",
    "",
    ""
  ]
}}

Editorial Rules

• Base every decision ONLY on today's news.
• Prefer people, movies, companies and events.
• Avoid evergreen observations.
• Avoid speculation.
• If no obvious loser exists, choose the company or project that had the weakest news day.
• "ShowBiz Take" should explain what today's news means for the entertainment industry.

Today's News:

{stories_json}
"""

    try:

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        report = json.loads(response.output_text)

    except Exception as e:

        print("\n========================================")
        print("DAILY REPORT")
        print("========================================")
        print("Unable to generate daily report:")
        print(e)
        print("Skipping Winners & Losers generation.\n")

        return None

    # Add today's date for the newsroom pipeline.
    report["date"] = datetime.now().strftime("%B %d, %Y").replace(" 0", " ")

    return report


if __name__ == "__main__":

    sample = [
        {
            "headline": "Christopher Nolan announces new film",
            "summary": "Major studio announcement.",
            "category": "Movies"
        },
        {
            "headline": "Netflix unveils new streaming slate",
            "summary": "Several new series announced.",
            "category": "TV & Streaming"
        }
    ]

    report = generate_daily_report(sample)

    if report is not None:
        print(json.dumps(report, indent=4))