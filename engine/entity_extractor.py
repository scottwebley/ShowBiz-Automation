"""
===========================================
ShowBiz Entity Extractor
Version 3.0
===========================================

Extracts entertainment entities from news
headlines for the Image Engine.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


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


def _clean_person_token(token: str) -> str:
    """
    Clean punctuation and possessives.
    """

    token = token.strip(
        ".,:;!?()[]{}\"'"
    )

    if token.endswith("'s"):
        token = token[:-2]

    elif token.endswith("’s"):
        token = token[:-2]

    return token

def _is_valid_person(first: str, second: str) -> bool:
    """
    Return True if two consecutive capitalized words
    are likely to represent a real person.
    """

    first = _clean_person_token(first)
    second = _clean_person_token(second)

    #
    # Basic length check.
    #

    if len(first) < 2 or len(second) < 2:
        return False

    #
    # Reject repeated words.
    #

    if first == second:
        return False

    #
    # Reject stop words.
    #

    if first in STOP_NAME_WORDS:
        return False

    if second in STOP_NAME_WORDS:
        return False

    #
    # Reject organizations.
    #

    if first in ORGANIZATIONS:
        return False

    if second in ORGANIZATIONS:
        return False

    #
    # Reject obvious headline words.
    #

    if first in {
        "An",
        "Big",
        "Breaking",
        "Latest",
        "New",
        "Close",
    }:
        return False

    if second in {
        "News",
        "Era",
        "Out",
    }:
        return False

    #
    # Reject numbers.
    #

    if first.isdigit() or second.isdigit():
        return False

    return True
# --------------------------------------------------
# PEOPLE
# --------------------------------------------------


def _extract_people(headline: str):
    """
    Extract likely person or performer names.

    Strategy:
      • Look for 2-word names.
      • Reject common verbs/connectors.
      • Preserve aliases.
    """

    people = []

    tokens = re.findall(
        r"[A-Z][A-Za-z0-9']*",
        headline,
    )

    i = 0

    while i < len(tokens):

        current = _clean_person_token(
            tokens[i]
        )

        #
        # Special case:
        # The Rock
        #

        if (
            current == "The"
            and i + 1 < len(tokens)
            and tokens[i + 1] == "Rock"
        ):

            people.append(
                normalize("The Rock")
            )

            i += 2
            continue

        #
        # First Last
        #

        if i + 1 < len(tokens):

            first = current

            second = _clean_person_token(
                tokens[i + 1]
            )

            if _is_valid_person(first, second):

                people.append(
                    normalize(
                        f"{first} {second}"
                    )
                )

                i += 2
                continue

        i += 1

    #
    # Remove duplicates.
    #

    seen = set()

    final = []

    for person in people:

        if person in seen:
            continue

        seen.add(person)

        final.append(person)

    return final


# --------------------------------------------------
# QUOTED TITLES
# --------------------------------------------------


def _extract_quoted_titles(
    headline: str,
):
    """
    Extract quoted titles.

    Example:

        RIIZE's 'Do Your Dance'

    becomes

        Do Your Dance
    """

    titles = []

    for title in re.findall(
        r"[\"']([^\"']+)[\"']",
        headline,
    ):

        title = title.strip()

        if len(title) < 2:
            continue

        if title not in titles:

            titles.append(title)

    return titles
# --------------------------------------------------
# ENTITY EXTRACTION
# --------------------------------------------------


def extract_entities(headline: str):
    """
    Extract entertainment entities from a headline.
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
    # Quoted titles
    #

    entities["movies"] = _extract_quoted_titles(
        headline
    )

    #
    # Organizations
    #

    for org in sorted(
        ORGANIZATIONS,
        key=len,
        reverse=True,
    ):

        if org.lower() in headline.lower():

            entities["organizations"].append(
                org
            )

    #
    # People
    #

    entities["people"] = _extract_people(
        headline
    )

    #
    # Single-word music artist detection.
    #

    for word in re.findall(
        r"\b[A-Z][A-Za-z0-9']+\b",
        headline,
    ):

        clean = _clean_person_token(word)

        if (
            clean.isupper()
            and len(clean) >= 3
            and clean not in entities["music_artists"]
        ):

            entities["music_artists"].append(
                clean
            )

    #
    # Generic keywords
    #

    words = re.findall(
        r"[A-Za-z0-9']+",
        headline,
    )

    #
    # Don't duplicate people, organizations,
    # or music artists.
    #

    excluded = {
        w.lower()
        for name in (
            entities["people"]
            + entities["organizations"]
            + entities["music_artists"]
        )
        for w in re.findall(
            r"[A-Za-z0-9']+",
            name,
        )
    }

    for word in words:

        clean = _clean_person_token(word)

        lower = clean.lower()

        if len(lower) < 4:
            continue

        if lower in IGNORE_KEYWORDS:
            continue

        if lower in excluded:
            continue

        if clean in entities["generic_keywords"]:
            continue

        entities["generic_keywords"].append(
            clean
        )

    return entities

# --------------------------------------------------
# TESTING
# --------------------------------------------------


if __name__ == "__main__":

    from pprint import pprint

    tests = [
        "Tiger in Your Sheets Has Kacey Musgraves Listeners Decoding a New Era",
        "RIIZE's 'Do Your Dance' Dance Challenge Surpasses 100M TikTok Views",
        "Taylor Swift and Travis Kelce's expected wedding celebrations approach",
        "The Rock Announces Big 'Moana 3' News",
    ]

    for headline in tests:

        print()
        print("=" * 60)
        print(headline)
        print("=" * 60)

        pprint(
            extract_entities(headline)
        )