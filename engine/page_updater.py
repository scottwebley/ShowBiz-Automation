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


def update_page(page_id, article):
    """
    Update an existing WordPress page.
    """

    data = {
        "title": article["title"],
        "content": article["content"],
        "excerpt": article["excerpt"],
        "status": "publish"
    }

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{page_id}",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD
        ),
        headers=HEADERS,
        json=data,
        timeout=60
    )

    print("\nPage Update Status:", response.status_code)

    if response.status_code not in (200, 201):

        print(response.text)
        return None

    page = response.json()

    print("\n✅ PAGE UPDATED")
    print("----------------------------")
    print("Page ID :", page["id"])
    print("Title   :", page["title"]["rendered"])
    print("URL     :", page["link"])

    return page