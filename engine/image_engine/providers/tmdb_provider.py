"""
===========================================
ShowBiz Media Engine
TMDb Provider
===========================================

Searches The Movie Database (TMDb)
for movies and TV shows.
"""

import requests

from engine.image_engine.config import (
    TMDB_API_KEY,
    TMDB_BASE_URL,
    TMDB_IMAGE_BASE,
)

from engine.image_engine.providers.base import (
    ImageProvider,
    ImageResult,
)


class TMDbProvider(ImageProvider):

    provider_name = "TMDb"

    def search(self, query):

        print(f"\nSearching TMDb for: {query}")

        url = f"{TMDB_BASE_URL}/search/movie"

        response = requests.get(

            url,

            params={

                "api_key": TMDB_API_KEY,

                "query": query

            },

            timeout=30

        )

        response.raise_for_status()

        data = response.json()

        results = []

        for movie in data.get("results", [])[:5]:

            backdrop = movie.get("backdrop_path")

            if not backdrop:
                continue

            results.append(

                ImageResult(

                    title=movie["title"],

                    image_url=f"{TMDB_IMAGE_BASE}{backdrop}",

                    page_url=f"https://www.themoviedb.org/movie/{movie['id']}",

                    width=1920,

                    height=1080,

                    source="TMDb",

                    license="TMDb"

                )

            )

        return results


def main():

    provider = TMDbProvider()

    images = provider.search("Toy Story")

    print()

    print("=" * 60)

    print("RESULTS")

    print("=" * 60)

    for image in images:

        print(image.title)
        print(image.image_url)
        print()


if __name__ == "__main__":
    main()