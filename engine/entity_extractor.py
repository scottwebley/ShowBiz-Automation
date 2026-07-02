"""
===========================================
ShowBiz Entity Extractor
Version 1.0
===========================================

Extracts entertainment entities from news headlines.

This module does NOT perform searching.

It simply identifies the important entities so that
other modules (Media Library Search, Image Verifier,
External Search, etc.) can make better decisions.
"""

from __future__ import annotations

import re


# ----------------------------------------
# Known entertainment aliases
# ----------------------------------------

ALIASES = {
    "The Rock": "Dwayne Johnson",
    "MCU": "Marvel Cinematic Universe",
    "LOTR": "The Lord of the Rings",
}


# ----------------------------------------
# Helper
# ----------------------------------------

def normalize(name: str) -> str:
    return ALIASES.get(name, name)


# ----------------------------------------
# Main extractor
# ----------------------------------------

def extract_entities(headline: str) -> dict:
    """
    Extract entertainment entities from a headline.

    Returns:

    {
        "people": [],
        "movies": [],
        "tv_shows": [],
        "music_artists": [],
        "organizations": [],
        "events": [],
        "franchises": [],
        "generic_keywords": []
    }
    """

    entities = {
        "people": [],
        "movies": [],
        "tv_shows": [],
        "music_artists": [],
        "organizations": [],
        "events": [],
        "franchises": [],
        "generic_keywords": [],
    }

    #
    # Very first version.
    #
    # Find quoted titles.
    #

    quoted = re.findall(r"[\"']([^\"']+)[\"']", headline)

    for title in quoted:

        if len(title) > 2:
            entities["movies"].append(title)

    #
    # Capitalized name sequences.
    #

    names = re.findall(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b",
        headline,
    )

    for name in names:

        name = normalize(name)

        if name not in entities["people"]:
            entities["people"].append(name)

    #
    # Generic keywords.
    #

    ignore = {
        "The",
        "A",
        "An",
        "And",
        "For",
        "Of",
        "In",
        "On",
        "With",
    }

    words = re.findall(r"[A-Za-z0-9']+", headline)

    for word in words:

        if len(word) < 4:
            continue

        if word in ignore:
            continue

        if word not in entities["generic_keywords"]:
            entities["generic_keywords"].append(word)

    return entities


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    headline = (
        "Taylor Swift and Travis Kelce's expected "
        "wedding celebrations approach"
    )

    from pprint import pprint

    pprint(extract_entities(headline))