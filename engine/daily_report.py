import json
from datetime import datetime

from dotenv import load_dotenv

from engine.openai_helper import (
    client,
    create_response,
)

load_dotenv()


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

    last_error = None

    for attempt in range(1, 4):

        try:

            if attempt > 1:
                print(
                    f"Retrying Daily Report "
                    f"(attempt {attempt}/3)..."
                )

            response = create_response(
                model="gpt-5.5",
                input=prompt,
            )

            report = json.loads(
                response.output_text
            )

            report["date"] = (
                datetime.now()
                .strftime("%B %d, %Y")
                .replace(" 0", " ")
            )

            return report

        except Exception as e:

            last_error = e

    print("\n========================================")
    print("DAILY REPORT")
    print("========================================")
    print("Unable to generate daily report:")
    print(last_error)
    print("Skipping Winners & Losers generation.\n")

    return None


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