"""
===========================================
ShowBiz Trailer Finder
Version 4.0
===========================================

Purpose:
    Build direct trailer links
    for ShowBiz Guides and
    ShowBiz Top Stories.

Features:
    - TMDb title search
    - Movie + TV support
    - TMDb video lookup
    - Official trailer preference
    - Safe fallback

Author:
    ShowBiz Automation
"""

import os
import requests

try:
    from dotenv import load_dotenv

    load_dotenv()

except Exception:
    pass

TMDB_API_URL = "https://api.themoviedb.org/3"


def get_api_key():
    """
    Return TMDb API key.

    Supports both .env and exported
    environment variables.
    """

    api_key = os.getenv("TMDB_API_KEY")

    if api_key:
        return api_key.strip()

    env_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        ".env",
    )

    if os.path.exists(env_path):

        try:

            with open(env_path, "r") as f:

                for line in f:

                    if line.startswith("TMDB_API_KEY="):

                        return (
                            line.split("=", 1)[1]
                            .strip()
                            .strip('"')
                            .strip("'")
                        )

        except Exception:
            pass

    return None


# ---------------------------------------------------------
# NEW
# ---------------------------------------------------------

def _search_media(title, media_type):
    """
    Search TMDb.

    Returns:
        dict or None
    """

    api_key = get_api_key()

    if not api_key or not title:
        return None

    try:

        response = requests.get(
            f"{TMDB_API_URL}/search/{media_type}",
            params={
                "api_key": api_key,
                "query": title,
                "language": "en-US",
                "include_adult": "false",
            },
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        print(data)

        results = data.get("results", [])

        if not results:
            return None

        best = results[0]

        return {
            "id": best.get("id"),
            "title": (
                best.get("title")
                or best.get("name")
                or title
            ),
            "media_type": media_type,
            "release_date": (
                best.get("release_date")
                or best.get("first_air_date")
                or ""
            ),
            "popularity": best.get("popularity", 0),
        }

    except Exception as exc:

        print("TMDb search failed:", exc)

        return None


def search_movie(title):
    """
    Search TMDb movie.
    """

    return _search_media(
        title,
        "movie",
    )


def search_tv(title):
    """
    Search TMDb TV.
    """

    return _search_media(
        title,
        "tv",
    )


def find_media(title):
    """
    Find movie or TV.
    """

    movie = search_movie(title)

    if movie:
        return movie

    return search_tv(title)


# ---------------------------------------------------------
# EXISTING
# ---------------------------------------------------------

def request_videos(
    movie_id,
    media_type="movie",
):
    """
    Get TMDb videos.

    media_type:
        movie
        tv
    """

    api_key = get_api_key()

    if not api_key or not movie_id:
        return []

    media_type = (
        media_type or "movie"
    ).lower()

    if media_type not in (
        "movie",
        "tv",
    ):
        media_type = "movie"

    try:

        response = requests.get(
            f"{TMDB_API_URL}/{media_type}/{movie_id}/videos",
            params={
                "api_key": api_key,
                "language": "en-US",
            },
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "results",
            [],
        )

    except Exception as exc:

        print(
            "Trailer lookup failed:",
            exc,
        )

        return []
def select_trailer(videos):
    """
    Select the best trailer.
    """

    if not videos:
        return None

    priority = [
        "Official Trailer",
        "Trailer",
        "Teaser",
    ]

    for name in priority:

        for video in videos:

            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
                and name.lower()
                in video.get("name", "").lower()
            ):
                return video

    for video in videos:

        if video.get("site") == "YouTube":
            return video

    return None


def find_trailer(
    movie_id=None,
    title="",
    media_type="movie",
):
    """
    Return trailer information.

    If no TMDb ID is supplied,
    automatically search TMDb.
    """

    if not movie_id and title:

        media = find_media(title)

        if media:

            movie_id = media["id"]
            media_type = media["media_type"]
            title = media["title"]

    videos = request_videos(
        movie_id,
        media_type=media_type,
    )

    trailer = select_trailer(videos)

    if trailer:

        key = trailer.get("key", "")

        return {
            "title": title,
            "label": "▶ Watch Official Trailer",
            "url": f"https://www.youtube.com/watch?v={key}",
            "embed_url": f"https://www.youtube.com/embed/{key}",
            "tmdb_id": movie_id,
            "media_type": media_type,
        }

    return {
        "title": title,
        "label": "▶ Watch Official Trailer",
        "url": "",
        "embed_url": "",
        "tmdb_id": movie_id,
        "media_type": media_type,
    }


def trailer_button(
    movie_id=None,
    title="",
    media_type="movie",
):
    """
    Return HTML trailer button.
    """

    trailer = find_trailer(
        movie_id=movie_id,
        title=title,
        media_type=media_type,
    )

    if not trailer["url"]:
        return ""

    return (
        '<p>'
        '<a class="showbiz-trailer-button" '
        f'href="{trailer["url"]}" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        f'{trailer["label"]}'
        '</a>'
        '</p>'
    )


if __name__ == "__main__":

    print(
        find_trailer(
            title="Clayface",
        )
    )    