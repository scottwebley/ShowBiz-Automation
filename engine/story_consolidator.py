"""
story_consolidator.py
ShowBiz Story Consolidator v1.0

Version 1 is ANALYSIS ONLY.

It never removes stories.
It never changes rankings.
It never changes publishing.

It simply reports headlines that appear to describe the same story.
"""

import re
from difflib import SequenceMatcher


SIMILARITY_THRESHOLD = 0.90

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "in", "into", "is", "it", "of",
    "on", "or", "that", "the", "to", "with"
}


def _normalize(text):
    """Normalize headline for comparison."""

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[^\w\s]", " ", text)

    words = [
        word
        for word in text.split()
        if word not in STOP_WORDS
    ]

    return " ".join(words)


def _similarity(a, b):
    """Return similarity score between two headlines."""

    return SequenceMatcher(
        None,
        _normalize(a),
        _normalize(b)
    ).ratio()


def analyze_story_duplicates(stories):
    """
    Analyze stories for duplicate headlines.

    Returns the original story list unchanged.
    """

    print("\n===================================")
    print("      STORY CONSOLIDATOR")
    print("      Analysis Mode v1.0")
    print("===================================")

    print(f"Stories downloaded: {len(stories)}\n")

    duplicate_count = 0

    for i in range(len(stories)):

        headline1 = stories[i].get("headline", "")

        for j in range(i + 1, len(stories)):

            headline2 = stories[j].get("headline", "")

            score = _similarity(headline1, headline2)

            if score >= SIMILARITY_THRESHOLD:

                duplicate_count += 1

                print("-----------------------------------")
                print(
                    f"Possible Duplicate "
                    f"({score * 100:.1f}%)"
                )
                print()

                print("Story A:")
                print(headline1)
                print()

                print("Story B:")
                print(headline2)
                print()

    if duplicate_count == 0:
        print("No obvious duplicate headlines found.")

    print("\n===================================\n")

    # IMPORTANT:
    # Version 1 NEVER modifies stories.

    return stories