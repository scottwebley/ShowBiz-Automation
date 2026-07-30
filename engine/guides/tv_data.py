"""
===========================================
ShowBiz TV Data
Version 1.1
===========================================

Purpose:
    Provide current TV metadata for
    ShowBiz TV guides.

Source:
    TMDb API

Features:
    - Trending TV
    - Airing Today
    - Currently On The Air
    - Structured TV data
    - TMDb IDs
    - Automatic .env loading
    - Safe fallback without API key

Author:
    ShowBiz Automation
"""

import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


# Load .env once.
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

def search_tv(query, limit=10):
    """
    Search TV shows by title.
    """

    data = request_tmdb(
        "search/tv",
        {
            "query": query,
        },
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )    

def normalize_results(
    results,
    limit,
    upcoming_only=False,
):

    shows = []
    today = datetime.today().date()

    for show in results[:limit]:

         air_date = show.get(
            "first_air_date",
            "",
        )
         
         if upcoming_only:

            if not air_date:
                continue

            try:

                air_date_obj = datetime.strptime(
                    air_date,
                    "%Y-%m-%d",
                ).date()

            except Exception:
                continue

            if air_date_obj <= today:
                continue

         poster = show.get("poster_path")

         shows.append(
            {
                "id": show.get("id"),
                "title": show.get("name", ""),
                "release_date": format_date(
                    show.get(
                        "first_air_date",
                        "",
                    )
                ),
                "overview": show.get(
                    "overview",
                    "",
                ),
                "rating": show.get(
                    "vote_average",
                    0,
                ),
                "popularity": show.get(
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

    return shows


def get_trending_tv(limit=10):

    data = request_tmdb(
        "trending/tv/week"
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def get_airing_today(limit=10):

    data = request_tmdb(
        "tv/airing_today"
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def get_on_the_air(limit=10):

    data = request_tmdb(
        "tv/on_the_air"
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def get_tv_guide(limit=24):

    combined = {}

    for collection in (
        normalize_results(
            request_tmdb(
                "discover/tv",
                {
                    "sort_by": "first_air_date.asc",
                    "first_air_date.gte": datetime.today().strftime("%Y-%m-%d"),
                    "first_air_date.lte": (
                        datetime.today() + timedelta(days=90)
                    ).strftime("%Y-%m-%d"),
                    "with_original_language": "en",
                    "watch_region": "US",
                },
            ).get("results", []),
            limit,
            upcoming_only=True,
        ),
    ):

        for show in collection:

            combined[show["id"]] = show

    guide = sorted(
        combined.values(),
        key=lambda x: (
            datetime.strptime(
                x["release_date"],
                "%B %d, %Y",
            ),
            -x["popularity"],
        ),
    )

    return guide[:limit]


if __name__ == "__main__":

    shows = get_tv_guide()

    if not shows:

        print("No TMDb TV shows found.")

    for show in shows:

        print(
            show["id"],
            show["title"],
            show["release_date"],
        )