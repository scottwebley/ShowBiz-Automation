"""
===========================================
ShowBiz Local Story Selector
Version 1.0
===========================================

Purpose:
    Offline fallback story selector.

This selector NEVER calls OpenAI.

It is used only when both the Homepage
Ranker and AI Story Selector fail.

Returns the ORIGINAL story object so that
all metadata is preserved.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


#
# Category priority.
#
# Higher number = more desirable.
#

CATEGORY_PRIORITY = {
    "Streaming": 100,
    "Movies": 95,
    "Movie": 95,
    "Television": 90,
    "TV": 90,
    "Entertainment Industry": 85,
    "Music": 80,
    "Awards": 75,
    "Celebrity": 70,
    "Style": 60,
}


def _category_score(story):

    category = story.get("category", "")

    return CATEGORY_PRIORITY.get(category, 50)


def _story_score(story):
    """
    Build a deterministic ranking tuple.

    The tuple is ordered from most
    important to least important.
    """

    return (

        #
        # Category importance
        #

        _category_score(story),

        #
        # Editorial score if present
        #

        story.get("editorial_score", 0),

        #
        # Feed score if present
        #

        story.get("score", 0),

        #
        # Longer headlines usually contain
        # more specific news.
        #

        len(story.get("headline", "")),
    )


def select_local_story(stories):
    """
    Select the best story using only
    local information.

    Never calls OpenAI.
    """

    if not stories:
        return None

    valid = []

    for story in stories:

        headline = story.get("headline", "").strip()

        if not headline:
            continue

        valid.append(story)

    if not valid:
        return stories[0]

    winner = max(
        valid,
        key=_story_score,
    )

    print("✓ Local Story Selector chose:")
    print(f"  {winner.get('headline', '')}")

    return winner


#
# Test
#

if __name__ == "__main__":

    sample = [

        {
            "headline": "Small celebrity interview",
            "category": "Celebrity",
            "score": 72,
        },

        {
            "headline": "Major Marvel movie announced",
            "category": "Movies",
            "score": 61,
        },

        {
            "headline": "Streaming giant reveals new series",
            "category": "Streaming",
            "score": 55,
        },
    ]

    winner = select_local_story(sample)

    print()
    print("Winner:")
    print(winner["headline"])