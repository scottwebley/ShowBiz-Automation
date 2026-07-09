"""
===========================================
ShowBiz Pending Story Manager
Version 1.0
===========================================

Purpose:
    Store a Top Story that was selected but
    could not be published because article
    generation failed.

This module does NOT:

    - Select stories
    - Write articles
    - Publish to WordPress

It only stores and retrieves the pending
story state.

Public API:

    save_pending_story(story)
    load_pending_story()
    clear_pending_story()
"""

import json
from pathlib import Path


PENDING_STORY_FILE = Path(
    "data/pending_story.json"
)


def save_pending_story(story):
    """
    Save a story for the next newsroom run.

    Stores only the fields needed to retry
    article generation.
    """

    PENDING_STORY_FILE.parent.mkdir(
        exist_ok=True
    )

    pending = {
        "headline": story.get("headline", ""),
        "summary": story.get("summary", ""),
        "category": story.get(
            "category",
            "Entertainment Industry",
        ),
    }

    with open(
        PENDING_STORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            pending,
            file,
            indent=4,
        )


def load_pending_story():
    """
    Load pending story.

    Returns:
        dict or None
    """

    if not PENDING_STORY_FILE.exists():

        return None

    with open(
        PENDING_STORY_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def clear_pending_story():
    """
    Remove pending story after
    successful publication.
    """

    if PENDING_STORY_FILE.exists():

        PENDING_STORY_FILE.unlink()


if __name__ == "__main__":

    test_story = {
        "headline": "Test Pending Story",
        "summary": "Test summary.",
        "category": "Movies",
    }

    save_pending_story(test_story)

    print(load_pending_story())

    clear_pending_story()

    print(load_pending_story())