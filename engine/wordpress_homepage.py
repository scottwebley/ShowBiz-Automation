"""
===========================================
ShowBiz WordPress Homepage
Version 2.0
===========================================

Purpose:
    Build the homepage from published
    WordPress posts instead of daily_news.json.

This module does NOT modify WordPress.

It only retrieves:

    • Current Top Story
    • Latest published posts

so the homepage builder has a single
source of truth.
"""

import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

TOP_STORY_CATEGORY = 64


def _get(endpoint, **params):

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/{endpoint}",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_current_top_story():
    """
    Returns the current published Top Story
    or None.
    """

    posts = _get(
        "posts",
        categories=TOP_STORY_CATEGORY,
        per_page=1,
        orderby="date",
        order="desc",
    )

    if not posts:
        return None

    return posts[0]


def get_latest_posts(limit=10):
    """
    Returns the latest published posts.
    """

    return _get(
        "posts",
        per_page=limit,
        orderby="date",
        order="desc",
    )


def build_homepage_feed(limit=10):
    """
    Returns:

        {
            "top_story": ...,
            "latest_news": [...]
        }
    """

    top_story = get_current_top_story()

    latest = get_latest_posts(limit + 5)

    latest_news = []

    top_id = None

    if top_story:
        top_id = top_story["id"]

    for post in latest:

        if post["id"] == top_id:
            continue

        latest_news.append(post)

        if len(latest_news) >= limit:
            break

    return {
        "top_story": top_story,
        "latest_news": latest_news,
    }


if __name__ == "__main__":

    homepage = build_homepage_feed()

    print()

    if homepage["top_story"]:
        print("Top Story:")
        print(homepage["top_story"]["title"]["rendered"])
    else:
        print("No Top Story found.")

    print()

    print("Latest:")

    for post in homepage["latest_news"]:

        print("-", post["title"]["rendered"])