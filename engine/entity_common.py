"""
===========================================
ShowBiz Entity Common
Version 1.0
===========================================

Shared constants and helper functions for
the ShowBiz Entity Extractor.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


# --------------------------------------------------
# ALIASES
# --------------------------------------------------

ALIASES = {
    "The Rock": "Dwayne Johnson",
    "MCU": "Marvel Cinematic Universe",
    "LOTR": "The Lord of the Rings",
}


# --------------------------------------------------
# ORGANIZATIONS
# --------------------------------------------------

ORGANIZATIONS = {
    "Netflix",
    "Disney",
    "Pixar",
    "Marvel",
    "Lucasfilm",
    "Apple",
    "Amazon",
    "Prime Video",
    "HBO",
    "Max",
    "Paramount",
    "NBC",
    "CBS",
    "ABC",
    "FOX",
    "Sony",
    "Universal",
    "Warner Bros",
    "Sky",
    "ITV",
    "BBC",
    "CNN",
    "MSNBC",
    "ESPN",
    "Hulu",
    "Peacock",
}


# --------------------------------------------------
# STOP WORDS
# --------------------------------------------------

STOP_NAME_WORDS = {
    "Is",
    "Are",
    "Was",
    "Were",
    "Has",
    "Have",
    "Had",
    "Do",
    "Does",
    "Did",
    "Announces",
    "Announced",
    "Reveal",
    "Reveals",
    "Revealed",
    "Confirms",
    "Confirmed",
    "Says",
    "Say",
    "After",
    "Before",
    "With",
    "Without",
    "From",
    "Into",
    "For",
    "In",
    "On",
    "At",
    "Of",
    "To",
    "And",
    "Or",
    "Big",
    "New",
    "Latest",
    "Breaking",
    "More",
    "Also",
    "Star",
    "News",
    "TV",
    "Show",
    "Movie",
    "Film",
    "Series",
    "Season",
    "Episode",
    "Challenge",
    "Challenges",
    "Listeners",
    "Listener",
    "Views",
    "View",
    "Decoding",
    "Surpasses",
    "Netflix",
    "HBO",
    "Disney",
    "Amazon",
    "Prime",
    "Video",
    "Mom",
    "Dad",
    "Britain",
    "Your",
    "My",
    "Our",
    "Their",
    "His",
    "Her",
    "Its",
    "Era",
}


IGNORE_KEYWORDS = {
    "the",
    "and",
    "with",
    "from",
    "this",
    "that",
    "after",
    "before",
    "more",
    "also",
    "news",
    "show",
    "movie",
    "today",
}


# --------------------------------------------------
# HELPERS
# --------------------------------------------------


def normalize(text: str) -> str:
    """
    Apply alias normalization.
    """

    return ALIASES.get(text, text)


def clean_person_token(token: str) -> str:
    """
    Remove punctuation and possessives.
    """

    token = token.strip(
        ".,:;!?()[]{}\"'"
    )

    if token.endswith("'s"):
        token = token[:-2]

    elif token.endswith("’s"):
        token = token[:-2]

    return token