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


def get_current_top_story():
    """
    Returns the most recently published ShowBiz article.
    """

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD
        ),
        headers=HEADERS,
        params={
            "per_page": 1,
            "status": "publish",
            "orderby": "date",
            "order": "desc"
        },
        timeout=30
    )

    response.raise_for_status()

    posts = response.json()

    if not posts:
        return None

    return posts[0]


def should_publish(candidate_story):

    current = get_current_top_story()

    if current is None:
        print("No published stories found.")
        return True

    print("\nCURRENT TOP STORY")
    print("----------------------------")
    print(current["title"]["rendered"])

    print("\nNEW CANDIDATE")
    print("----------------------------")
    print(candidate_story["headline"])

    # Don't republish the same story
    if current["title"]["rendered"].strip().lower() == candidate_story["headline"].strip().lower():

        print("\nDecision: KEEP CURRENT STORY")
        print("Reason: Same headline already published.")

        return False

    print("\nDecision: PUBLISH NEW STORY")

    return True


if __name__ == "__main__":

    test_story = {
        "headline": "This is a test story"
    }

    should_publish(test_story)