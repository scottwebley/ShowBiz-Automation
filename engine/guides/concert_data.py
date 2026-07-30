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

import json
import os

from datetime import datetime
from pathlib import Path

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
    seen = set()

    blocked = (
        "season pass",
        "day pass",
        "weekend pass",
        "hotel package",
        "hotel deals",
        "ticket package",
        "ticket + hotel",
        "ticket and hotel",
        "official ticket",
        "official ticket + hotel",
        "official caesars ticket",
        "travel package",
        "vacation package",
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

    generic_attractions = (
        "happy hour",
        "princess concert",
        "summer school",
        "festival",
        "symphony",
        "orchestra",
        "series",
        "experience",
        "tribute",
        "showcase",
        "show",
        "concert",
    )

    for event in events:

        title = event.get("name", "").strip()

        if not title:
            continue

        lower = title.lower()

        if any(word in lower for word in blocked):
            continue

        dates = event.get("dates", {})
        start = dates.get("start", {})
        embedded = event.get("_embedded", {})
        venues = embedded.get("venues", [])
        attractions = embedded.get("attractions", [])

        artist = ""
        artist_id = ""

        if attractions:

            title_lower = title.lower()
            best = None

            # 1. Music attraction whose name appears in title.
            for attraction in attractions:

                name = attraction.get("name", "").strip()

                if not name:
                    continue

                lower_name = name.lower()

                if any(word in lower_name for word in generic_attractions):
                    continue

                classes = attraction.get("classifications", [])

                segment = ""

                if classes:
                    segment = (
                        classes[0]
                        .get("segment", {})
                        .get("name", "")
                    )

                if (
                    segment == "Music"
                    and lower_name in title_lower
                ):
                    best = attraction
                    break

            # 2. Any music attraction that isn't generic.
            if best is None:

                for attraction in attractions:

                    name = attraction.get("name", "").strip()

                    if not name:
                        continue

                    lower_name = name.lower()

                    if any(word in lower_name for word in generic_attractions):
                        continue

                    classes = attraction.get("classifications", [])

                    segment = ""

                    if classes:
                        segment = (
                            classes[0]
                            .get("segment", {})
                            .get("name", "")
                        )

                    if segment == "Music":
                        best = attraction
                        break

            # 3. First non-generic attraction.
            if best is None:

                for attraction in attractions:

                    name = attraction.get("name", "").strip()

                    if not name:
                        continue

                    lower_name = name.lower()

                    if any(word in lower_name for word in generic_attractions):
                        continue

                    best = attraction
                    break

            # 4. Fallback.
            if best is None:
                best = attractions[0]

            artist = best.get("name", "")
            artist_id = best.get("id", "")

        venue = ""
        city = ""
        state = ""
        country = ""

        if venues:

            venue_info = venues[0]

            venue = venue_info.get("name", "")
            city = venue_info.get("city", {}).get("name", "")
            state = venue_info.get("state", {}).get("stateCode", "")
            country = venue_info.get("country", {}).get("countryCode", "")

        poster = ""

        images = event.get("images", [])

        if images:

            ranked = sorted(
                images,
                key=lambda img: (
                    "16_9" in img.get("url", ""),
                    img.get("width", 0),
                ),
                reverse=True,
            )

            poster = ranked[0].get("url", "")

        classification = ""

        classes = event.get("classifications", [])

        if classes:

            classification = (
                classes[0]
                .get("segment", {})
                .get("name", "")
            )

        event_date = format_date(
            start.get("localDate", "")
        )

        duplicate_key = (
            artist.strip().lower(),
            event_date,
            venue.strip().lower(),
            city.strip().lower(),
            state.strip().lower(),
        )

        if duplicate_key in seen:
            continue

        seen.add(duplicate_key)

        items.append(
            {
                "id": event.get("id", ""),
                "title": title,
                "artist": artist,
                "artist_id": artist_id,
                "event_date": event_date,
                "venue": venue,
                "city": city,
                "state": state,
                "country": country,
                "classification": classification,
                "poster": poster,
                "url": event.get("url", ""),
                "overview": venue,
            }
        )

        if len(items) >= limit:
            break

    return items
def get_concert_guide(limit=24):
    """
    Return the best upcoming concerts.
    """

    from .concert_api import (
        fetch_ticketmaster_events,
    )

    today = datetime.today()

    concerts = normalize_events(
        fetch_ticketmaster_events(
            today.strftime("%Y-%m-%d")
        ),
        limit=5000,
    )

    upcoming = []

    for concert in concerts:

        try:

            event_date = datetime.strptime(
                concert["event_date"],
                "%B %d, %Y",
            )

        except Exception:

            continue

        if event_date.date() < today.date():

            continue

        concert["_sort_date"] = event_date

        upcoming.append(
            concert
        )

    upcoming.sort(
        key=lambda c: c["_sort_date"]
    )

    featured = upcoming[:limit]

    for concert in featured:

        concert.pop(
            "_sort_date",
            None,
        )

    return featured