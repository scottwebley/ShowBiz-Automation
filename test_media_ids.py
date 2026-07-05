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

TEST_IDS = [
    1670,
    30112,
    30113,
    30114,
    30115,
    30116,
    30190,
    30213,
    30296,
]


def check(media_id):
    url = f"{WP_URL}/wp-json/wp/v2/media/{media_id}"

    r = requests.get(
        url,
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        timeout=30,
    )

    print("=" * 60)
    print(f"Media ID: {media_id}")
    print(f"HTTP: {r.status_code}")

    if r.status_code == 200:
        data = r.json()

        print("Title :", data.get("title", {}).get("rendered"))
        print("Type  :", data.get("media_type"))
        print("URL   :", data.get("source_url"))

    else:
        print(r.text[:500])


def main():

    print("=" * 60)
    print("WORDPRESS MEDIA TEST")
    print("=" * 60)

    for media_id in TEST_IDS:
        check(media_id)


if __name__ == "__main__":
    main()