"""
===========================================
ShowBiz Local Story Runner
Version 2.0
===========================================

Purpose:
    Runtime implementation for the
    Local Story Selector.

    This module contains the workflow for
    selecting the best local story using
    deterministic editorial scoring.

    It NEVER calls OpenAI.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

from engine.editorial_duplicates import (
    build_duplicate_groups,
)

from engine.editorial_scoring import (
    editorial_story_score,
    story_sort_key,
)


def _headline(story):
    return (
        story.get("headline")
        or story.get("title")
        or ""
    ).strip()


def run_local_story_selector(stories):
    """
    Select the highest-ranked story using
    deterministic local editorial scoring.
    """

    if not stories:
        return None

    valid = []

    for story in stories:

        if _headline(story):
            valid.append(story)

    if not valid:
        return stories[0]

    #
    # Build duplicate groups once.
    #

    duplicate_groups = build_duplicate_groups(valid)

    ranked = sorted(
        valid,
        key=lambda story: story_sort_key(
            story,
            duplicate_groups,
        ),
        reverse=True,
    )

    print()
    print("=" * 50)
    print("LOCAL STORY SELECTOR V2")
    print("=" * 50)
    print()

    print("Top Candidates:")

    for i, story in enumerate(ranked[:10], 1):

        print(
            f"{i:2d}. "
            f"[{story.get('category','')}] "
            f"quality="
            f"{editorial_story_score(story, duplicate_groups):4d} "
            f"editorial={story.get('editorial_score',0):3} "
            f"feed={story.get('score',0):3} :: "
            f"{_headline(story)}"
        )

    print()

    winner = ranked[0]

    print("✓ Local Story Selector chose:")
    print(f"  {_headline(winner)}")

    return winner


if __name__ == "__main__":

    sample = [
        {
            "headline":
                "Disney Announces New Pixar Film Release Date",
            "category": "Movies",
            "source": "Deadline",
            "score": 61,
        },
        {
            "headline":
                "Disney Announces New Pixar Film Release Date",
            "category": "Movies",
            "source": "Yahoo",
            "score": 60,
        },
        {
            "headline":
                "Warner Bros. Reveals First Trailer For Major DC Movie",
            "category": "Movies",
            "source": "Variety",
            "score": 59,
        },
    ]

    winner = run_local_story_selector(sample)

    print()
    print("Winner:")
    print(_headline(winner))