import json
from datetime import datetime, timedelta

from engine.openai_helper import (
    client,
    create_response,
)


def _week_label():
    """
    Return the editorial week beginning on Monday.
    """

    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    return (
        f"Week of "
        f"{monday.strftime('%B')} "
        f"{monday.day}, "
        f"{monday.year}"
    )


def _build_story_list(stories):
    """
    Build a numbered story list for GPT.
    """

    lines = []

    for i, story in enumerate(stories, start=1):

        lines.append(
            f"""
Story {i}

Headline:
{story.get("headline", "")}

Summary:
{story.get("summary", "")}

Category:
{story.get("category", "")}
"""
        )

    return "\n".join(lines)


def generate_featured_entertainer(stories):
    """
    Generates the ShowBiz Featured Entertainer of the Week.

    Returns a Python dictionary or None.
    """

    if not stories:
        return None

    current_date = datetime.now()

    story_text = _build_story_list(stories)

    prompt = f"""
You are the senior editorial board for ShowBiz.com.

Analyze the supplied entertainment news.

Choose ONE entertainer who most deserves to be named
Featured Entertainer of the Week.

Use ONLY the supplied stories.

Do not invent facts.

Return ONLY valid JSON.

Return EXACTLY this structure:

{{
    "story_number": 1,
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

Rules:

- story_number MUST be the selected story number.
- story_number must be an integer.
- summary should be concise.
- why_selected should focus on THIS WEEK.
- Do not fabricate quotes.
- If no quote is appropriate return "".
- Return ONLY JSON.

Stories:

{story_text}
"""

    try:

        response = create_response(
            model="gpt-5.5",
            input=prompt,
        )

        entertainer = json.loads(
            response.output_text
        )

        if not isinstance(entertainer, dict):
            raise ValueError(
                "Response is not an object."
            )

        required = [
            "story_number",
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

        for field in required:

            if field not in entertainer:
                raise ValueError(
                    f"Missing field: {field}"
                )

        if not isinstance(
            entertainer["story_number"],
            int,
        ):
            raise ValueError(
                "story_number must be an integer."
            )

        if (
            entertainer["story_number"] < 1
            or entertainer["story_number"] > len(stories)
        ):
            raise ValueError(
                "story_number out of range."
            )

        if not isinstance(
            entertainer["career_highlights"],
            list,
        ):
            raise ValueError(
                "career_highlights must be a list."
            )

        if not isinstance(
            entertainer["recent_projects"],
            list,
        ):
            raise ValueError(
                "recent_projects must be a list."
            )

        if not isinstance(
            entertainer["watch_next"],
            list,
        ):
            raise ValueError(
                "watch_next must be a list."
            )

        story_index = entertainer["story_number"] - 1

        entertainer["source_story"] = stories[story_index]
        entertainer["image_query"] = entertainer["name"]
        entertainer["week"] = _week_label()

        entertainer["generated_date"] = (
            current_date.strftime("%B %d, %Y")
            .replace(" 0", " ")
        )

        return entertainer

    except Exception as e:

        print("\n========================================")
        print("FEATURED ENTERTAINER")
        print("========================================")
        print("Unable to generate Featured Entertainer:")
        print(e)
        print("Skipping Featured Entertainer generation.\n")

        return None


if __name__ == "__main__":

    sample = [
        {
            "headline": (
                "Christopher Nolan announces new film"
            ),
            "summary": (
                "Major studio announcement."
            ),
            "category": "Movies",
        },
        {
            "headline": (
                "Taylor Swift announces surprise tour dates"
            ),
            "summary": (
                "Fans react to new stadium tour."
            ),
            "category": "Music",
        },
        {
            "headline": (
                "Zendaya signs new starring role"
            ),
            "summary": (
                "Upcoming feature film announced."
            ),
            "category": "Movies",
        },
    ]

    report = generate_featured_entertainer(sample)

    if report is not None:

        print(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False,
            )
        )