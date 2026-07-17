"""
TMDb Provider / Trailer Debug
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE = "https://api.themoviedb.org/3"


def request(endpoint):

    response = requests.get(
        f"{BASE}/{endpoint}",
        params={
            "api_key": API_KEY,
            "language": "en-US",
            "region": "US",
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def debug_movie(movie_id):

    print("\n==============================")
    print("WATCH PROVIDERS")
    print("==============================")

    providers = request(
        f"movie/{movie_id}/watch/providers"
    )

    print(providers)

    print("\n==============================")
    print("VIDEOS")
    print("==============================")

    videos = request(
        f"movie/{movie_id}/videos"
    )

    print(videos)


if __name__ == "__main__":

    #
    # Avatar Aang: The Last Airbender
    #
    debug_movie(1234821)