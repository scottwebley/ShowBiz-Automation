"""
===========================================
ShowBiz Editorial Story Type
Version 1.0
===========================================

Purpose:
    Deterministically classify an
    entertainment news story.

    This module contains NO scoring logic.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


STORY_TYPES = {

    "breaking": (
        "breaking",
        "developing",
        "just in",
    ),

    "box_office": (
        "box office",
        "opening weekend",
        "weekend gross",
        "ticket sales",
    ),

    "casting": (
        "cast",
        "casting",
        "joins",
        "added to cast",
        "set to star",
        "starring",
    ),

    "trailer": (
        "trailer",
        "teaser",
        "first look",
        "official trailer",
    ),

    "release_date": (
        "release date",
        "premiere",
        "premieres",
        "debuts",
        "opening date",
    ),

    "renewal": (
        "renewed",
        "renewal",
        "picked up",
        "season renewed",
    ),

    "cancellation": (
        "cancelled",
        "canceled",
        "cancelation",
        "ending after",
        "final season",
    ),

    "award": (
        "oscar",
        "academy award",
        "emmy",
        "grammy",
        "golden globe",
        "tony award",
        "wins",
        "winner",
        "nominee",
        "nomination",
    ),

    "industry": (
        "ceo",
        "executive",
        "earnings",
        "revenue",
        "merger",
        "acquisition",
        "layoffs",
        "shares",
        "studio",
    ),

    "music": (
        "tour",
        "concert",
        "album",
        "single",
        "music video",
    ),

    "festival": (
        "festival",
        "comic-con",
        "comic con",
        "sxsw",
        "cannes",
        "sundance",
        "tiff",
    ),

    "legal": (
        "lawsuit",
        "sues",
        "sued",
        "court",
        "legal",
        "trial",
        "settlement",
    ),

    "obituary": (
        "dies",
        "dead",
        "death",
        "passes away",
        "obituary",
    ),

    "review": (
        "review",
        "review:",
        "reviews:",
        "rated",
    ),

    "opinion": (
        "opinion",
        "editorial",
        "column",
        "commentary",
    ),

    "listicle": (
        "top 10",
        "top ten",
        "best ",
        "ranking",
        "ranked",
    ),

    "streaming_guide": (
        "what to watch",
        "where to watch",
        "streaming guide",
        "watch guide",
        "watching guide",
        "now streaming",
    ),
}


def _headline(story):
    return (
        story.get("headline")
        or story.get("title")
        or ""
    ).lower()


def detect_story_type(story):
    """
    Return the first matching
    editorial story type.
    """

    text = _headline(story)

    if not text:
        return "general"

    for story_type, phrases in STORY_TYPES.items():

        if any(
            phrase in text
            for phrase in phrases
        ):
            return story_type

    return "general"


if __name__ == "__main__":

    sample = {

        "headline":
        "Disney Releases First Trailer For New Pixar Movie"

    }

    print(detect_story_type(sample))