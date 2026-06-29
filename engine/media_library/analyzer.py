"""
ShowBiz Media Library Analyzer
Version 1.4

Loads the WordPress Media Library and prints the first media item.
"""

import json
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


def main():

    print("=" * 60)
    print("SHOWBIZ MEDIA LIBRARY ANALYZER")
    print("=" * 60)

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/media",
        params={
            "per_page": 1,
            "page": 1,
        },
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        timeout=30,
    )

    print("\nStatus:", response.status_code)

    response.raise_for_status()

    item = response.json()[0]

    print("\nFIRST MEDIA ITEM\n")
    print(json.dumps(item, indent=4))


if __name__ == "__main__":
    main()