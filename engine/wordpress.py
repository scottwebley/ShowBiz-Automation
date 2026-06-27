import requests
from requests.auth import HTTPBasicAuth

from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

# True = Publish immediately
# False = Save as Draft
PUBLISH_IMMEDIATELY = True


def get_category_id(category_name):
    """
    Look up a WordPress category by its name.
    """

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/categories",
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        headers=HEADERS,
        params={"search": category_name},
    )

    if response.status_code != 200:
        return None

    for category in response.json():
        if category["name"].lower() == category_name.lower():
            return category["id"]

    return None


def normalize_category(ai_category):
    """
    Convert AI-generated categories into your WordPress categories.
    """

    if not ai_category:
        return "Entertainment Industry"

    mapping = {
        "Movie": "Movies",
        "Movies": "Movies",
        "Film": "Movies",

        "TV": "TV & Streaming",
        "Television": "TV & Streaming",
        "Streaming": "TV & Streaming",
        "TV & Streaming": "TV & Streaming",

        "Music": "Music",

        "Celebrity": "Celebrity News",
        "Celebrity News": "Celebrity News",

        "Gaming": "Gaming",

        "Style": "Style",

        "Entertainment": "Entertainment Industry",
        "Industry": "Entertainment Industry",
    }

    return mapping.get(ai_category, "Entertainment Industry")


def publish_post(article):

    wp_category = normalize_category(article.get("category", ""))

    category_id = get_category_id(wp_category)

    data = {
        "title": article["title"],
        "content": article["content"],
        "excerpt": article["excerpt"],
        "status": "publish" if PUBLISH_IMMEDIATELY else "draft",
    }

    if category_id:
        data["categories"] = [category_id]

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        headers=HEADERS,
        json=data,
    )

    print("\nStatus:", response.status_code)

    if response.status_code == 201:

        post = response.json()

        print("\n✅ SUCCESS")
        print("Post ID:", post["id"])
        print("Title:", post["title"]["rendered"])
        print("Category:", wp_category)
        print("Status:", post["status"])
        print("Link:", post["link"])

        return post

    print("\n❌ FAILED")
    print(response.text)

    return None