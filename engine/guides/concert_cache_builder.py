"""
Build a local cache of upcoming concert tours.

This runs before the Concert Guide so the guide
can reuse tour information without making dozens
of Ticketmaster API requests.
"""

import json
from datetime import datetime
from pathlib import Path

from engine.guides.concert_api import (
    fetch_ticketmaster_events,
)
from engine.guides.concert_data import (
    normalize_events,
)
from engine.guides.concert_tour_data import (
    apply_tour_data,
)


CACHE_FILE = Path("data/concert_cache.json")


def build_cache():

    print("Downloading Ticketmaster events...")

    today = datetime.today().strftime(
        "%Y-%m-%d"
    )

    #
    # Get the concerts that could appear
    # in the guide.
    #

    concerts = normalize_events(

        fetch_ticketmaster_events(
            start_date=today,
        ),

        limit=24,

    )

    print(
        f"Featured concerts: {len(concerts)}"
    )

    from engine.guides.concert_api import (
        fetch_artist_events,
    )

    cached = []

    processed = set()

    for concert in concerts:

        artist_id = concert.get(
            "artist_id",
            ""
        )

        if (
            not artist_id
            or artist_id in processed
        ):

            continue

        processed.add(
            artist_id
        )

        print(
            f"Fetching {concert['artist']}..."
        )

        artist_events = fetch_artist_events(
            artist_id,
            concert.get(
                "artist",
                ""
            ),
      )

        if not artist_events:

            continue

        tour = normalize_events(
            artist_events,
            limit=10000,
        )

        tour = apply_tour_data(
            tour
        )

        cached.extend(
            tour
        )

    CACHE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            cached,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(
        f"Cached {len(cached)} concerts."
    )

def main():

    print()
    print("========================================")
    print("BUILDING CONCERT CACHE")
    print("========================================")

    build_cache()

    print()
    print("✓ Concert cache updated.")


if __name__ == "__main__":

    main()