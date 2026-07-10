"""
===========================================
ShowBiz Guide Publisher
Version 1.0
===========================================

Purpose:
    Publish an existing ShowBiz Guide
    to an existing WordPress page.

This module does NOT:

    • Generate AI content
    • Select images
    • Build HTML

It simply updates an existing page.

Public Functions:

    publish_page()

Author:
    ShowBiz Automation
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


def publish_page(page_id: int, title: str, html: str) -> bool:
    """
    Publish HTML to an existing WordPress page.

    Returns True on success.
    """

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{page_id}",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        json={
            "title": title,
            "content": html,
        },
        timeout=60,
    )

    print()
    print(f"Publishing Page {page_id}")
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS")
        return True

    print("FAILED")
    print(response.text)

    return False


if __name__ == "__main__":

    print("ShowBiz Guide Publisher")
    print("Import this module from a guide script.")