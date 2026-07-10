"""
===========================================
ShowBiz Poster Finder
Version 1.0
===========================================

Purpose:
    Find the best poster for a movie
    using the existing ShowBiz Media
    Library search engine.

This module does NOT:

    • Search the web
    • Generate AI images
    • Upload media

It simply wraps the existing
Media Library search.

Author:
    ShowBiz Automation
"""

from engine.media_library.search import find_best_image


def find_poster(title: str):
    """
    Find the best poster for a movie.

    Args:
        title (str)

    Returns:
        MediaResult | None
    """

    if not title:
        return None

    return find_best_image(title)


def poster_html(title: str) -> str:
    """
    Build HTML for a movie poster.

    Args:
        title (str)

    Returns:
        str
    """

    poster = find_poster(title)

    if poster is None:
        return ""

    return (
        f'<img '
        f'src="{poster.url}" '
        f'alt="{title}" '
        f'class="showbiz-movie-poster">'
    )


if __name__ == "__main__":

    movie = "Superman"

    poster = find_poster(movie)

    if poster:

        print(movie)
        print(poster.url)

    else:

        print("No poster found.")