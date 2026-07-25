"""
===========================================
ShowBiz TMDb Image Provider
Version 1.2
===========================================

Purpose:
    Retrieve official TMDb poster artwork,
    download it locally, and return the
    local filename for WordPress upload.
"""

from pathlib import Path

import requests

from engine.guides.movie_data import search_movies


SKIP_CATEGORIES = {
    "Music",
    "Gaming",
    "Style",
    "Fashion",
    "Theater",
    "Theatre",
    "Entertainment Industry",
}

IMAGE_DIR = Path("images")


def _safe_filename(title):
    filename = "".join(
        c.lower() if c.isalnum() else "-"
        for c in title
    )

    while "--" in filename:
        filename = filename.replace("--", "-")

    return filename.strip("-") + ".jpg"


def _download_image(url, title):
    """
    Download poster into the images folder.
    """

    IMAGE_DIR.mkdir(exist_ok=True)

    filename = IMAGE_DIR / _safe_filename(title)

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✓ TMDb poster saved: {filename}")

        return str(filename)

    except Exception as exc:
        print(f"TMDb download failed: {exc}")
        return None


def get_movie_poster(story):
    """
    Return a local TMDb poster image.

    Args:
        story (dict | str)

    Returns:
        str | None
    """

    if isinstance(story, str):
        title = story
        category = ""
    else:
        title = story.get("headline", "")
        category = story.get("category", "")

    if category in SKIP_CATEGORIES:
        print(f"Skipping TMDb ({category} story).")
        return None

    if not title:
        return None

    try:
        movies = search_movies(title, limit=1)

        if not movies:
            return None

        poster = movies[0].get("poster")

        if not poster:
            return None

        print(f"✓ TMDb poster found: {movies[0]['title']}")

        return _download_image(
            poster,
            movies[0]["title"],
        )

    except Exception as exc:
        print(f"TMDb provider error: {exc}")

    return None


if __name__ == "__main__":

    tests = [
        {
            "headline": "Superman",
            "category": "Movies",
        },
        {
            "headline": "Blade Runner 2099",
            "category": "Television",
        },
        {
            "headline": "Toy Story 5",
            "category": "Movies",
        },
        {
            "headline": "Chris Brown",
            "category": "Music",
        },
    ]

    for story in tests:

        print("\n--------------------------------")
        print(story["headline"])

        image = get_movie_poster(story)

        print(image)