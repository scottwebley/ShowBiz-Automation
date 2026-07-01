"""
===========================================
ShowBiz AI Image Verifier
Version 1.1
===========================================

Reviews Media Library candidates and chooses
the best image for a story.

This module does NOT search the Media Library.
It only evaluates the candidates it receives.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

#
# Always load the project's .env file,
# regardless of where this module is run.
#

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        f"OPENAI_API_KEY not found in {PROJECT_ROOT / '.env'}"
    )

client = OpenAI()


def verify_image(story, candidates):
    """
    story:
        {
            "headline": "...",
            "summary": "..."
        }

    candidates:
        [
            {
                "media_id": 31874,
                "title": "...",
                "caption": "...",
                "filename": "..."
            },
            ...
        ]
    """

    if not candidates:
        return {
            "media_id": None,
            "confidence": 0,
            "reason": "No candidate images supplied."
        }

    candidate_text = ""

    for i, image in enumerate(candidates, start=1):

        candidate_text += f"""
Candidate {i}

Media ID:
{image.get("media_id")}

Title:
{image.get("title", "")}

Caption:
{image.get("caption", "")}

Filename:
{image.get("filename", "")}
"""

    prompt = f"""
You are the Photo Editor for ShowBiz.com.

Choose the ONE image that best represents
the entertainment story.

If NONE of the images are appropriate,
return media_id = null.

Do NOT choose images based only on
matching keywords.

Prefer the image that best represents:

- person
- movie
- TV show
- musician
- company
- event

Return ONLY valid JSON.

Story Headline:
{story.get("headline", "")}

Story Summary:
{story.get("summary", "")}

Available Images:

{candidate_text}

Return JSON in exactly this format:

{{
    "media_id": 123,
    "confidence": 97,
    "reason": "..."
}}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    text = response.output_text.strip()

    try:
        return json.loads(text)

    except Exception:
        return {
            "media_id": None,
            "confidence": 0,
            "reason": f"Could not parse AI response: {text}"
        }


if __name__ == "__main__":

    story = {
        "headline":
        "Danny Glover Reveals Alzheimer's Diagnosis",

        "summary":
        "The actor announced his diagnosis..."
    }

    candidates = [

        {
            "media_id": 31874,
            "title": "Danny Glover at SAG Awards",
            "caption": "Danny Glover attends the SAG Awards.",
            "filename": "danny-glover.jpg"
        },

        {
            "media_id": 26908,
            "title": "The Bluff",
            "caption": "Scarlett Johansson attends premiere.",
            "filename": "the-bluff.jpg"
        },

        {
            "media_id": 12000,
            "title": "Hollywood Sign",
            "caption": "Los Angeles skyline.",
            "filename": "hollywood.jpg"
        }

    ]

    result = verify_image(
        story,
        candidates,
    )

    print("\n========================================")
    print("AI IMAGE REVIEW")
    print("========================================")
    print(result)