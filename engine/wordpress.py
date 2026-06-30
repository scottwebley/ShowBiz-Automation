import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

from engine.media import upload_image


HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}


def publish_post(article):
    """
    Publish a ShowBiz article to WordPress.

    Supports two image formats:

        media:<id>
            Uses an existing WordPress Media Library item.

        images/example.png
            Uploads a new image and uses it as the featured image.
    """

    featured_media = None

    # -----------------------------------------
    # Featured Image
    # -----------------------------------------

    image = article.get("image")

    if image:

        # Existing WordPress Media Library image

        if isinstance(image, str) and image.startswith("media:"):

            featured_media = int(image.split(":")[1])

            print(
                f"\nUsing existing Media Library image "
                f"(ID {featured_media})"
            )

        # Upload newly generated image

        else:

            print("\nUploading featured image...")

            featured_media = upload_image(image)

    # -----------------------------------------
    # Build WordPress post
    # -----------------------------------------

    data = {
        "title": article["title"],
        "content": article["content"],
        "excerpt": article["excerpt"],
        "status": "publish",
    }

    if article.get("category_id"):
        data["categories"] = [article["category_id"]]

    if featured_media:
        data["featured_media"] = featured_media

    # -----------------------------------------
    # Publish
    # -----------------------------------------

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD
        ),
        headers=HEADERS,
        json=data,
        timeout=60
    )

    print("\nPublish Status:", response.status_code)

    if response.status_code not in (200, 201):

        print(response.text)

        return None

    post = response.json()

    print("\n✅ ARTICLE PUBLISHED")
    print("----------------------------")
    print("Post ID :", post["id"])
    print("Title   :", post["title"]["rendered"])
    print("Status  :", post["status"])
    print("URL     :", post["link"])

    if featured_media:
        print("Featured Image :", featured_media)

    return post


if __name__ == "__main__":

    print("wordpress.py is ready.")