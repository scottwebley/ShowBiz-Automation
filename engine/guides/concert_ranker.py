# ===========================
# PART 1 OF 2
# concert_ranker.py
# ===========================

"""
===========================================
ShowBiz Concert Ranker
Version 2.0
===========================================

Ranks concerts by editorial value
before they are sent to the AI.

Author:
    ShowBiz Automation
"""

import re

from engine.guides.concert_artist_rankings import (
    artist_score,
)


VENUE_BONUSES = {

    "stadium": 120,
    "field": 110,
    "arena": 100,
    "amphitheatre": 95,
    "amphitheater": 95,
    "bowl": 90,
    "center": 70,
    "centre": 70,
    "pavilion": 70,
    "theatre": 60,
    "theater": 60,
    "opera": 60,
    "casino": 35,

}


VENUE_PENALTIES = {

    "nightclub": -80,
    "night club": -80,
    "club": -60,
    "bar": -70,
    "saloon": -70,
    "lounge": -60,

}


TITLE_BONUSES = {

    "world tour": 120,
    "stadium tour": 120,
    "arena tour": 110,
    "farewell": 90,
    "reunion": 90,
    "festival": 85,
    "orchestra": 70,
    "symphony": 70,
    "live": 20,

}


TITLE_PENALTIES = {

    "dance party": -150,
    "emo night": -140,
    "club bangers": -140,
    "brunch": -130,
    "karaoke": -130,
    "day out with thomas": -200,
    "family dance": -170,
    "dj": -90,
    "after party": -120,
    "pool party": -140,
    "latin night": -120,

}


def _score_text(text, table):

    score = 0

    text = text.lower()

    for key, value in table.items():

        if key in text:

            score += value

    return score


def score_concert(concert):

    score = 0

    title = concert.get(
        "title",
        ""
    )

    venue = concert.get(
        "venue",
        ""
    )

    score += _score_text(
        title,
        TITLE_BONUSES,
    )

    score += _score_text(
        title,
        TITLE_PENALTIES,
    )

    score += _score_text(
        venue,
        VENUE_BONUSES,
    )

    score += _score_text(
        venue,
        VENUE_PENALTIES,
    )

    score += min(
        len(
            re.findall(
                r"\w+",
                title,
            )
        ),
        12,
    )

    #
    # Tour Intelligence bonuses.
    #

    total_dates = concert.get(
        "total_tour_dates",
        0,
    ) or 0

    if total_dates >= 50:

        score += 120

    elif total_dates >= 30:

        score += 90

    elif total_dates >= 15:

        score += 60

    elif total_dates >= 8:

        score += 35

    if concert.get(
        "next_stop"
    ):

        score += 25

    if concert.get(
        "final_stop"
    ):

        score += 15

    return score


def editorial_bonus(concert):

    score = 0

    title = concert.get(
        "title",
        ""
    ).lower()

    venue = concert.get(
        "venue",
        ""
    ).lower()
        #
    # Multi-artist concerts
    # are usually more notable.
    #
    if " feat." in title:

        score += 25

    if "&" in title:

        score += 15

    if "/" in title:

        score += 15

    #
    # Major venue bonus.
    #
    major_venues = (

        "madison square garden",
        "hollywood bowl",
        "red rocks",
        "ruoff",
        "the forum",
        "kia forum",
        "bridgestone",
        "crypto.com",
        "wembley",

    )

    for name in major_venues:

        if name in venue:

            score += 100

    #
    # Very small venue penalty.
    #
    small_venues = (

        "saloon",
        "bar",
        "pub",
        "taproom",
        "brewery",

    )

    for name in small_venues:

        if name in venue:

            score -= 60

    #
    # Tour Intelligence bonuses.
    #

    total_dates = concert.get(
        "total_tour_dates",
        0,
    ) or 0

    if total_dates >= 50:

        score += 100

    elif total_dates >= 30:

        score += 75

    elif total_dates >= 15:

        score += 50

    elif total_dates >= 8:

        score += 25

    if concert.get(
        "tour_start_date"
    ):

        score += 10

    if concert.get(
        "tour_end_date"
    ):

        score += 10

    return score


def rank_concerts(
    concerts,
    limit=24,
):

    ranked = []

    for concert in concerts:

        total = (
            score_concert(
                concert
            )
            + editorial_bonus(
                concert
            )
            + artist_score(
                concert.get(
                    "title",
                    "",
                )
            )
        )

        item = dict(
            concert
        )

        item["editorial_score"] = total

        ranked.append(
            item
        )

    ranked.sort(
        key=lambda c: (
            -c["editorial_score"],
            c.get(
                "event_date",
                "",
            ),
        )
    )

    return ranked[:limit]


def print_ranked(
    concerts,
    limit=24,
):

    ranked = rank_concerts(
        concerts,
        limit=limit,
    )

    for concert in ranked:

        print(
            f"{concert['editorial_score']:>4}  "
            f"{concert['event_date']}  "
            f"{concert['title']}  "
            f"| {concert['venue']}"
        )

    return ranked


if __name__ == "__main__":

    try:

        from engine.guides.concert_data import (
            get_concert_guide,
        )

        concerts = get_concert_guide(
            limit=100
        )

        print()
        print(
            "========================================"
        )
        print(
            "SHOWBIZ CONCERT RANKER"
        )
        print(
            "========================================"
        )
        print()

        print_ranked(
            concerts,
            limit=24,
        )

    except Exception as exc:

        print(
            "Concert ranker test failed:"
        )

        print(exc)