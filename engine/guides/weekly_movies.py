"""
===========================================
ShowBiz Weekly Movies Guide
Version 1.3 DEBUG v2
===========================================

Generate and publish the
"What Movies To See Right Now" guide.

Debug version:
    - Saves AI output before enrichment.
    - Saves enriched output before publishing.

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import write_guide
from engine.guides.guide_enricher import enrich_guide
from engine.guides.movie_prompt import (
    TITLE,
    PROMPT,
)
from engine.guides.movie_data import (
    get_now_playing,
    get_upcoming_movies,
)
from engine.publisher import publish_html


PAGE_ID = 23240


def get_movies():

    movies = []

    movies.extend(
        get_now_playing(
            limit=10
        )
    )

    movies.extend(
        get_upcoming_movies(
            limit=10
        )
    )

    return movies


def build_movie_context(movies):

    if not movies:
        return ""

    context = """

CURRENT MOVIE DATA:

Use the following movies as
the source for this guide.

"""

    for movie in movies:

        context += f"""
Title: {movie.get("title")}
Release Date: {movie.get("release_date")}
Rating: {movie.get("rating")}
Popularity: {movie.get("popularity")}
Overview: {movie.get("overview")}
Poster: {movie.get("poster")}

"""

    return context


def build_guide():

    movies = get_movies()

    movie_context = build_movie_context(
        movies
    )

    prompt = (
        PROMPT
        + movie_context
    )

    html = write_guide(
        title=TITLE,
        prompt=prompt,
    )

    with open(
        "movie_ai_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            html
        )

    enriched_html = enrich_guide(
        title=TITLE,
        html=html,
        movies=movies,
    )

    with open(
        "movie_enriched_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            enriched_html
        )

    return enriched_html


def publish_guide():

    html = build_guide()

    return publish_html(
        page_id=PAGE_ID,
        html=html,
    )


def main():

    print()
    print("========================================")
    print("UPDATING MOVIES GUIDE (DEBUG v2)")
    print("========================================")

    success = publish_guide()

    print()

    if success:

        print(
            "✓ Movies Guide updated."
        )

        print(
            "✓ Saved movie_ai_output.html"
        )

        print(
            "✓ Saved movie_enriched_output.html"
        )

    else:

        print(
            "✗ Movies Guide failed."
        )


if __name__ == "__main__":

    main()