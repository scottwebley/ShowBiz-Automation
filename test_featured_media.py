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

MEDIA_ID = 41044


def main():

    auth = HTTPBasicAuth(
        WP_USERNAME,
        WP_APP_PASSWORD,
    )

    print("=" * 60)
    print("TESTING FEATURED MEDIA")
    print("=" * 60)

    #
    # Fetch media
    #

    print(f"\nFetching media {MEDIA_ID}...")

    r = requests.get(
        f"{WP_URL}/wp-json/wp/v2/media/{MEDIA_ID}",
        auth=auth,
        headers=HEADERS,
        timeout=30,
    )

    print("Status:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return

    media = r.json()

    print("\nMEDIA")
    print("-" * 60)
    print("ID        :", media.get("id"))
    print("Status    :", media.get("status"))
    print("Type      :", media.get("media_type"))
    print("Mime      :", media.get("mime_type"))
    print("Parent    :", media.get("post"))
    print("Source URL:", media.get("source_url"))

    #
    # Create post
    #

    print("\nCreating test post...")

    payload = {
        "title": "Featured Media API Test",
        "status": "draft",
        "content": "<p>Testing featured media.</p>",
        "featured_media": MEDIA_ID,
    }

    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=auth,
        headers=HEADERS,
        json=payload,
        timeout=30,
    )

    print("Create Status:", r.status_code)

    if r.status_code not in (200, 201):
        print(r.text)
        return

    post = r.json()

    post_id = post["id"]

    print("\nPOST CREATED")
    print("-" * 60)
    print("Post ID               :", post_id)
    print("Sent featured_media   :", MEDIA_ID)
    print("Returned featured_media:",
          post.get("featured_media"))

    #
    # Read it back
    #

    r = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        auth=auth,
        headers=HEADERS,
        timeout=30,
    )

    print("\nRead Status:", r.status_code)

    if r.status_code == 200:

        post = r.json()

        print("\nREAD BACK")
        print("-" * 60)
        print("featured_media:",
              post.get("featured_media"))

    #
    # Delete draft
    #

    print("\nDeleting test post...")

    r = requests.delete(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        params={"force": True},
        auth=auth,
        headers=HEADERS,
        timeout=30,
    )

    print("Delete Status:", r.status_code)

    print("\nDone.")


if __name__ == "__main__":
    main()