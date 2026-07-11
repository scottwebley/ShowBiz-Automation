"""
===========================================
ShowBiz Poster Debug
Version 1.1
===========================================

Purpose:
    Verify TMDb connectivity and
    inspect the movie data returned
    by movie_data.py.

Author:
    ShowBiz Automation
"""

import os

from engine.guides.movie_data import (
    get_api_key,
    get_now_playing,
)


def main():

    print()
    print("========================================")
    print("POSTER DEBUG")
    print("========================================")

    print()
    print("Environment Variable:")
    print(repr(os.getenv("TMDB_API_KEY")))

    print()
    print("get_api_key():")
    print(repr(get_api_key()))

    movies = get_now_playing(limit=10)

    print()
    print("Movies Returned:")
    print(len(movies))

    if not movies:

        print()
        print("No movies returned.")
        return

    for movie in movies:

        print()
        print("----------------------------------------")

        print("TITLE:")
        print(movie.get("title", ""))

        print()
        print("TMDB POSTER:")
        print(movie.get("poster", ""))

        print()
        print("MOVIE ID:")
        print(movie.get("id"))

        print("----------------------------------------")


if __name__ == "__main__":
    main()