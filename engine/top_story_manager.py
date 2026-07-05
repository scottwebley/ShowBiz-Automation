"""
===========================================
ShowBiz Top Story Manager
Version 2.3
===========================================

Purpose:
    Decide whether today's highest-ranked
    story should replace the current
    ShowBiz Top Story.

New in Version 2.3

- Decodes HTML entities.
- Normalizes smart punctuation before
  comparing titles.
- Prevents duplicate Top Story
  publications caused by punctuation
  differences.
"""

from html import unescape

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


def _auth():
    return HTTPBasicAuth(
        WP_USERNAME,
        WP_APP_PASSWORD,
    )


def _normalize_title(title):
    """
    Normalize titles before comparison.
    """

    return (
        unescape(title)
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .strip()
        .lower()
    )


def get_top_story_posts():
    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={
            "categories": TOP_STORY_CATEGORY,
            "per_page": 100,
            "orderby": "date",
            "order": "desc",
            "status": "publish",
        },
        auth=_auth(),
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_current_top_story():

    posts = get_top_story_posts()

    if not posts:
        return None

    return posts[0]


def should_replace_top_story(candidate_story):

    current = get_current_top_story()

    if current is None:

        print("\nNo current Top Story.")
        return True

    current_title = _normalize_title(
        current["title"]["rendered"]
    )

    candidate_title = _normalize_title(
        candidate_story["headline"]
    )

    print("\nCurrent Top Story:")
    print(unescape(current["title"]["rendered"]))

    print("\nCandidate:")
    print(candidate_story["headline"])

    if current_title == candidate_title:

        print("\nDecision: KEEP")
        return False

    print("\nDecision: REPLACE")
    return True


def retire_previous_top_stories(keep_post_id):
    """
    Remove the Top Story category from every
    Top Story except the newly published one.
    """

    posts = get_top_story_posts()

    if not posts:
        return

    print(f"\nChecking {len(posts)} Top Story post(s)...")

    for post in posts:

        if post["id"] == keep_post_id:
            print(
                f"✓ Keeping Top Story: "
                f"{post['title']['rendered']}"
            )
            continue

        categories = post.get("categories", [])

        new_categories = [
            c for c in categories
            if c != TOP_STORY_CATEGORY
        ]

        if new_categories == categories:
            continue

        response = requests.post(
            f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
            auth=_auth(),
            headers=HEADERS,
            json={
                "categories": new_categories
            },
            timeout=30,
        )

        response.raise_for_status()

        print(
            f"✓ Retired Top Story: "
            f"{post['title']['rendered']}"
        )

    print("\nTop Story cleanup complete.")


if __name__ == "__main__":

    posts = get_top_story_posts()

    print(f"\nCurrent Top Story posts: {len(posts)}")

    for post in posts:
        print("-", unescape(post["title"]["rendered"]))