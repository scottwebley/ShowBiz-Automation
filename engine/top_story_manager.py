"""
===========================================
ShowBiz Top Story Manager
Version 1.0
===========================================

Purpose:
    Decide whether today's highest-ranked
    story should replace the current
    ShowBiz Top Story.

Version 1.0

Rules:

- If there is no current Top Story:
      REPLACE

- If today's #1 headline matches the
  current Top Story:
      KEEP

- Otherwise:
      REPLACE

Future versions can add:

- age weighting
- editorial score thresholds
- breaking-news bonus
- AI comparison
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


TOP_STORY_CATEGORY = 64   # <-- replace with your real category ID


def get_current_top_story():
    """
    Return the current Top Story post
    or None.
    """

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={
            "categories": TOP_STORY_CATEGORY,
            "per_page": 1,
            "orderby": "date",
            "order": "desc",
        },
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    posts = response.json()

    if not posts:
        return None

    return posts[0]


def should_replace_top_story(candidate_story):
    """
    Returns:

        True
            Publish new Top Story

        False
            Keep current Top Story
    """

    current = get_current_top_story()

    if current is None:

        print("\nNo current Top Story.")

        return True

    current_title = (
        current["title"]["rendered"]
        .strip()
        .lower()
    )

    candidate_title = (
        candidate_story["headline"]
        .strip()
        .lower()
    )

    print("\nCurrent Top Story:")
    print(current["title"]["rendered"])

    print("\nCandidate:")
    print(candidate_story["headline"])

    if current_title == candidate_title:

        print("\nDecision: KEEP")

        return False

    print("\nDecision: REPLACE")

    return True


if __name__ == "__main__":

    print("Top Story Manager ready.")