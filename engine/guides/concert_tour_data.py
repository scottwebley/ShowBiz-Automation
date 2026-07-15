"""
===========================================
ShowBiz Concert Tour Data
Version 1.0
===========================================

Purpose:
    Calculate tour information for
    normalized concert dictionaries.
"""

from collections import defaultdict
from datetime import datetime


DATE_FORMAT = "%b %d, %Y"


def parse_date(date_string):
    """
    Convert a formatted date into a
    datetime object.
    """

    if not date_string:
        return None

    try:
        return datetime.strptime(
            date_string,
            DATE_FORMAT,
        )
    except Exception:
        return None


def group_shows_by_artist(concerts):
    """
    Group concerts into tours.

    Prefer the Ticketmaster attraction ID.
    Fall back to the artist name if needed.
    """

    groups = defaultdict(list)

    for concert in concerts:

        artist_id = (
            concert.get(
                "artist_id",
                ""
            )
            .strip()
        )

        artist = (
            concert.get(
                "artist",
                ""
            )
            .strip()
            .lower()
        )

        if artist_id:

            key = f"id:{artist_id}"

        elif artist:

            key = f"artist:{artist}"

        else:

            key = (
                concert.get(
                    "title",
                    ""
                )
                .strip()
                .lower()
            )

        groups[key].append(
            concert
        )

    return groups


def sort_tour_dates(groups):
    """
    Sort every artist's shows by date.
    """

    for shows in groups.values():

        shows.sort(
            key=lambda show: (
                parse_date(
                    show.get(
                        "event_date",
                        "",
                    )
                )
                or datetime.max
            )
        )

    return groups


def build_stop(show):
    """
    Build a readable stop string.
    """

    city = show.get(
        "city",
        "",
    )

    state = show.get(
        "state",
        "",
    )

    date = show.get(
        "event_date",
        "",
    )

    location = city

    if state:
        location += f", {state}"

    if date:
        location += f" • {date}"

    return location


def apply_tour_data(concerts):
    """
    Calculate complete tour information
    for every concert in the list.
    """

    today = datetime.today()

    groups = group_shows_by_artist(
        concerts
    )

    groups = sort_tour_dates(
        groups
    )

    for shows in groups.values():

        if not shows:
            continue

        #
        # Keep only valid dated shows.
        #

        valid = []

        for show in shows:

            date = parse_date(
                show.get(
                    "event_date",
                    ""
                )
            )

            if date:

                valid.append(
                    (
                        date,
                        show,
                    )
                )

        if not valid:
            continue

        valid.sort(
            key=lambda item: item[0]
        )

        #
        # Entire tour.
        #

        start_date = valid[0][1].get(
            "event_date",
            ""
        )

        end_date = valid[-1][1].get(
            "event_date",
            ""
        )

        total = len(valid)

        final_stop = build_stop(
            valid[-1][1]
        )

        #
        # Find next upcoming show.
        #

        next_index = None

        for index, (date, _) in enumerate(valid):

            if date >= today:

                next_index = index
                break

        #
        # Apply to every concert.
        #

        for current_index, (_, show) in enumerate(valid):

            show[
                "tour_start_date"
            ] = start_date

            show[
                "tour_end_date"
            ] = end_date

            show[
                "total_tour_dates"
            ] = total

            if (
                next_index is not None
                and next_index < total
            ):

                show[
                    "next_stop"
                ] = build_stop(
                    valid[next_index][1]
                )

            else:

                show[
                    "next_stop"
                ] = ""

            show[
                "final_stop"
            ] = final_stop

    return concerts