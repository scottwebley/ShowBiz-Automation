"""
ShowBiz Unsplash Provider
"""

import os
import tempfile

import requests

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from config import UNSPLASH_ACCESS_KEY


def build_query(story):
    """
    Build an Unsplash search query from the story.

    Rather than searching the entire headline, extract the
    most important subject for better image matches.
    """

    if isinstance(story, dict):
        headline = (
            story.get("headline")
            or story.get("title")
            or story.get("query")
            or ""
        )
    else:
        headline = str(story)

    if not headline:
        return ""

    query = headline

    # Remove common entertainment/news phrases.
    replacements = [
        "Why ",
        "How ",
        "What ",
        "When ",
        "Where ",
        "Who ",
        "Box Office",
        "at the Box Office",
        "Review",
        "Reviews",
        "Trailer",
        "Official Trailer",
        "First Look",
        "Opening Weekend",
        "Premiere",
        "Premieres",
        "Debuts",
        "Debut",
        "Announced",
        "Announces",
        "Revealed",
        "Reveals",
        "Confirmed",
        "Explained",
        "Explains",
        "Interview",
    ]

    for text in replacements:
        query = query.replace(text, "")

    query = query.replace(":", " ")
    query = query.replace("-", " ")

    words = query.split()

    # Keep only the first few words.
    query = " ".join(words[:3]).strip()

    print(f"Unsplash query: {query}")

    return query


def search_unsplash(story, per_page=5):
    """
    Search Unsplash for matching photos.
    """

    if not UNSPLASH_ACCESS_KEY:
        print("Unsplash API key not configured.")
        return []

    query = build_query(story)

    if not query:
        return []

    response = requests.get(
        "https://api.unsplash.com/search/photos",
        headers={
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        },
        params={
            "query": query,
            "orientation": "landscape",
            "per_page": per_page,
        },
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def download_unsplash_image(photo):
    """
    Download an Unsplash image to a temporary file.
    """

    image_url = photo["urls"]["regular"]

    response = requests.get(image_url, timeout=30)
    response.raise_for_status()

    filename = os.path.join(
        tempfile.gettempdir(),
        f"unsplash_{photo['id']}.jpg",
    )

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename


def get_unsplash_image(story):
    """
    Search and download the best Unsplash image.
    Returns the local filename or None.
    """

    try:
        results = search_unsplash(story)

        if not results:
            return None

        return download_unsplash_image(results[0])

    except Exception as e:
        print(f"Unsplash error: {e}")
        return None


if __name__ == "__main__":
    test_story = {
        "headline": "Taylor Swift announces world tour"
    }

    image = get_unsplash_image(test_story)

    if image:
        print("Downloaded:", image)
    else:
        print("No image found.")