import json
from datetime import datetime, timedelta
from pathlib import Path

from engine.ai_news import get_top_stories
from engine.featured_entertainer import (
    generate_featured_entertainer,
)
from engine.featured_entertainer_writer import (
    write_featured_entertainer,
)
from engine.image_selector import get_featured_image
from engine.wordpress import publish_post


CATEGORY_ID = 63

FEATURED_JSON = Path(
    "data/featured_entertainer.json"
)


def current_editorial_week():
    """
    Return the Monday of the current editorial week.
    """

    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    return (
        f"Week of "
        f"{monday.strftime('%B')} "
        f"{monday.day}, "
        f"{monday.year}"
    )


def save_featured_entertainer(report, post):
    """
    Save homepage data.
    """

    FEATURED_JSON.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "week": current_editorial_week(),
        "name": report.get("name", ""),
        "profession": report.get("profession", ""),
        "headline": report.get("headline", ""),
        "url": post.get("link", ""),
        "post_id": post.get("id", 0),
    }

    with open(
        FEATURED_JSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    print(
        "✓ featured_entertainer.json updated"
    )


def already_published_this_week():

    if not FEATURED_JSON.exists():
        return False

    try:

        with open(
            FEATURED_JSON,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return (
            data.get("week")
            == current_editorial_week()
        )

    except Exception:

        return False


def main():

    print("\n==============================")
    print(" FEATURED ENTERTAINER")
    print("==============================\n")

    if already_published_this_week():

        print(
            "Featured Entertainer has already "
            "been published this week."
        )

        print("Skipping publication.\n")

        return

    print(
        "STEP 1: Downloading this week's "
        "entertainment news..."
    )

    stories = get_top_stories()

    if not stories:

        print("No stories found.")

        return

    print(
        f"✓ {len(stories)} stories downloaded.\n"
    )

    print(
        "STEP 2: AI editorial analysis..."
    )

    report = generate_featured_entertainer(
        stories
    )

    if report is None:

        print(
            "\nFeatured Entertainer "
            "generation failed.\n"
        )

        return

    print(
        "✓ Featured Entertainer selected.\n"
    )

    print(
        "STEP 3: Writing HTML article..."
    )

    article = write_featured_entertainer(
        report
    )

    print(
        "✓ HTML article created.\n"
    )

    #
    # Use the exact story selected
    # by the AI engine.
    #

    image_story = report.get(
        "source_story"
    )

    if image_story is None:

        image_story = stories[0]

    print(
        "STEP 4: Selecting featured image..."
    )

    image = get_featured_image(
        image_story
    )
    if image:

        article["image"] = image

        print(
            "✓ Featured image selected.\n"
        )

    else:

        print(
            "⚠ No featured image available."
        )

    #
    # Publish into the Featured
    # Entertainer category.
    #

    article["category_id"] = CATEGORY_ID

    print(
        "STEP 5: Publishing article..."
    )

    post = publish_post(article)

    if not post:

        print(
            "\nPublication failed.\n"
        )

        return

    #
    # Save homepage JSON.
    #

    save_featured_entertainer(
        report,
        post
    )

    print("\n==============================")
    print(" FEATURED ENTERTAINER PUBLISHED")
    print("==============================")
    print(f"Post ID : {post['id']}")
    print(
        f"Title   : "
        f"{post['title']['rendered']}"
    )
    print(
        f"URL     : "
        f"{post['link']}"
    )
    print("==============================\n")


if __name__ == "__main__":
    main()