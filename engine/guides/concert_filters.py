"""
===========================================
ShowBiz Concert Filters
Version 2.0
===========================================

Filters out events that should never
appear in the national ShowBiz
Concert Guide.

Author:
    ShowBiz Automation
"""

import re


TITLE_FILTERS = (

    "vip",
    "parking",
    "fast lane",
    "fast pass",
    "club level seating",
    "premium seating",
    "hospitality package",
    "meet & greet",
    "meet and greet",
    "season pass",
    "3 day pass",
    "2 day pass",
    "weekend pass",
    "family dance",
    "dance party",
    "emo night",
    "karaoke",
    "brunch",
    "day out with thomas",
    "kids day",
    "silent disco",
    "paint & sip",
    "paint and sip",
    "bingo",

)


VENUE_FILTERS = (

    "nightclub",
    "bar",
    "pub",
    "taproom",
    "brewery",

)


TRIBUTE_FILTERS = (

    "tribute",
    "tributes",
    "experience",
    "vs.",
    "vs ",
    "salute to",
    "performing the music of",
    "music of",
    "remembering",
    "celebration of",

)


SUPPLEMENTAL_FILTERS = (

    "q&a",
    "podcast",
    "after party",
    "soundcheck",
    "listening party",

)


def _normalize(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    return " ".join(
        text.split()
    )


def should_keep(concert):

    title = _normalize(
        concert.get(
            "title",
            "",
        )
    )

    artist = _normalize(
        concert.get(
            "artist",
            "",
        )
    )

    venue = _normalize(
        concert.get(
            "venue",
            "",
        )
    )

    #
    # Reject generic attractions that
    # are not touring artists.
    #

    generic_artists = (

        "happy hour",
        "princess concert",
        "summer school",
        "festival",
        "symphony",
        "orchestra",
        "series",
        "experience",
        "tribute",

    )

    for phrase in generic_artists:

        if phrase in artist:

            return False

    #
    # Reject unwanted titles.
    #

    for phrase in TITLE_FILTERS:

        if phrase in title:

            return False

    #
    # Reject unwanted venues.
    #

    for phrase in VENUE_FILTERS:

        if phrase in venue:

            return False

    #
    # Reject tribute / experience events.
    #

    for phrase in TRIBUTE_FILTERS:

        if phrase in title:

            return False

    #
    # Reject supplemental events.
    #

    for phrase in SUPPLEMENTAL_FILTERS:

        if phrase in title:

            return False

    #
    # Must have an artist.
    #

    if not artist:

        return False

    #
    # Ignore obvious venue/program names.
    #

    if artist == venue:

        return False

    #
    # Ignore one-off venue programs.
    #

    if (
        "night" in artist
        or "hour" in artist
        or "session" in artist
    ):

        return False

    return True


def remove_duplicates(concerts):

    seen = set()

    results = []

    for concert in concerts:

        key = (

            _normalize(
                concert.get(
                    "title",
                    "",
                )
            ),

            _normalize(
                concert.get(
                    "venue",
                    "",
                )
            ),

            concert.get(
                "event_date",
                "",
            ),

        )

        if key in seen:

            continue

        seen.add(key)

        results.append(concert)

    return results


def remove_duplicate_artists(concerts):

    best = {}

    for concert in concerts:

        artist = _normalize(
            concert.get(
                "title",
                "",
            )
        )

        score = concert.get(
            "editorial_score",
            0,
        )

        existing = best.get(
            artist
        )

        if existing is None:

            best[artist] = concert

            continue

        if score > existing.get(
            "editorial_score",
            0,
        ):

            best[artist] = concert

    return list(
        best.values()
    )


def filter_concerts(concerts):

    concerts = [

        concert

        for concert in concerts

        if should_keep(
            concert
        )

    ]

    concerts = remove_duplicates(
        concerts
    )

    concerts = remove_duplicate_artists(
        concerts
    )

    return concerts


if __name__ == "__main__":

    from engine.guides.concert_data import (
        get_concert_guide,
    )

    concerts = get_concert_guide(
        limit=100
    )

    print()

    print(
        "Before:",
        len(concerts),
    )

    concerts = filter_concerts(
        concerts
    )

    print(
        "After:",
        len(concerts),
    )

    print()

    for concert in concerts[:20]:

        print(
            concert["event_date"],
            "-",
            concert["title"],
        )