"""
===========================================
ShowBiz Local Story Selector
Version 3.0
===========================================

Purpose:
    Public entry point for the offline
    Local Story Selector.

    All implementation has been moved to
    engine.local_story_runner.

    This module exists only to preserve
    the public API.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

from engine.local_story_runner import (
    run_local_story_selector,
)


def select_local_story(stories):
    """
    Select the best story using only
    local information.

    Never calls OpenAI.

    Returns the ORIGINAL story object so
    that all metadata is preserved.
    """

    return run_local_story_selector(stories)


#
# Test
#

if __name__ == "__main__":

    sample = [

        {
            "headline": "Disney Announces New Pixar Film Release Date",
            "category": "Movies",
            "source": "Deadline",
            "score": 61,
        },

        {
            "headline": "Warner Bros. Reveals First Trailer For Major DC Movie",
            "category": "Movies",
            "source": "Variety",
            "score": 59,
        },
    ]

    winner = select_local_story(sample)

    print()

    if winner:
        print("Winner:")
        print(
            winner.get("headline")
            or winner.get("title")
            or ""
        )