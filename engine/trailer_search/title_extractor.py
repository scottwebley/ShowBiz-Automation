"""
Extract the movie, TV series, or video game title from an entertainment
headline.

This module is completely independent of the publishing pipeline.
"""

import re


SEASON_PATTERN = re.compile(
    r"\bSeason\s+\d+\b",
    re.IGNORECASE,
)

EPISODE_PATTERN = re.compile(
    r"\bEpisode\s+\d+\b",
    re.IGNORECASE,
)

CUT_PATTERNS = [
    r"\bgets\b",
    r"\bget\b",
    r"\bearns\b",
    r"\bwins\b",
    r"\badds\b",
    r"\breveals\b",
    r"\bannounces\b",
    r"\bdelayed\b",
    r"\bdelays\b",
    r"\breceives\b",
    r"\bsets\b",
    r"\bshares\b",
    r"\bdebuts\b",
    r"\bopens\b",
    r"\blaunches\b",
]


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title(headline: str) -> str | None:
    """
    Extract the likely movie, TV show, or video game title.

    Examples:

        Wednesday Season 3 gets first teaser
            -> Wednesday

        The Fantastic Four: First Steps earns huge opening
            -> The Fantastic Four: First Steps

        Grand Theft Auto VI delayed again
            -> Grand Theft Auto VI
    """

    if not headline:
        return None

    text = _clean(headline)

    text = text.replace('"', "").replace("'", "")

    text = SEASON_PATTERN.sub("", text)
    text = EPISODE_PATTERN.sub("", text)

    for pattern in CUT_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            text = text[:m.start()]
            break

    text = re.sub(r"\bfirst teaser\b.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bofficial teaser\b.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bofficial trailer\b.*", "", text, flags=re.IGNORECASE)

    text = re.sub(r"\s+", " ", text)

    return text.strip(" :-") or None