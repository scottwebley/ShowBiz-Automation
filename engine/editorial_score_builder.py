"""
===========================================
ShowBiz Editorial Score Builder
Version 1.0
===========================================

Purpose:
    Build the deterministic editorial score.

    This module contains the scoring
    implementation used by
    editorial_scoring.py.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

from engine.editorial_duplicates import duplicate_penalty
from engine.editorial_entities import count_major_entities
from engine.editorial_keywords import (
    BREAKING_NEWS_TERMS,
    EVERGREEN_PENALTIES,
    HARD_REJECTION_TERMS,
    INDUSTRY_TERMS,
    MAJOR_FRANCHISES,
    MAJOR_STUDIOS,
    STREAMING_PENALTIES,
    contains_any,
    count_matches,
)
from engine.editorial_sources import source_score
from engine.editorial_story_type import detect_story_type


STORY_TYPE_BONUS = {
    "breaking": 200,
    "box_office": 180,
    "trailer": 140,
    "renewal": 130,
    "cancellation": 130,
    "casting": 120,
    "award": 120,
    "industry": 110,
    "release_date": 100,
    "festival": 90,
    "music": 80,
    "legal": 70,
    "obituary": 60,
    "general": 0,
    "review": -100,
    "opinion": -150,
    "listicle": -250,
    "streaming_guide": -200,
}


def build_editorial_score(
    story,
    duplicate_groups=None,
):
    """
    Build the complete editorial score.
    """

    headline = (
        story.get("headline")
        or story.get("title")
        or ""
    ).strip()

    if not headline:
        return -100000

    text = headline.lower()

    if contains_any(
        text,
        HARD_REJECTION_TERMS,
    ):
        return -1000

    score = 0

    #
    # Source quality
    #

    score += source_score(story)

    #
    # Story classification
    #

    story_type = detect_story_type(story)

    score += STORY_TYPE_BONUS.get(
        story_type,
        0,
    )

    #
    # Editorial keyword bonuses
    #

    score += (
        count_matches(
            text,
            BREAKING_NEWS_TERMS,
        )
        * 120
    )

    score += (
        count_matches(
            text,
            MAJOR_STUDIOS,
        )
        * 90
    )

    score += (
        count_matches(
            text,
            MAJOR_FRANCHISES,
        )
        * 80
    )

    score += (
        count_matches(
            text,
            INDUSTRY_TERMS,
        )
        * 45
    )

    #
    # Major entities
    #

    score += (
        count_major_entities(text)
        * 75
    )

    #
    # Editorial penalties
    #

    if contains_any(
        text,
        EVERGREEN_PENALTIES,
    ):
        score -= 250

    if contains_any(
        text,
        STREAMING_PENALTIES,
    ):
        score -= 120

    #
    # Duplicate penalty
    #

    if duplicate_groups is not None:

        score -= duplicate_penalty(
            story,
            duplicate_groups,
        )

    #
    # Prefer descriptive headlines
    #

    score += min(
        len(headline) // 5,
        20,
    )

    return score


if __name__ == "__main__":

    sample = {
        "headline":
            "Disney Releases First Trailer "
            "For New Pixar Movie",
        "source": "Deadline",
    }

    print(build_editorial_score(sample))