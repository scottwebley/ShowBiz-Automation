import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD


HEADERS = {
    "User-Agent": "ShowBiz-Automation/3.0"
}


# WordPress page IDs
PAGES = {
    2129: "content/entertainment_news.html",
    2134: "content/movies.html",
    2136: "content/music_and_tours.html",
    2138: "content/television.html",
    2140: "content/style.html",
}


def publish_page(page_id, html_file):
    """Publish one HTML file to one WordPress page."""

    path = Path(html_file)

    if not path.exists():
        print(f"⚠ File not found: {html_file}")
        return

    html = path.read_text(encoding="utf-8")

    data = {
        "content": html
    }

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{page_id}",
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        headers=HEADERS,
        json=data
    )

    if response.status_code == 200:
        print(f"✓ Updated page {page_id}")

    else:
        print(f"✗ Failed page {page_id}")
        print(response.status_code)
        print(response.text)


def publish_all():
    print("\n==============================")
    print("Publishing ShowBiz Pages")
    print("==============================\n")

    for page_id, html_file in PAGES.items():
        publish_page(page_id, html_file)

    print("\n✓ Publishing Complete")