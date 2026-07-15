"""
===========================================
ShowBiz Trailer Finder
Version 3.0
===========================================

Purpose:
    Build direct movie trailer links
    for ShowBiz Guides.

Features:
    - TMDb video lookup
    - Direct YouTube trailer URLs
    - Official trailer preference
    - Safe fallback

Author:
    ShowBiz Automation
"""

import os
import requests


TMDB_API_URL = "https://api.themoviedb.org/3"


def get_api_key():
    """
    Return TMDb API key.
    """

    return os.getenv(
        "TMDB_API_KEY"
    )


def request_videos(movie_id):
    """
    Get TMDb movie videos.
    """

    api_key = get_api_key()

    if not api_key or not movie_id:
        return []

    try:

        response = requests.get(
            f"{TMDB_API_URL}/movie/{movie_id}/videos",
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
            []
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
                video.get("site")
                == "YouTube"
                and video.get("type")
                == "Trailer"
                and name.lower()
                in video.get(
                    "name",
                    "",
                ).lower()
            ):

                return video


    for video in videos:

        if (
            video.get("site")
            == "YouTube"
        ):

            return video


    return None


def find_trailer(
    movie_id=None,
    title="",
):
    """
    Return trailer information.

    Supports:

        find_trailer(
            movie_id,
            title
        )

    """

    videos = request_videos(
        movie_id
    )

    trailer = select_trailer(
        videos
    )


    if trailer:

        return {

            "title": title,

            "label":
                "▶ Watch Official Trailer",

            "url":
                f"https://www.youtube.com/watch?v={trailer.get('key')}",

        }


    return {

        "title": title,

        "label":
            "▶ Watch Official Trailer",

        "url":
            "",

    }


def trailer_button(
    movie_id=None,
    title="",
):
    """
    Return HTML trailer button.
    """

    trailer = find_trailer(
        movie_id,
        title,
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
        trailer_button(
            1081003,
            "Supergirl",
        )
    )