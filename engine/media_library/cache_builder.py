"""
===========================================================
ShowBiz Media Cache Builder
Version 2.0
===========================================================

Downloads the complete WordPress Media Library and enriches
each media item with parent post metadata.

Adds:
    parent_post_title
    parent_post_slug
    parent_post_excerpt

before saving media_cache.json.
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

CACHE_FILE = Path(__file__).parent / "media_cache.json"

POST_CACHE = {}


def get_post(post_id):
    """
    Download one WordPress post.

    Cached so multiple images attached to the same
    article only require one REST request.
    """

    if not post_id:
        return None

    if post_id in POST_CACHE:
        return POST_CACHE[post_id]

    try:

        response = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
            auth=HTTPBasicAuth(
                WP_USERNAME,
                WP_APP_PASSWORD,
            ),
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code != 200:
            print(f"[POST ERROR] {post_id} -> HTTP {response.status_code}")
            print(response.text[:500])
            POST_CACHE[post_id] = None
            return None

        post = response.json()

        parent = {
            "parent_post_title": (
                post.get("title", {}).get("rendered", "")
            ),
            "parent_post_slug": post.get(
                "slug",
                "",
            ),
            "parent_post_excerpt": (
                post.get("excerpt", {}).get("rendered", "")
            ),
        }

        POST_CACHE[post_id] = parent

        if parent["parent_post_title"]:
            print(
                f"[POST OK] {post_id}: "
                f"{parent['parent_post_title'][:80]}"
            )
        else:
            print(f"[POST EMPTY] {post_id}")

        return parent

    except Exception as e:

        print(f"[POST EXCEPTION] {post_id}: {e}")

        POST_CACHE[post_id] = None
        return None


def load_media():

    page = 1
    media = []

    while True:

        print(f"Downloading page {page}...")

        print("WP_URL:", WP_URL)
        print("WP_USERNAME:", WP_USERNAME)
        print("APP PASSWORD PRESENT:", bool(WP_APP_PASSWORD))

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

        for item in items:

            post_id = item.get("post")

            if post_id:

                parent = get_post(post_id)

                if parent:

                    item.update(parent)

            media.append(item)

        page += 1

    return media


def main():

    print("=" * 60)
    print("SHOWBIZ MEDIA CACHE BUILDER")
    print("=" * 60)

    print("\nConnecting to WordPress...\n")

    media = load_media()

    print(f"\nDownloaded {len(media)} media items.")
    print(f"Cached {len(POST_CACHE)} parent posts.")

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