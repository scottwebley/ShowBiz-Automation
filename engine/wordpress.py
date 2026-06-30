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

TOP_STORY_CATEGORY = 64


def get_current_top_story():
    """
    Returns the current Top Story post,
    or None if one doesn't exist.
    """

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        params={
            "categories": TOP_STORY_CATEGORY,
            "per_page": 1,
            "orderby": "date",
            "order": "desc",
        },
        timeout=60,
    )

    if response.status_code != 200:
        return None

    posts = response.json()

    if not posts:
        return None

    return posts[0]


def remove_top_story_category():

    post = get_current_top_story()

    if post is None:

        print("\nNo existing Top Story found.")

        return

    categories = post.get("categories", [])

    if TOP_STORY_CATEGORY not in categories:
        return

    new_categories = [
        c
        for c in categories
        if c != TOP_STORY_CATEGORY
    ]

    print(
        f"\nRemoving Top Story category from "
        f"Post {post['id']}"
    )

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        json={
            "categories": new_categories,
        },
        timeout=60,
    )

    if response.status_code not in (200, 201):

        print(
            "Unable to update previous Top Story."
        )

        print(response.text)

    else:

        print("Previous Top Story updated.")


def publish_post(article):
    """
    Publish a ShowBiz article.

    Automatically:

    • Removes Top Story category
      from the previous Top Story.

    • Publishes the new article.

    • Supports existing Media Library
      images and generated images.
    """

    featured_media = None

    image = article.get("image")

    if image:

        if (
            isinstance(image, str)
            and image.startswith("media:")
        ):

            featured_media = int(
                image.split(":")[1]
            )

            print(
                f"\nUsing existing Media Library image "
                f"(ID {featured_media})"
            )

        else:

            print(
                "\nUploading featured image..."
            )

            featured_media = upload_image(image)

    #
    # Demote previous Top Story
    #

    remove_top_story_category()

    #
    # Build WordPress post
    #

    data = {
        "title": article["title"],
        "content": article["content"],
        "excerpt": article["excerpt"],
        "status": "publish",
        "categories": article["category_ids"],
    }

    if featured_media:
        data["featured_media"] = featured_media
            #
    # Publish
    #

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        headers=HEADERS,
        json=data,
        timeout=60,
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
    print("Categories :", post.get("categories", []))

    if featured_media:
        print("Featured Image :", featured_media)

    return post


if __name__ == "__main__":

    print("wordpress.py is ready.")