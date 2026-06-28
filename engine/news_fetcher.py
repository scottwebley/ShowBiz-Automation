from engine.ai_news import fetch_news


CATEGORY_MAP = {
    "Movies": 7,
    "TV & Streaming": 15,
    "Music": 8,
    "Gaming": 5,
    "Celebrity News": 3,
    "Entertainment Industry": 4,
    "Style": 12,
    "ShowBiz Originals": 11
}


def fetch_story():
    """
    Fetch today's top entertainment story.
    """

    story = fetch_news()

    category = story.get("category", "Entertainment Industry")

    story["category"] = category
    story["category_id"] = CATEGORY_MAP.get(
        category,
        CATEGORY_MAP["Entertainment Industry"]
    )

    # Temporary image location.
    # Later this will be generated automatically.
    story["image"] = "images/latest_story.png"

    return story