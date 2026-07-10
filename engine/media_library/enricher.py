"""
===========================================
ShowBiz Media Library Enricher
Version 1.1
===========================================

Purpose:
    Use AI to enrich Media Library metadata
    for a single WordPress attachment.

Author:
    ShowBiz Automation
"""

import json

from dotenv import load_dotenv

from engine.openai_helper import (
    client,
    create_response,
)
from engine.media_library.normalize import safe

load_dotenv()


GENERIC_PREFIXES = (
    "aggregator downloaded",
    "licensed-image",
    "img_",
    "dsc",
    "gettyimages-",
)


def needs_enrichment(item):
    """
    Return True if this media item should
    be enriched.
    """

    title = normalize_title(item)
    filename = safe(
        item.get("filename")
    ).lower()

    if not title.strip():
        return True

    for prefix in GENERIC_PREFIXES:

        if title.startswith(prefix):
            return True

        if filename.startswith(prefix):
            return True

    return False


def normalize_title(item):
    """
    Return the attachment title as a
    lowercase string.
    """

    return safe(
        item.get("title")
    ).lower()


def build_prompt(item):
    """
    Build the AI enrichment prompt.
    """

    return f"""
You are enriching metadata for a
WordPress Media Library image.

Return ONLY valid JSON.

Required format:

{{
    "title": "...",
    "alt": "...",
    "caption": "...",
    "entities": [],
    "confidence": 0
}}

Current metadata:

{json.dumps(item, indent=2)}
"""


def enrich(item):
    """
    Enrich one media item.

    Returns:
        dict
    """

    if not needs_enrichment(item):

        return {
            "skipped": True,
            "reason": "Already descriptive."
        }

    prompt = build_prompt(item)

    response = create_response(
        model="gpt-5.5",
        input=prompt,
    )

    text = response.output_text.strip()

    if text.startswith("```"):

        text = text.split(
            "\n",
            1,
        )[1]

        text = text.rsplit(
            "```",
            1,
        )[0]

    return json.loads(text)