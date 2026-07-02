"""
===========================================
ShowBiz Homepage Feed
Version 1.0
===========================================

Builds the editorial homepage feed used by the
ShowBiz front page.

Input:
    ranked_stories

Output:
    data/front_page.json
"""

import json
from datetime import datetime
from pathlib import Path


OUTPUT_FILE = Path("data/front_page.json")


def build_front_page_feed(ranked_stories):
    """
    Build the homepage editorial feed.

    Parameters
    ----------
    ranked_stories : list
        Stories returned by Homepage Ranker.

    Returns
    -------
    dict
        Homepage feed dictionary.
    """

    if not ranked_stories:
        raise ValueError("No ranked stories supplied.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    feed = {
        "generated_at": datetime.utcnow().isoformat(),
        "top_story": ranked_stories[0],
        "latest_news": ranked_stories[1:11],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=4, ensure_ascii=False)

    print(f"✓ Homepage feed written to {OUTPUT_FILE}")

    return feed


def main():
    print(
        "This module is intended to be imported by newsroom.py.\n"
        "No standalone action performed."
    )


if __name__ == "__main__":
    main()