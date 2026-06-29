"""
===========================================
ShowBiz Media Cache Builder
Version 1.0
===========================================

Downloads the complete WordPress Media Library
and saves it locally as media_cache.json.
"""

import json
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

CACHE_FILE = (
    Path(__file__).parent / "media_cache.json"
)


def load_media():

    page = 1
    media = []

    while True:

        print(f"Downloading page {page}...")

        response = requests.get(
            f"{WP_URL}/wp-json/wp/v2/media",
            params={
                "per_page": 100,
                "page": page,
            },
            auth=HTTPBasicAuth(
                WP_USERNAME,
                WP_APP_PASSWORD,
            ),
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code == 400:
            break

        response.raise_for_status()

        items = response.json()

        if not items:
            break

        media.extend(items)

        page += 1

    return media
def main():

    print("=" * 60)
    print("SHOWBIZ MEDIA CACHE BUILDER")
    print("=" * 60)

    print("\nConnecting to WordPress...\n")

    media = load_media()

    print(f"\nDownloaded {len(media)} media items.")

    print("\nSaving cache...")

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            media,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nCache saved to:\n{CACHE_FILE}")

    print("\nDone.")


if __name__ == "__main__":
    main()