"""
===========================================
ShowBiz Homepage Feed
Version 2.0
===========================================

Builds the editorial homepage feed from
published WordPress posts.

Source of truth:
    WordPress

Output:
    data/front_page.json
"""

import json
from datetime import datetime
from pathlib import Path

from engine.wordpress_homepage import build_homepage_feed

OUTPUT_FILE = Path("data/front_page.json")


def build_front_page_feed():
    """
    Build the homepage feed from WordPress.

    Returns
    -------
    dict
        Homepage feed dictionary.
    """

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    homepage = build_homepage_feed()

    feed = {
        "generated_at": datetime.utcnow().isoformat(),
        "top_story": homepage["top_story"],
        "latest_news": homepage["latest_news"],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=4, ensure_ascii=False)

    print(f"✓ Homepage feed written to {OUTPUT_FILE}")

    return feed


def main():
    feed = build_front_page_feed()

    print()

    if feed["top_story"]:
        print("Top Story:")
        print(feed["top_story"]["title"]["rendered"])

    print()

    print("Latest Stories:")

    for post in feed["latest_news"]:
        print("-", post["title"]["rendered"])


if __name__ == "__main__":
    main()