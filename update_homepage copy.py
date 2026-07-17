import sys

import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

# ---------------------------------------------------------
# ShowBiz Homepage
#
# This is the LIVE homepage configured under:
# WordPress → Settings → Reading
# ---------------------------------------------------------

PAGE_ID = 2146

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}


def main():

    with open("content/homepage.html", "r", encoding="utf-8") as f:
        content = f.read()

    # -----------------------------------------------------
    # Safety Check
    # Refuse to upload anything that does not appear to be
    # a Gutenberg homepage.
    # -----------------------------------------------------

    if "<!-- wp:" not in content:
        print("ERROR")
        print()
        print("This does not appear to be a Gutenberg homepage.")
        print("Upload cancelled.")
        sys.exit(1)

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        headers=HEADERS,
        json={
            "content": content
        },
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS")
        print(f"Homepage (Page {PAGE_ID}) updated.")
    else:
        print("FAILED")
        print(response.text)


if __name__ == "__main__":
    main()