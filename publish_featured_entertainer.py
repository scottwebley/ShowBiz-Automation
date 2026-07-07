import json
from datetime import datetime, timedelta
from pathlib import Path

from engine.ai_news import get_top_stories
from engine.featured_entertainer import (
    generate_featured_entertainer,
)
from engine.featured_entertainer_profile import (
    generate_featured_entertainer_profile,
)
from engine.featured_entertainer_writer_v3 import (
    write_featured_entertainer,
)
from engine.image_selector import get_featured_image
from engine.wordpress import publish_post


CATEGORY_ID = 63

FEATURED_JSON = Path(
    "data/featured_entertainer.json"
)

ARCHIVE_DIR = Path(
    "data/featured_entertainers"
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


def archive_featured_entertainer(
    profile,
    article,
):
    """
    Save a permanent archive copy.
    """

    ARCHIVE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    slug = (
        profile.get("name", "")
        .lower()
        .replace(" ", "-")
        .replace("/", "-")
    )

    date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    json_file = (
        ARCHIVE_DIR /
        f"{date}-{slug}.json"
    )

    html_file = (
        ARCHIVE_DIR /
        f"{date}-{slug}.html"
    )

    with open(
        json_file,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            profile,
            f,
            indent=4,
            ensure_ascii=False,
        )

    with open(
        html_file,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            article.get(
                "content",
                "",
            )
        )

    print(
        f"✓ Archived: {json_file.name}"
    )


def already_published_this_week():

    return False

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
        return False

    # Temporary test override.
    # Remove this line after testing.

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

    profile = generate_featured_entertainer_profile(
        report
    )

    if profile is None:

        print(
            "\nFeatured profile "
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
        profile
    )

    print(
        "✓ HTML article created.\n"
    )

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
        save_featured_entertainer(
        report,
        post
    )

    archive_featured_entertainer(
        profile,
        article,
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