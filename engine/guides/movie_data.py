"""
===========================================
ShowBiz Movie Data Provider
Version 3.2
===========================================

Purpose:
    Provide current movie metadata for
    ShowBiz movie guides.

Source:
    TMDb API

Features:
    - Current theatrical movies
    - Popular movies
    - Structured movie data
    - TMDb movie IDs for trailer lookup
    - Automatic .env loading
    - Safe fallback without API key

Author:
    ShowBiz Automation
"""

import os

import requests
from dotenv import load_dotenv


# Load .env once when this module is imported.
load_dotenv()


TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def get_api_key():
    """
    Return TMDb API key.
    """

    return os.getenv(
        "TMDB_API_KEY"
    )


def empty_result():
    """
    Return safe empty result.
    """

    return []


def request_tmdb(endpoint, params=None):
    """
    Make TMDb API request.
    """

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


def get_now_playing(limit=10):
    """
    Get movies currently in theaters.
    """

    data = request_tmdb(
        "movie/now_playing",
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def get_popular_movies(limit=10):
    """
    Get popular movies.
    """

    data = request_tmdb(
        "movie/popular",
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def search_movies(query, limit=10):
    """
    Search movies.
    """

    data = request_tmdb(
        "search/movie",
        {
            "query": query,
        },
    )

    return normalize_results(
        data.get("results", []),
        limit,
    )


def normalize_results(results, limit):
    """
    Convert TMDb data into ShowBiz format.
    """

    movies = []

    for movie in results[:limit]:

        poster = movie.get(
            "poster_path"
        )

        movies.append(
            {
                "id": movie.get(
                    "id"
                ),
                "title": movie.get(
                    "title",
                    "",
                ),
                "release_date": movie.get(
                    "release_date",
                    "",
                ),
                "overview": movie.get(
                    "overview",
                    "",
                ),
                "rating": movie.get(
                    "vote_average",
                    0,
                ),
                "popularity": movie.get(
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

    return movies


if __name__ == "__main__":

    movies = get_now_playing()

    if not movies:

        print(
            "No TMDb movies found."
        )

    for movie in movies:

        print(
            movie["id"],
            movie["title"],
            movie["release_date"],
        )