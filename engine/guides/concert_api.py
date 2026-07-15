"""
===========================================
ShowBiz Concert API
Version 1.0
===========================================

Purpose:
    Handle all Ticketmaster API
    communication for the
    ShowBiz Concert Guide.
"""

import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()


TICKETMASTER_URL = (
    "https://app.ticketmaster.com/"
    "discovery/v2/events.json"
)


PAGE_SIZE = 50

MAX_PAGES = 20

REQUEST_DELAY = 0.35

TIMEOUT = 20


def get_api_key():
    """
    Return the Ticketmaster API key.
    """

    return os.getenv(
        "TICKETMASTER_API_KEY"
    )


def request_ticketmaster(
    params=None,
    endpoint=None,
):
    """
    Make a Ticketmaster request.
    """

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

        endpoint = TICKETMASTER_URL

        params.setdefault(
            "countryCode",
            "US",
        )

        params.setdefault(
            "size",
            PAGE_SIZE,
        )

        params.setdefault(
            "sort",
            "date,asc",
        )

    try:

        response = requests.get(
            endpoint,
            params=params,
            timeout=TIMEOUT,
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


def fetch_ticketmaster_events(
    start_date,
    classification="Music",
    max_pages=MAX_PAGES,
):
    """
    Download all upcoming events
    from Ticketmaster.
    """

    all_events = []

    for page in range(max_pages):

        if page:

            time.sleep(
                REQUEST_DELAY
            )

        data = request_ticketmaster(
            {
                "classificationName": classification,
                "page": page,
                "startDateTime": (
                    start_date
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

        if not events:

            break

        all_events.extend(
            events
        )

        if len(events) < PAGE_SIZE:

            break

    #
    # Remove duplicate Ticketmaster IDs.
    #

    unique = {}

    for event in all_events:

        event_id = event.get(
            "id"
        )

        if (
            event_id
            and event_id
            not in unique
        ):

            unique[event_id] = event

    return list(
        unique.values()
    )

def fetch_artist_events(
    artist_id,
    artist_name="",
    max_pages=MAX_PAGES,
):
    """
    Download every available Ticketmaster
    event for a single attraction.
    """

    if not artist_id:
        return []

    print()
    print(f"Artist: {artist_name}")
    print(f"Attraction ID: {artist_id}")

    all_events = []

    for page in range(max_pages):

        if page:
            time.sleep(REQUEST_DELAY)

        data = request_ticketmaster(
            {
                "attractionId": artist_id,
                "page": page,
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

        if not events:
            break

        print(
            f"  Page {page}: {len(events)} events"
        )

        for event in events[:3]:

            print(
                "   -",
                event.get(
                    "name",
                    ""
                )
            )

        all_events.extend(
            events
        )

        if len(events) < PAGE_SIZE:
            break

    unique = {}

    for event in all_events:

        event_id = event.get(
            "id"
        )

        if event_id:

            unique[event_id] = event

    print(
        f"Total unique events: {len(unique)}"
    )

    return list(
        unique.values()
    )