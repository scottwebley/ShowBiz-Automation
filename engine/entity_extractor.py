"""
===========================================
ShowBiz Entity Extractor
Version 3.4
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
    "Disney+",
    "Pixar",
    "Marvel",
    "Lucasfilm",
    "Apple",
    "Apple TV",
    "Amazon",
    "Prime Video",
    "HBO",
    "Max",
    "Paramount",
    "NBC",
    "CBS",
    "ABC",
    "FOX",
    "FX",
    "FX Networks",
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

    "Television Academy",
    "Academy of Television Arts and Sciences",

    "Emmy Awards",
    "Emmys",
    "Oscars",
    "Golden Globes",
    "Grammy Awards",
    "Tony Awards",
}


# --------------------------------------------------
# KNOWN ENTERTAINMENT TITLES
# --------------------------------------------------

KNOWN_TITLES = {
    "Alien: Earth",
    "Stranger Things",
    "The Last of Us",
    "Total Eclipse of the Heart",
    "Game of Thrones",
    "House of the Dragon",
    "The Walking Dead",
    "Yellowstone",
    "Moana",
    "Avatar",
    "Frozen",
    "Wicked",
    "Barbie",
    "Titanic",
    "Batman",
    "Superman",
    "Godzilla",
}




# --------------------------------------------------
# KNOWN MUSIC ARTISTS
# --------------------------------------------------

KNOWN_MUSIC_ARTISTS = {
    "Destiny's Child",
    "Taylor Swift",
    "Beyoncé",
    "Drake",
    "Metallica",
    "The Beatles",
    "Backstreet Boys",
    "NSYNC",
    "BTS",
    "BLACKPINK",
}

# --------------------------------------------------
# LOCATION / CONTEXT WORDS
# --------------------------------------------------

LOCATION_WORDS = {
    "Indianapolis",
    "New",
    "York",
    "Los",
    "Angeles",
    "Chicago",
    "Boston",
    "Miami",
    "Dallas",
    "London",
    "Paris",
    "Toronto",
    "Austin",
    "Atlanta",
    "Nashville",
    "Hollywood",
    "California",
    "Texas",
    "Florida",
}


# --------------------------------------------------
# TITLE WORDS
# --------------------------------------------------

TITLE_WORDS = {
    "Total",
    "Eclipse",
    "Heart",
    "Moana",
    "Avatar",
    "Frozen",
    "Wicked",
    "Barbie",
    "Titanic",
    "Batman",
    "Superman",
    "Godzilla",
}


TITLE_PHRASES = {
    "Total Eclipse",
    "Eclipse Heart",
    "Total Eclipse of the Heart",
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

    return ALIASES.get(
        text,
        text,
    )



def _clean_person_token(
    token: str,
) -> str:

    token = token.strip(
        ".,:;!?()[]{}\"'"
    )

    if token.endswith("'s"):

        token = token[:-2]

    elif token.endswith("’s"):

        token = token[:-2]

    return token



def _is_known_title_fragment(
    text: str,
) -> bool:

    clean = text.strip()

    for title in KNOWN_TITLES:

        if clean.lower() == title.lower():

            return True

    return False



def _is_title_fragment(
    first: str,
    second: str,
) -> bool:

    phrase = (
        f"{first} {second}"
    )

    if phrase in TITLE_PHRASES:

        return True


    if (
        first in TITLE_WORDS
        and second in TITLE_WORDS
    ):

        return True


    return False



def _is_valid_person(
    first: str,
    second: str,
) -> bool:

    first = _clean_person_token(
        first
    )

    second = _clean_person_token(
        second
    )


    if len(first) < 2 or len(second) < 2:

        return False


    if first == second:

        return False


    if first in STOP_NAME_WORDS:

        return False


    if second in STOP_NAME_WORDS:

        return False


    if first in LOCATION_WORDS:

        return False


    if second in LOCATION_WORDS:

        return False


    if _is_title_fragment(
        first,
        second,
    ):

        return False


    if _is_known_title_fragment(
        f"{first} {second}",
    ):

        return False


    if first in ORGANIZATIONS:

        return False


    if second in ORGANIZATIONS:

        return False


    if first.isdigit() or second.isdigit():

        return False


    return True



# --------------------------------------------------
# PEOPLE
# --------------------------------------------------


def _extract_people(
    headline: str,
):

    people = []

    protected_titles = list(
        KNOWN_TITLES
    )

    working = headline

    #
    # Remove known titles so they cannot be
    # mistaken for people.
    #

    for title in protected_titles:

        working = working.replace(
            title,
            "",
        )

    tokens = re.findall(
        r"[A-Z][A-Za-z0-9']*",
        working,
    )

    reject_first = {

        "Awards",
        "Award",
        "Host",
        "Hosts",
        "Hosting",
        "Primetime",
        "Academy",
        "Golden",
        "Grammy",
        "Oscar",
        "Oscars",
        "Emmy",
        "Emmys",
        "Movie",
        "Movies",
        "Series",
        "Season",
        "Episode",

        # Headline verbs

        "Celebrates",
        "Celebrating",
        "Announces",
        "Announced",
        "Returns",
        "Return",
        "Wins",
        "Win",
        "Upcoming",
        "Featuring",
        "Feature",
        "Reaching",

    }

    reject_second = {

        "Awards",
        "Award",
        "September",
        "October",
        "November",
        "December",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "Emmy",
        "Emmys",
        "Oscar",
        "Oscars",

    }

    i = 0

    while i < len(tokens):

        current = _clean_person_token(
            tokens[i]
        )

        #
        # Alias:
        # The Rock -> Dwayne Johnson
        #

        if (
            current == "The"
            and i + 1 < len(tokens)
            and tokens[i + 1] == "Rock"
        ):

            people.append(
                normalize(
                    "The Rock"
                )
            )

            i += 2
            continue

        #
        # Pattern:
        # Starring Cole Escola
        # Featuring Taylor Swift
        #

        if (
            current in {
                "Starring",
                "Featuring",
                "Feature",
            }
            and i + 2 < len(tokens)
        ):

            first = _clean_person_token(
                tokens[i + 1]
            )

            second = _clean_person_token(
                tokens[i + 2]
            )

            if _is_valid_person(
                first,
                second,
            ):

                people.append(
                    normalize(
                        f"{first} {second}"
                    )
                )

                i += 3
                continue

        #
        # Standard First Last extraction
        #

        if i + 1 < len(tokens):

            first = current

            second = _clean_person_token(
                tokens[i + 1]
            )

            if first in reject_first:

                i += 1
                continue

            if second in reject_second:

                i += 1
                continue

            if _is_valid_person(
                first,
                second,
            ):

                people.append(
                    normalize(
                        f"{first} {second}"
                    )
                )

                i += 2
                continue

        i += 1

    return list(
        dict.fromkeys(
            people
        )
    )
# --------------------------------------------------
# QUOTED TITLES
# --------------------------------------------------


def _extract_quoted_titles(
    headline: str,
):

    """
    Extract titles enclosed in real quotation marks.

    Ignore apostrophes used in contractions
    and possessives.
    """

    titles = []

    #
    # Double quotes
    #

    for title in re.findall(
        r'"([^"]+)"',
        headline,
    ):

        title = title.strip()

        if len(title) >= 2 and title not in titles:
            titles.append(title)

    #
    # Smart quotes
    #

    for title in re.findall(
        r'“([^”]+)”',
        headline,
    ):

        title = title.strip()

        if len(title) >= 2 and title not in titles:
            titles.append(title)

    return titles



# --------------------------------------------------
# ENTITY EXTRACTION
# --------------------------------------------------


def extract_entities(
    headline: str,
):

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


    quoted_titles = _extract_quoted_titles(
        headline
    )


    entities["movies"] = list(
        quoted_titles
    )


    headline_lower = headline.lower()


    # ----------------------------------------------
    # Organizations
    # ----------------------------------------------

    for org in sorted(
        ORGANIZATIONS,
        key=len,
        reverse=True,
    ):

        if org.lower() in headline_lower:

            entities["organizations"].append(
                org
            )


    # ----------------------------------------------
    # Known titles
    # ----------------------------------------------

    for title in sorted(
        KNOWN_TITLES,
        key=len,
        reverse=True,
    ):

        if title.lower() in headline_lower:

            entities["tv_shows"].append(
                title
            )


    # ----------------------------------------------
    # People
    # ----------------------------------------------

    entities["people"] = _extract_people(
        headline
    )


    filtered_people = []


    for person in entities["people"]:

        if any(
            word in TITLE_WORDS
            for word in person.split()
        ):

            continue


        if person in filtered_people:

            continue


        filtered_people.append(
            person
        )


    entities["people"] = filtered_people



    # ----------------------------------------------
    # Known music artists
    # ----------------------------------------------

    matched_music_words = set()

    for artist in sorted(KNOWN_MUSIC_ARTISTS, key=len, reverse=True):
        if artist.lower() in headline_lower:
            if artist not in entities["music_artists"]:
                entities["music_artists"].append(artist)
            for token in re.findall(r"[A-Za-z0-9']+", artist):
                matched_music_words.add(token.upper())

    # ----------------------------------------------
    # Music-style uppercase detection
    # ----------------------------------------------

    excluded_music = {

        token.lower()

        for value in (
            entities["organizations"]
        )

        for token in re.findall(
            r"[A-Za-z0-9']+",
            value,
        )

    }

    IGNORE_MUSIC_WORDS = {
        "ALERT",
        "BREAKING",
        "NEW",
        "NEWS",
        "MUSIC",
        "LIVE",
        "WATCH",
        "VIDEO",
        "EXCLUSIVE",
        "UPDATE",
        "TODAY",
        "NOW",
    }


    for word in re.findall(
        r"\b[A-Z][A-Za-z0-9']+\b",
        headline,
    ):

        clean = _clean_person_token(
            word
        )

        if (

            clean.isupper()

            and len(clean) >= 3

            and clean not in IGNORE_MUSIC_WORDS

            and clean.upper() not in matched_music_words

            and clean.lower()
            not in excluded_music

            and clean
            not in entities["music_artists"]

        ):

            entities["music_artists"].append(
                clean
            )
                # ----------------------------------------------
    # Generic keywords
    # ----------------------------------------------

    excluded = set()

    for value in (

        entities["people"]

        + entities["organizations"]

        + entities["music_artists"]

        + quoted_titles

        + entities["tv_shows"]

    ):

        for token in re.findall(
            r"[A-Za-z0-9']+",
            value,
        ):

            excluded.add(
                token.lower()
            )


    skip_words = {

        *IGNORE_KEYWORDS,

        "your",

        "their",

        "listeners",

        "listener",

        "surpasses",

        "decoding",

        "views",

        "view",

        "challenge",

        "challenges",

        "announces",

        "announced",

        "expected",

        "breaking",

        "latest",

        "more",

        "also",

        "has",

        "have",

        "had",

        "season",

        "cast",

        "revealed",

        "reveals",

        "what",

    }


    for word in re.findall(
        r"[A-Za-z0-9']+",
        headline,
    ):

        clean = _clean_person_token(
            word
        )

        if not clean:
            continue

        #
        # Ignore pure numbers.
        #

        if clean.isdigit():
            continue

        #
        # "The Rock" is already normalized to
        # Dwayne Johnson.
        #

        if clean == "Rock":
            continue

        lower = clean.lower()

        if len(lower) < 4:
            continue

        if lower in excluded:
            continue

        if lower in skip_words:
            continue

        if clean in LOCATION_WORDS:
            continue

        if clean in TITLE_WORDS:
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
    "ALERT ALERT! NEW DESTINY'S CHILD MUSIC!! ALERT ALERT!",
]


    for headline in tests:

        print()

        print("=" * 60)

        print(headline)

        print("=" * 60)


        pprint(
            extract_entities(
                headline
            )
        )