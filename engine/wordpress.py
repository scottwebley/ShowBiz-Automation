import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

from engine.media import upload_image
from engine.link_enricher import enrich_links


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
    # Link Enrichment
    # -----------------------------------------

    article["content"] = enrich_links(
        article["content"]
    )

    # -----------------------------------------
    # Build WordPress post
    # -----------------------------------------

    data = {
        "title": article["title"],
        "content": article["content"],
        "excerpt": article["excerpt"],
        "status": "publish",
    }

    #
    # Categories
    #
    # Supports BOTH the new category_ids list and
    # the older single category_id.
    #

    if article.get("category_ids"):
        data["categories"] = article["category_ids"]

    elif article.get("category_id"):
        data["categories"] = [article["category_id"]]

    #
    # Featured image
    #

    if featured_media:
        data["featured_media"] = featured_media

    # -----------------------------------------
    # Publish
    # -----------------------------------------

    print("\n========================================")
    print("WORDPRESS PUBLISH PAYLOAD")
    print("========================================")
    print("Title           :", data.get("title"))
    print("Image field     :", article.get("image"))
    print("Featured Media  :", featured_media)
    print("Categories      :", data.get("categories"))
    print("========================================")

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
    
    print("\n========== WORDPRESS RESPONSE ==========")
    print("Post ID   :", post["id"])
    print("Categories:", post.get("categories"))
    print("========================================")

    print(
        "\nWordPress returned featured_media:",
        post.get("featured_media")
    )

    print("\n✅ ARTICLE PUBLISHED")
    print("----------------------------")
    print("Post ID :", post["id"])
    print("Title   :", post["title"]["rendered"])
    print("Status  :", post["status"])
    print("URL     :", post["link"])

    if "categories" in data:
        print("Categories :", data["categories"])

    if featured_media:
        print("Featured Image :", featured_media)

    return post


if __name__ == "__main__":

    print("wordpress.py is ready.")