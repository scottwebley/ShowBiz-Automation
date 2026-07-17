"""
Featured Entertainer storage helpers.
"""

import json
from datetime import datetime
from pathlib import Path


FEATURED_JSON = Path(
    "data/featured_entertainer.json"
)

ARCHIVE_DIR = Path(
    "data/featured_entertainers"
)


def save_featured_entertainer(report, post, week):
    """
    Save the Featured Entertainer data used
    by the homepage updater.
    """

    FEATURED_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "week": week,
        "name": report.get("name", ""),
        "profession": report.get("profession", ""),
        "headline": report.get("headline", ""),
        "url": post.get("link", ""),
        "post_id": post.get("id", 0),
    }

    with open(
        FEATURED_JSON,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(
        "✓ featured_entertainer.json updated"
    )


def archive_featured_entertainer(
    profile,
    article,
):
    """
    Save an archive copy of this week's
    Featured Entertainer.
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
                ""
            )
        )

    print(
        f"✓ Archived: {json_file.name}"
    )