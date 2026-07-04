
"""
ShowBiz Top Story Inspector
Read-only diagnostic utility.
"""

import requests
from requests.auth import HTTPBasicAuth

from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

TOP_STORY_CATEGORY = 64

HEADERS = {"User-Agent": "ShowBiz-Automation/1.0"}


def wp_get(endpoint):
    r = requests.get(
        f"{WP_URL}{endpoint}",
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def category_name(cat_id):
    try:
        return wp_get(f"/wp-json/wp/v2/categories/{cat_id}")["name"]
    except Exception:
        return "(unknown)"


def media_info(media_id):
    if not media_id:
        return None
    try:
        m = wp_get(f"/wp-json/wp/v2/media/{media_id}")
        return {
            "title": m["title"]["rendered"],
            "url": m.get("source_url", ""),
        }
    except Exception:
        return None


def main():
    print("=" * 60)
    print("SHOWBIZ TOP STORY INSPECTOR")
    print("=" * 60)

    posts = wp_get(
        f"/wp-json/wp/v2/posts?categories={TOP_STORY_CATEGORY}"
        "&orderby=date&order=desc&per_page=20"
    )

    print(f"\nTop Story posts found: {len(posts)}\n")

    if not posts:
        return

    if len(posts) > 1:
        print("WARNING: More than one Top Story exists.\n")

    for i, post in enumerate(posts, start=1):
        print("=" * 60)
        print(f"TOP STORY #{i}")
        print("=" * 60)
        print("ID       :", post["id"])
        print("Title    :", post["title"]["rendered"])
        print("Status   :", post["status"])
        print("Date     :", post["date"])
        print("Sticky   :", post["sticky"])
        print("Permalink:", post["link"])
        print("\nCategories")
        for cid in post["categories"]:
            print(f"  {cid:>3}  {category_name(cid)}")

        media_id = post.get("featured_media", 0)
        print("\nFeatured Media:", media_id)
        if media_id:
            info = media_info(media_id)
            if info:
                print("  Title:", info["title"])
                print("  URL  :", info["url"])
            else:
                print("  Unable to retrieve media details.")
        else:
            print("  No featured image assigned.")
        print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Top Story posts: {len(posts)}")


if __name__ == "__main__":
    main()
