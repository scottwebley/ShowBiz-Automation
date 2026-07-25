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
print("ENTITY_EXTRACTOR VERSION 3.4 TEST")
print(__file__)


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
    "Warner Bros.",
    "Warner Brothers",
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
    "The Morning Show",
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

COMMON_NON_NAME_WORDS = {
    # Existing words...
    "New", "Latest", "Breaking", "Update", "Live", "Exclusive",
    "Alert", "Watch", "Today", "Tomorrow", "Yesterday",

    # Organizations / generic nouns
    "Netflix", "Disney", "Marvel", "DC", "AEW", "WWE",
    "Music", "Movie", "Movies", "Film", "TV", "Television",
    "Streaming", "Gaming", "Broadway", "Theater", "Theatre",
    "Concert", "Festival", "Award", "Awards",

    # False-name starters
    "Thousands",
    "Thousand",
    "Hundreds",
    "Hundred",
    "Millions",
    "Million",
    "Billions",
    "Billion",
    "Dozens",
    "Several",
    "Many",
    "Most",
    "Some",
    "Few",
    "Countless",
    "Multiple",
    "Numerous",
    "More",
    "Less",
    "Over",
    "Under",
    "Around",
    "Nearly",
    "Almost",
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

    if first in COMMON_NON_NAME_WORDS:
        return False

    if second in COMMON_NON_NAME_WORDS:
        return False

    #
    # Reject abbreviation pairs like:
    # AEW WBD
    # ABC NBC
    #

    if first.isupper() and second.isupper():
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

    protected_titles = list(KNOWN_TITLES)

    working = headline

    #
    # Remove quoted titles first so they don't leave
    # stray capitalized words behind.
    #

    for title in _extract_quoted_titles(headline):
        working = working.replace(title, "")

    #
    # Remove known titles so they cannot be
    # mistaken for people.
    #

    for title in protected_titles:
        working = working.replace(title, "")

    #
    # Protect well-known brands so they are not
    # broken into fake people like "Video AI".
    #

    protected_brands = (
        "Prime Video",
        "Amazon Prime Video",
        "Apple TV+",
        "Apple TV",
        "Disney+",
        "Disney Plus",
        "Paramount+",
        "Paramount Plus",
        "Warner Bros.",
        "Warner Bros",
        "HBO Max",
        "Prime",
        "Netflix",
        "Peacock",
        "Hulu",
        "Max",
    )

    for brand in protected_brands:
        working = re.sub(
            rf"\b{re.escape(brand)}\b",
            " ",
            working,
            flags=re.IGNORECASE,
        )

    tokens = []

    bad_person_tokens = {
        "AI",
        "TV",
        "Video",
        "Streaming",
        "Stream",
        "Movie",
        "Movies",
        "Series",
        "Season",
        "Episode",
        "Prime",
        "Amazon",
        "Netflix",
        "Disney",
        "Apple",
        "Peacock",
        "Hulu",
        "Max",
        "Plus",
    }

    for token in re.findall(r"[A-Z][A-Za-z0-9'.&+-]*", working):

        clean = _clean_person_token(token)

        if not clean:
            continue

        if clean in bad_person_tokens:
            continue

        if clean in {
            "Bros",
            "Inc",
            "Corp",
            "Co",
            "LLC",
            "Ltd",
            "Group",
            "Studios",
            "Studio",
            "Discovery",
            "Pictures",
            "Entertainment",
            "Media",
        }:
            continue

        tokens.append(clean)

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

        "Singer",
        "Actor",
        "Actress",
        "Musician",
        "Rapper",
        "Producer",
        "Director",
        "Filmmaker",
        "Writer",
        "Author",
        "Composer",
        "Comedian",
        "DJ",
        "Band",
        "Group",
        "Performer",
        "Star",
        "Celebrity",

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
        "Gets",
        "Get",
        "Breaks",
        "Break",
        "Sends",
        "Send",
        "Signals",
        "Signal",
        "Turns",
        "Turn",
        "Blocks",
        "Block",
        "Judge",
        "Judges",
        "Powers",
        "Prepares",

        "Media",
        "Giants",
        "Shock",
        "Shocks",
        "Tie",
        "Up",
        "Through",
        "Industry",
        "Entertainment",
        "Streaming",
        "Gaming",
        "Music",
        "Television",
        "Legal",
        "Fight",
        "Merger",
        "Frozen",
        "Costly",
        "Lawsuit",
        "Lawsuits",
        "Trial",
        "Regulators",
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

    generic_words = {
        "Toward",
        "Towards",
        "Against",
        "Across",
        "Inside",
        "Outside",
        "During",
        "Following",
        "Starting",
        "Ending",
        "Rolling",
        "Line",
        "Video",
        "Prime",
        "Streaming",
        "Movie",
        "Series",
        "Season",
        "Episode",
        "AI",
        "TV",
    }

    def looks_like_real_name(first, second):

        if first in generic_words or second in generic_words:
            return False

        if first.endswith("ly") or second.endswith("ly"):
            return False

        if not (
            len(first) >= 2
            and len(second) >= 2
            and first[0].isupper()
            and second[0].isupper()
        ):
            return False

        return True

    i = 0

    while i < len(tokens):

        current = _clean_person_token(tokens[i])

        if (
            current == "The"
            and i + 1 < len(tokens)
            and tokens[i + 1] == "Rock"
        ):
            people.append(normalize("The Rock"))
            i += 2
            continue

        if (
            current in {
                "Starring",
                "Featuring",
                "Feature",
            }
            and i + 2 < len(tokens)
        ):

            first = _clean_person_token(tokens[i + 1])
            second = _clean_person_token(tokens[i + 2])

            if (
                looks_like_real_name(first, second)
                and _is_valid_person(first, second)
            ):
                people.append(normalize(f"{first} {second}"))
                i += 2
                continue

        if i + 1 < len(tokens):

            first = current
            second = _clean_person_token(tokens[i + 1])

            if first in reject_first:
                i += 1
                continue

            if second in reject_second:
                i += 1
                continue

            if (
                first in TITLE_WORDS
                or second in TITLE_WORDS
            ):
                i += 1
                continue

            pair = f"{first} {second}".lower()

            if any(
                pair in title.lower()
                for title in KNOWN_TITLES
            ):
                i += 1
                continue

            if (
                f"{first} {second}" in ORGANIZATIONS
                or first in ORGANIZATIONS
                or second in ORGANIZATIONS
            ):
                i += 1
                continue

            if second in {
                "Block",
                "Shock",
                "Giants",
                "Through",
                "Up",
            }:
                i += 1
                continue

            if (
                looks_like_real_name(first, second)
                and _is_valid_person(first, second)
            ):
                people.append(normalize(f"{first} {second}"))
                i += 2
                continue

        i += 1

    return list(dict.fromkeys(people))
# --------------------------------------------------
# QUOTED TITLES
# --------------------------------------------------


def _extract_quoted_titles(headline: str):
    """
    Extract movie/TV titles enclosed in quotation marks.

    Supports:
        "Blade Runner 2099"
        'Blade Runner 2099'
        “Blade Runner 2099”
        ‘Blade Runner 2099’
    """

    titles = []

    patterns = [
        r'"([^"]+)"',
        r"'([^']+)'",
        r"“([^”]+)”",
        r"‘([^’]+)’",
    ]

    for pattern in patterns:
        for title in re.findall(pattern, headline):
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
    "Singer Chris Brown pleads guilty over bottle attack at a London nightclub",
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