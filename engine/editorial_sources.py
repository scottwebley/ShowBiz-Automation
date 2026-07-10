"""
===========================================
ShowBiz Editorial Sources
Version 1.0
===========================================

Purpose:
    Source reputation scoring for the
    Local Story Selector.

    This module contains NO editorial
    keyword logic.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


# ---------------------------------------------------------
# Preferred original reporting
# ---------------------------------------------------------

PREFERRED_SOURCES = (
    "deadline",
    "variety",
    "the hollywood reporter",
    "billboard",
    "screen daily",
    "indiewire",
    "the wrap",
    "broadcast",
    "music business worldwide",
    "pollstar",
)


# ---------------------------------------------------------
# Trusted news organizations
# ---------------------------------------------------------

TRUSTED_WIRES = (
    "associated press",
    "ap",
    "reuters",
    "bbc",
    "npr",
    "abc news",
    "cbs news",
    "nbc news",
    "pbs",
)


# ---------------------------------------------------------
# Entertainment trades
# ---------------------------------------------------------

TRADE_PUBLICATIONS = (
    "deadline",
    "variety",
    "the hollywood reporter",
    "billboard",
    "screen rant",
    "empire",
    "total film",
    "rolling stone",
)


# ---------------------------------------------------------
# Lower-value syndicated / clickbait
# ---------------------------------------------------------

LOW_VALUE_SOURCES = (
    "yahoo",
    "aol",
    "msn",
    "flipboard",
    "newsbreak",
    "bored panda",
    "the mirror",
    "daily mail",
    "the sun",
)


# ---------------------------------------------------------
# Syndication indicators
# ---------------------------------------------------------

MIRROR_PATTERNS = (
    "via ",
    "syndicated",
    "republished",
    "originally appeared",
    "originally published",
    "from our partners",
)


def _story_text(story) -> str:
    """
    Combine all possible source fields.
    """

    fields = (
        story.get("source"),
        story.get("publisher"),
        story.get("site"),
        story.get("domain"),
        story.get("url"),
    )

    return " ".join(
        str(f).lower()
        for f in fields
        if f
    )


def _contains(text: str, phrases) -> bool:
    return any(p in text for p in phrases)


def source_score(story) -> int:
    """
    Reputation score based only on
    story source.

    Positive = trusted/original
    Negative = mirror/clickbait
    """

    text = _story_text(story)

    score = 0

    if _contains(text, PREFERRED_SOURCES):
        score += 150

    if _contains(text, TRADE_PUBLICATIONS):
        score += 80

    if _contains(text, TRUSTED_WIRES):
        score += 70

    if _contains(text, LOW_VALUE_SOURCES):
        score -= 80

    if _contains(text, MIRROR_PATTERNS):
        score -= 120

    return score


if __name__ == "__main__":

    sample = {
        "source": "Deadline",
        "url": "https://deadline.com/example",
    }

    print(source_score(sample))