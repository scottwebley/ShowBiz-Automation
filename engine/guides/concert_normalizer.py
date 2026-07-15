"""
===========================================
ShowBiz Concert Normalizer
Version 1.0
===========================================

Purpose:
    Normalize Ticketmaster events into
    the ShowBiz concert format.
"""

from datetime import datetime


def safe_get(value, default=""):
    """
    Return a clean string.
    """

    if value is None:
        return default

    return str(value).strip()


def format_date(date_string):
    """
    Convert a Ticketmaster UTC date
    into a friendly format.
    """

    if not date_string:
        return ""

    formats = (
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    )

    for fmt in formats:

        try:

            dt = datetime.strptime(
                date_string,
                fmt,
            )

            return dt.strftime(
                "%b %d, %Y"
            )

        except ValueError:

            pass

    return date_string


def normalize_city(event):
    """
    Return city.
    """

    return safe_get(
        event.get(
            "_embedded",
            {}
        ).get(
            "venues",
            [{}]
        )[0].get(
            "city",
            {}
        ).get(
            "name",
            ""
        )
    )


def normalize_state(event):
    """
    Return state.
    """

    venue = (
        event.get(
            "_embedded",
            {}
        ).get(
            "venues",
            [{}]
        )[0]
    )

    state = venue.get(
        "state",
        {}
    ).get(
        "stateCode",
        ""
    )

    if state:
        return state

    return venue.get(
        "country",
        {}
    ).get(
        "countryCode",
        ""
    )


def normalize_venue(event):
    """
    Return venue name.
    """

    return safe_get(
        event.get(
            "_embedded",
            {}
        ).get(
            "venues",
            [{}]
        )[0].get(
            "name",
            ""
        )
    )


def normalize_country(event):
    """
    Return country code.
    """

    return safe_get(
        event.get(
            "_embedded",
            {}
        ).get(
            "venues",
            [{}]
        )[0].get(
            "country",
            {}
        ).get(
            "countryCode",
            ""
        )
    )


def normalize_events(events):
    """
    Convert Ticketmaster events into
    ShowBiz concert dictionaries.
    """

    concerts = []

    for event in events:

        dates = event.get(
            "dates",
            {}
        ).get(
            "start",
            {}
        )

        attractions = (
            event.get(
                "_embedded",
                {}
            ).get(
                "attractions",
                []
            )
        )

        attraction_ids = []

        for attraction in attractions:

            attraction_id = attraction.get(
                "id"
            )

            if attraction_id:

                attraction_ids.append(
                    attraction_id
                )

        concerts.append(
            {
                "id": event.get(
                    "id",
                    ""
                ),
                "artist": event.get(
                    "name",
                    ""
                ),
                "venue": normalize_venue(
                    event
                ),
                "city": normalize_city(
                    event
                ),
                "state": normalize_state(
                    event
                ),
                "country": normalize_country(
                    event
                ),
                "event_date": format_date(
                    dates.get(
                        "localDate",
                        ""
                    )
                ),
                "ticket_url": event.get(
                    "url",
                    ""
                ),
                "attraction_ids": attraction_ids,
                "images": event.get(
                    "images",
                    [],
                ),
            }
        )

    return concerts


if __name__ == "__main__":

    print()

    print(
        "Concert Normalizer"
    )

    print(
        "Module loaded."
    )