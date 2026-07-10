"""
===========================================
ShowBiz Editorial Scoring
Version 2.0
===========================================

Purpose:
    Public API for deterministic editorial
    scoring.

    Scoring implementation lives in
    engine.editorial_score_builder.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

from engine.editorial_score_builder import (
    build_editorial_score,
)


CATEGORY_PRIORITY = {
    "Entertainment Industry": 25,
    "Movies": 24,
    "Movie": 24,
    "Television": 23,
    "TV": 23,
    "Celebrity": 22,
    "Awards": 21,
    "Music": 20,
    "Streaming": 12,
    "Style": 8,
}


def _headline(story):
    return (
        story.get("headline")
        or story.get("title")
        or ""
    ).strip()


def _category_score(story):
    return CATEGORY_PRIORITY.get(
        story.get("category", ""),
        10,
    )


def editorial_story_score(
    story,
    duplicate_groups=None,
):
    """
    Public scoring API.
    """

    return build_editorial_score(
        story,
        duplicate_groups,
    )


def story_sort_key(
    story,
    duplicate_groups=None,
):
    """
    Stable deterministic ranking tuple.
    """

    headline = _headline(story)

    return (
        editorial_story_score(
            story,
            duplicate_groups,
        ),
        story.get("editorial_score", 0),
        story.get("score", 0),
        _category_score(story),
        len(headline),
        headline.lower(),
    )


if __name__ == "__main__":

    sample = {
        "headline": (
            "Disney Releases First Trailer "
            "For New Pixar Movie"
        ),
        "category": "Movies",
        "source": "Deadline",
        "score": 61,
    }

    print(editorial_story_score(sample))
    print(story_sort_key(sample))