"""
===========================================
ShowBiz Streaming Data
Version 1.0
===========================================

Purpose:
    Provide streaming metadata for
    ShowBiz Streaming Guide.

Source:
    TMDb API

Author:
    ShowBiz Automation
"""

import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


load_dotenv()

TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def get_api_key():
    return os.getenv("TMDB_API_KEY")


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


def request_tmdb(endpoint, params=None):

    api_key = get_api_key()

    if not api_key:
        print("TMDB_API_KEY not found.")
        return {}

    if params is None:
        params = {}

    params.update(
        {
            "api_key": api_key,
            "language": "en-US",
            "region": "US",
        }
    )

    try:

        response = requests.get(
            f"{TMDB_API_URL}/{endpoint}",
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:

        print(
            "TMDb request failed:",
            exc,
        )

        return {}


def normalize_results(
    results,
    limit,
):

    items = []

    for item in results[:limit]:

        poster = item.get(
            "poster_path"
        )

        release_date = (
            item.get("release_date")
            or item.get("first_air_date")
            or ""
        )

        media_type = item.get(
            "media_type",
            "movie",
        )

        title = (
            item.get("title")
            or item.get("name")
            or ""
        )

        items.append(
            {
                "id": item.get("id"),
                "title": title,
                "media_type": media_type,
                "release_date": format_date(
                    release_date
                ),
                "overview": item.get(
                    "overview",
                    "",
                ),
                "rating": item.get(
                    "vote_average",
                    0,
                ),
                "popularity": item.get(
                    "popularity",
                    0,
                ),
                "poster": (
                    f"{TMDB_IMAGE_URL}{poster}"
                    if poster
                    else ""
                ),
            }
        )

    return items
def get_streaming_guide(limit=24):
    """
    Return a combined list of
    upcoming movies and TV
    suitable for the Streaming Guide.

    NOTE:
        This starts with TMDb's
        upcoming releases. We can
        later replace the queries
        with streaming-specific
        sources without changing
        the public interface.
    """

    combined = {}

    #
    # Upcoming Movies
    #
    movie_data = request_tmdb(
        "movie/upcoming",
        {
            "page": 1,
        },
    )

    today = datetime.today().date()

    for movie in normalize_results(
        movie_data.get("results", []),
        limit,
    ):

        if not movie["release_date"]:
            continue

        try:
            release = datetime.strptime(
                movie["release_date"],
                "%B %d, %Y",
            ).date()

        except Exception:
            continue

        if release <= today:
            continue

        movie["media_type"] = "movie"

        combined[
            (
                "movie",
                movie["id"],
            )
        ] = movie

    #
    # Upcoming TV
    #
    tv_data = request_tmdb(
        "discover/tv",
        {
            "sort_by": "first_air_date.asc",
            "first_air_date.gte": (
                datetime.today().strftime(
                    "%Y-%m-%d"
                )
            ),
            "first_air_date.lte": (
                datetime.today()
                + timedelta(days=90)
            ).strftime("%Y-%m-%d"),
            "watch_region": "US",
            "with_original_language": "en",
        },
    )

    for show in normalize_results(
        tv_data.get("results", []),
        limit,
    ):

        show["media_type"] = "tv"

        combined[
            (
                "tv",
                show["id"],
            )
        ] = show

    guide = sorted(
        combined.values(),
        key=lambda item: (
            datetime.strptime(
                item["release_date"],
                "%B %d, %Y",
            )
            if item["release_date"]
            else datetime.max,
            item["title"],
        ),
    )

    return guide[:limit]


if __name__ == "__main__":

    titles = get_streaming_guide()

    if not titles:

        print(
            "No streaming titles found."
        )

    for item in titles:

        print(
            item["media_type"],
            item["title"],
            item["release_date"],
        )