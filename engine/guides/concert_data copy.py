"""
===========================================
ShowBiz Concert Data
Version 1.0
===========================================

Purpose:
    Retrieve upcoming concerts from
    the Ticketmaster Discovery API
    for the ShowBiz Concert Guide.

Author:
    ShowBiz Automation
"""

import os

from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()


TICKETMASTER_URL = (
    "https://app.ticketmaster.com/discovery/v2/events.json"
)


def get_api_key():

    return os.getenv(
        "TICKETMASTER_API_KEY"
    )


def format_date(date_string):

    if not date_string:
        return ""

    try:

        return datetime.strptime(
            date_string,
            "%Y-%m-%d",
        ).strftime("%B %d, %Y")

    except Exception:

        return date_string


def request_ticketmaster(params=None):

    api_key = get_api_key()

    if not api_key:

        print(
            "TICKETMASTER_API_KEY not found."
        )

        return {}

    if params is None:

        params = {}

    params.update(
        {
            "apikey": api_key,
            "countryCode": "US",
            "size": 50,
            "sort": "date,asc",
        }
    )

    try:

        response = requests.get(
            TICKETMASTER_URL,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:

        print(
            "Ticketmaster request failed:",
            exc,
        )

        return {}
def normalize_events(events, limit=24):

    items = []

    blocked = (

        "season pass",
        "day pass",
        "weekend pass",
        "hotel package",
        "ticket package",
        "official caesars ticket",
        "vip package",
        "vip experience",
        "parking",
        "fast lane",
        "fast pass",
        "club access",
        "lounge",
        "table reservation",
        "meet & greet",
        "entry pass",
        "entry to all shows",
        "blue friday special",
        "package",
        "add-on",
        "upgrade",

    )

    for event in events:

        title = event.get(
            "name",
            "",
        ).strip()

        if not title:
            continue

        lower = title.lower()

        if any(
            word in lower
            for word in blocked
        ):
            continue

        dates = event.get(
            "dates",
            {}
        )

        start = dates.get(
            "start",
            {}
        )

        embedded = event.get(
            "_embedded",
            {}
        )

        venues = embedded.get(
            "venues",
            []
        )

        venue = ""
        city = ""

        if venues:

            venue = venues[0].get(
                "name",
                ""
            )

            city = (
                venues[0]
                .get(
                    "city",
                    {}
                )
                .get(
                    "name",
                    ""
                )
            )

        image = ""

        images = event.get(
            "images",
            []
        )

        if images:

            image = max(
                images,
                key=lambda x: x.get(
                    "width",
                    0,
                ),
            ).get(
                "url",
                ""
            )

        classification = ""

        classifications = event.get(
            "classifications",
            []
        )

        if classifications:

            classification = (
                classifications[0]
                .get(
                    "segment",
                    {}
                )
                .get(
                    "name",
                    ""
                )
            )

        items.append(
            {
                "id": event.get(
                    "id"
                ),
                "title": title,
                "event_date": format_date(
                    start.get(
                        "localDate",
                        ""
                    )
                ),
                "venue": venue,
                "city": city,
                "classification": classification,
                "poster": image,
                "url": event.get(
                    "url",
                    ""
                ),
                "overview": venue,
            }
        )

        if len(items) >= limit:
            break

    return items
def get_concert_guide(limit=24):
    """
    Return the best upcoming concerts.

    Rules:

    • Search multiple Ticketmaster pages.
    • Keep only future events.
    • Remove duplicate Ticketmaster IDs.
    • Sort chronologically.
    """

    today = datetime.today().date()

    all_events = []

    #
    # Search up to 10 pages
    # (approximately 500 events).
    #
    for page in range(10):

        data = request_ticketmaster(
            {
                "classificationName": "Music",
                "page": page,
                "startDateTime": (
                    today.strftime("%Y-%m-%d")
                    + "T00:00:00Z"
                ),
            }
        )

        events = (
            data.get(
                "_embedded",
                {}
            ).get(
                "events",
                []
            )
        )

        #
        # No more events.
        #
        if not events:
            break

        all_events.extend(
            events
        )

        #
        # Last page returned
        # fewer than 50 events.
        #
        if len(events) < 50:
            break

    #
    # Remove duplicate
    # Ticketmaster IDs.
    #
    unique = {}

    for event in all_events:

        event_id = event.get(
            "id"
        )

        if (
            event_id
            and event_id not in unique
        ):

            unique[event_id] = event

    concerts = normalize_events(
        list(
            unique.values()
        ),
        limit=5000,
    )

    upcoming = []

    for concert in concerts:

        try:

            event_date = datetime.strptime(
                concert["event_date"],
                "%B %d, %Y",
            ).date()

        except Exception:

            continue

        #
        # Ignore expired events.
        #
        if event_date < today:

            continue

        concert["_sort_date"] = event_date

        upcoming.append(
            concert
        )

    #
    # Chronological order.
    #
    upcoming.sort(
        key=lambda c: (
            c["_sort_date"],
            c.get(
                "title",
                "",
            ).lower(),
        )
    )

    #
    # Remove helper field.
    #
    for concert in upcoming:

        concert.pop(
            "_sort_date",
            None,
        )

    return upcoming[:limit]