#!/usr/bin/env python3

"""
update_featured_entertainer_homepage.py

Reads data/featured_entertainer.json and updates the
ShowBiz Featured Entertainer homepage component through
the ShowBiz Newsroom REST API.

This script is completely standalone and does not publish
posts or modify any other part of the system.
"""

import json
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)


FEATURED_JSON = Path("data/featured_entertainer.json")

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0",
    "Content-Type": "application/json",
}


def load_featured():
    if not FEATURED_JSON.exists():
        raise FileNotFoundError(
            f"{FEATURED_JSON} not found."
        )

    with open(
        FEATURED_JSON,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def update_homepage(featured):

    payload = {
        "name": featured.get("name", ""),
        "profession": featured.get("profession", ""),
        "headline": featured.get("headline", ""),
        "url": featured.get("url", ""),
    }

    print("\n========================================")
    print("UPDATING FEATURED ENTERTAINER")
    print("========================================")
    print("Name      :", payload["name"])
    print("Headline  :", payload["headline"])
    print("URL       :", payload["url"])
    print("========================================")

    response = requests.post(
        f"{WP_URL}/wp-json/showbiz/v1/featured-entertainer",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        json=payload,
        timeout=60,
    )

    print("\nStatus:", response.status_code)

    if response.status_code not in (200, 201):
        print("\nFAILED")
        print(response.text)
        return False

    print("\n✅ Homepage Featured Entertainer updated.")

    try:
        print(response.json())
    except Exception:
        pass

    return True


def main():

    print("\n==============================")
    print(" FEATURED ENTERTAINER UPDATE")
    print("==============================")

    featured = load_featured()

    update_homepage(featured)

    print("\nDone.\n")


if __name__ == "__main__":
    main()