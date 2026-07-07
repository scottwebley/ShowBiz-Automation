"""
===========================================
ShowBiz Featured Entertainer Profile
Version 1.0
===========================================

Generates the complete Featured Entertainer
profile using GPT-5.5.

This module does NOT write HTML.

It returns a structured Python dictionary
that is later rendered by
featured_entertainer_writer.py.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

PROMPT_FILE = Path(
    "prompts/featured_entertainer_profile.md"
)


def _load_prompt() -> str:
    """
    Load the master Featured Entertainer prompt.
    """

    return PROMPT_FILE.read_text(
        encoding="utf-8"
    )


def _build_input(report: dict) -> str:
    """
    Build the GPT input using the selected
    Featured Entertainer.
    """

    headline = report.get(
        "headline",
        ""
    )

    summary = report.get(
        "summary",
        ""
    )

    profession = report.get(
        "profession",
        ""
    )

    why_selected = report.get(
        "why_selected",
        ""
    )

    prompt = _load_prompt()

    return f"""
{prompt}

----------------------------------------------------
CURRENT FEATURED ENTERTAINER
----------------------------------------------------

Name:
{report.get("name","")}

Profession:
{profession}

Headline:
{headline}

Summary:
{summary}

Why Featured:
{why_selected}

----------------------------------------------------

Return ONLY valid JSON.
"""
def generate_featured_entertainer_profile(
    report: dict,
) -> dict | None:
    """
    Generate the complete Featured
    Entertainer profile.

    Returns a structured dictionary
    or None.
    """

    if not report:
        return None

    prompt = _build_input(report)

    try:

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt,
        )

        profile = json.loads(
            response.output_text
        )

        if not isinstance(
            profile,
            dict,
        ):
            raise ValueError(
                "Profile is not a JSON object."
            )
        #
        # Required fields.
        #

        required = [
            "name",
            "profession",
            "headline",
            "opening_feature",
            "quick_facts",
            "early_life",
            "family",
            "career_story",
            "career_highlights",
            "television",
            "films",
            "awards",
            "business_ventures",
            "philanthropy",
            "current_projects",
            "interesting_facts",
            "why_featured",
            "watch_next",
            "related_internal_topics",
            "official_links",
        ]

        for field in required:

            if field not in profile:

                raise ValueError(
                    f"Missing field: {field}"
                )

        #
        # Validate dictionaries.
        #

        for field in (
            "quick_facts",
            "family",
        ):

            if not isinstance(
                profile[field],
                dict,
            ):

                raise ValueError(
                    f"{field} must be an object."
                )

        #
        # Validate lists.
        #

        list_fields = [
            "career_highlights",
            "television",
            "films",
            "awards",
            "business_ventures",
            "philanthropy",
            "current_projects",
            "interesting_facts",
            "watch_next",
            "related_internal_topics",
            "official_links",
        ]

        for field in list_fields:

            if not isinstance(
                profile[field],
                list,
            ):

                raise ValueError(
                    f"{field} must be a list."
                )

        #
        # Preserve weekly metadata.
        #

        profile["week"] = report.get(
            "week",
            ""
        )

        profile["generated_date"] = report.get(
            "generated_date",
            ""
        )

        profile["image_query"] = report.get(
            "image_query",
            report.get("name", "")
        )

        profile["source_story"] = report.get(
            "source_story"
        )
        return profile

    except Exception as e:

        print()
        print("=" * 40)
        print("FEATURED ENTERTAINER PROFILE")
        print("=" * 40)
        print(e)
        print()

        return None
    