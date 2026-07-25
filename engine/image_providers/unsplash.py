"""
ShowBiz Unsplash Provider
Version 1.0

Searches Unsplash for editorial images and downloads the
highest-ranked result for the Image Engine.
"""

from __future__ import annotations

import os
import requests

from config import UNSPLASH_ACCESS_KEY

SEARCH_URL = "https://api.unsplash.com/search/photos"

DOWNLOAD_DIR = "images"


def search_unsplash(story):
    """
    Returns a list of Unsplash search results.
    """

    if not UNSPLASH_ACCESS_KEY:
        print("Unsplash API key not configured.")
        return []

    if isinstance(story, dict):
        query = story.get("headline", "")
    else:
        query = str(story)

    params = {
        "query": query,
        "per_page": 5,
        "orientation": "landscape",
    }

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    response = requests.get(
        SEARCH_URL,
        params=params,
        headers=headers,
        timeout=20,
    )

    response.raise_for_status()

    return response.json().get("results", [])


def download_unsplash_image(result):
    """
    Downloads one Unsplash image.
    Returns the local filename.
    """

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    url = result["urls"]["regular"]

    slug = (
        result.get("slug")
        or result.get("id")
        or "unsplash"
    )

    filename = os.path.join(
        DOWNLOAD_DIR,
        f"{slug}.jpg",
    )

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename


def get_unsplash_image(story):
    """
    Search and download the best Unsplash image.
    Returns local filename or None.
    """

    print("\n========================================")
    print(">>> UNSPLASH PROVIDER VERSION 1.0 <<<")
    print("========================================")

    try:

        print(f"Story type : {type(story).__name__}")

        if isinstance(story, dict):
            print(f"Headline   : {story.get('headline', '')}")

        print("\nCalling search_unsplash()...")

        results = search_unsplash(story)

        print(f"Unsplash returned {len(results)} result(s).")

        if not results:
            return None

        print("Downloading first Unsplash image...")

        filename = download_unsplash_image(results[0])

        print(f"Downloaded: {filename}")

        return filename

    except Exception as e:
        print(f"Unsplash error: {e}")
        return None