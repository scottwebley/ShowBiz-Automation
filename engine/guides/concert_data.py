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


def request_ticketmaster(
    params=None,
    endpoint=None,
):

    api_key = get_api_key()

    if not api_key:

        print(
            "TICKETMASTER_API_KEY not found."
        )

        return {}

    if params is None:

        params = {}

    params.setdefault(
        "apikey",
        api_key,
    )

    if endpoint is None:

        endpoint = (
            TICKETMASTER_URL
        )

        params.setdefault(
            "countryCode",
            "US",
        )

        params.setdefault(
            "size",
            50,
        )

        params.setdefault(
            "sort",
            "date,asc",
        )

    try:

        response = requests.get(
            endpoint,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:

        print()

        print(
            "Ticketmaster request failed"
        )

        print(
            endpoint
        )

        print(
            exc
        )

        return {}
def get_attraction_image(
    attraction_ids,
):
    """
    DEBUG VERSION

    Inspect one attraction record so
    we can see what the Ticketmaster
    Attractions API actually contains.
    """

    if not attraction_ids:

        return ""

    attraction_id = attraction_ids[0]

    endpoint = (
        "https://app.ticketmaster.com/"
        f"discovery/v2/attractions/{attraction_id}.json"
    )

    data = request_ticketmaster(
        endpoint=endpoint,
    )

    print()
    print("========================================")
    print("TICKETMASTER ATTRACTION DEBUG")
    print("========================================")
    print()

    print("Attraction ID:")
    print(attraction_id)
    print()

    print("Keys:")
    print(sorted(data.keys()))
    print()

    images = data.get(
        "images",
        []
    )

    print(
        "Images:",
        len(images)
    )

    for image in images[:10]:

        print(
            image.get(
                "ratio"
            ),
            image.get(
                "width"
            ),
            "x",
            image.get(
                "height"
            ),
            image.get(
                "url"
            ),
        )

    print()

    print("URL:")
    print(
        data.get(
            "url"
        )
    )

    print()

    print("Name:")
    print(
        data.get(
            "name"
        )
    )

    print()

    return ""  
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

        #
        # DEBUG
        #
        if "usher raymond" in title.lower():

            print()
            print("=" * 60)
            print("DEBUG EVENT:", title)
            print("=" * 60)

            for image in event.get(
                "images",
                [],
            ):

                print(
                    f"ratio={image.get('ratio')}  "
                    f"{image.get('width')}x{image.get('height')}"
                )

                print(
                    image.get(
                        "url",
                        "",
                    )
                )

                print()

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

        attraction_ids = []

        for attraction in embedded.get(
            "attractions",
            []
        ):

            attraction_id = attraction.get(
                "id"
            )

            if attraction_id:

                attraction_ids.append(
                    attraction_id
                )

        #
        # Choose the best Ticketmaster
        # concert artwork.
        #
        poster = ""

        best_score = -1

        for image in event.get(
            "images",
            [],
        ):

            url = image.get(
                "url",
                "",
            )

            width = image.get(
                "width",
                0,
            )

            height = image.get(
                "height",
                0,
            )

            score = width * height

            if "_SOURCE" in url:

                score += 1000000000

            elif "_TABLET_LANDSCAPE_LARGE" in url:

                score += 500000000

            elif "_TABLET_LANDSCAPE" in url:

                score += 250000000

            elif "_ARTIST_PAGE" in url:

                score += 100000000

            elif "_RETINA_LANDSCAPE" in url:

                score += 75000000

            elif "_RETINA_PORTRAIT" in url:

                score += 50000000

            elif "_EVENT_DETAIL_PAGE" in url:

                score += 25000000

            if score > best_score:

                best_score = score
                poster = url

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
                "id": event.get("id"),
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
                "poster": poster,
                "url": event.get(
                    "url",
                    ""
                ),
                "overview": venue,
                "attraction_ids": attraction_ids,
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