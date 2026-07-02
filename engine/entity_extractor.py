"""
===========================================
ShowBiz Entity Extractor
Version 2.0
===========================================

Extracts entertainment entities from news
headlines for the Image Engine.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


ALIASES = {
    "The Rock": "Dwayne Johnson",
    "MCU": "Marvel Cinematic Universe",
    "LOTR": "The Lord of the Rings",
}


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
}


STOP_NAME_WORDS = {
    "Is",
    "Are",
    "Was",
    "Were",
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
    "More",
    "Also",
    "Star",
    "News",
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


def normalize(text: str) -> str:
    return ALIASES.get(text, text)


def _extract_people(headline: str):

    people = []

    tokens = re.findall(r"[A-Z][A-Za-z0-9']*", headline)

    i = 0

    while i < len(tokens):

        current = tokens[i]

        #
        # The Rock
        #

        if (
            current == "The"
            and i + 1 < len(tokens)
            and tokens[i + 1] == "Rock"
        ):

            people.append(normalize("The Rock"))
            i += 2
            continue

        #
        # First Last
        #

        if i + 1 < len(tokens):

            first = tokens[i]
            second = tokens[i + 1]

            if (
                first not in STOP_NAME_WORDS
                and second not in STOP_NAME_WORDS
            ):

                people.append(normalize(f"{first} {second}"))
                i += 2
                continue

        i += 1

    #
    # Remove duplicates preserving order.
    #

    seen = set()
    final = []

    for person in people:

        if person in seen:
            continue

        seen.add(person)
        final.append(person)

    return final


def extract_entities(headline: str):

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
    # Quoted titles.
    #

    for title in re.findall(r"[\"']([^\"']+)[\"']", headline):

        if len(title) > 2:

            entities["movies"].append(title)

    #
    # Organizations.
    #

    for org in ORGANIZATIONS:

        if org.lower() in headline.lower():

            entities["organizations"].append(org)

    #
    # People.
    #

    entities["people"] = _extract_people(headline)

    #
    # Generic keywords.
    #

    words = re.findall(r"[A-Za-z0-9']+", headline)

    for word in words:

        lower = word.lower()

        if len(lower) < 4:
            continue

        if lower in IGNORE_KEYWORDS:
            continue

        if word in entities["people"]:
            continue

        if word not in entities["generic_keywords"]:
            entities["generic_keywords"].append(word)

    return entities


if __name__ == "__main__":

    from pprint import pprint

    tests = [
        "The Rock Announces Big 'Moana 3' News",
        "Ashley Tisdale Is a Toxic Mom in New Netflix TV Show, Ali Wong & 1 More Also Star",
        "Taylor Swift and Travis Kelce's expected wedding celebrations approach",
    ]

    for headline in tests:

        print()
        print("=" * 60)
        print(headline)
        print("=" * 60)

        pprint(extract_entities(headline))