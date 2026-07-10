"""
===========================================
ShowBiz Trailer Finder
Version 1.0
===========================================

Purpose:
    Build an official YouTube search URL
    for a movie trailer.

This module does NOT:

    • Scrape YouTube
    • Use the YouTube API
    • Verify videos

It simply creates a reliable search URL.

Author:
    ShowBiz Automation
"""

from urllib.parse import quote_plus


def find_trailer(title: str) -> dict:
    """
    Build a YouTube search URL for the
    movie's official trailer.

    Args:
        title (str): Movie title.

    Returns:
        dict
    """

    query = f"{title} official trailer"

    return {
        "title": "Official Trailer",
        "url": (
            "https://www.youtube.com/results"
            f"?search_query={quote_plus(query)}"
        ),
    }


if __name__ == "__main__":

    trailer = find_trailer("Superman")

    print(trailer["title"])
    print(trailer["url"])