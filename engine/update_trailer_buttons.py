import os
import sys
import re

import requests
from requests.auth import HTTPBasicAuth

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

PATTERN = re.compile(
    r"\b(trailer|teaser|first look)\b",
    re.IGNORECASE,
)


def main():
    auth = HTTPBasicAuth(
        WP_USERNAME,
        WP_APP_PASSWORD,
    )

    page = 1
    matches = []

    while True:
        response = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts",
            auth=auth,
            headers=HEADERS,
            params={
                "per_page": 100,
                "page": page,
                "status": "publish",
            },
            timeout=60,
        )

        if response.status_code == 400:
            try:
                error = response.json()
            except Exception:
                error = {}

            if error.get("code") == "rest_post_invalid_page_number":
                break

        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            return

        posts = response.json()

        if not posts:
            break

        for post in posts:
            title = post["title"]["rendered"]

            if PATTERN.search(title):
                matches.append(post)

        page += 1

    print()
    print("=" * 60)
    print("TRAILER ARTICLES")
    print("=" * 60)

    if not matches:
        print("None found.")
        return

    for post in matches:
        print(f"{post['id']:>6}  {post['title']['rendered']}")

    print()
    print(f"Found {len(matches)} trailer article(s).")


if __name__ == "__main__":
    main()