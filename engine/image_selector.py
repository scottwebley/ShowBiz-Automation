"""
===========================================
ShowBiz Image Selector
Version 1.1
===========================================

Purpose:
    Select the best featured image for a story.

Workflow:
    1. Build intelligent search queries.
    2. Search the local Media Library cache.
    3. If a strong match exists, return its Media ID.
    4. Otherwise generate a new editorial image.

Author:
    ShowBiz Automation
"""

import re

from engine.media_library.search import find_best_image
from engine.image_generator import generate_image


MINIMUM_SCORE = 1000

STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "for",
    "to",
    "of",
    "in",
    "on",
    "with",
    "by",
    "from",
    "at",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "returns",
    "return",
    "returned",
    "announces",
    "announce",
    "reveals",
    "reveal",
    "revealed",
    "confirms",
    "confirm",
    "behind",
    "today",
    "new",
    "after",
    "before",
    "during",
    "over",
    "under",
    "into",
    "like",
}


def build_search_queries(story):
    """
    Build progressively simpler search queries.
    """

    headline = story.get("headline", "")

    words = re.findall(r"[A-Za-z0-9']+", headline)

    keywords = [
        w
        for w in words
        if len(w) > 2 and w.lower() not in STOP_WORDS
    ]

    queries = []

    if keywords:
        queries.append(" ".join(keywords))

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[:2]))

    if len(keywords) >= 3:
        queries.append(" ".join(keywords[:3]))

    for word in keywords:
        queries.append(word)

    seen = set()
    final_queries = []

    for query in queries:
        query = query.strip()

        if query and query not in seen:
            final_queries.append(query)
            seen.add(query)

    return final_queries


def get_featured_image(story):
    """
    Returns either:

        media:<id>

    or

        path/to/generated/image.png
    """

    queries = build_search_queries(story)

    best_result = None

    print("Searching Media Library...\n")

    for query in queries:

        print(f"Trying: {query}")

        result = find_best_image(query)

        if not result:
            continue

        print(f"Score: {result.score}")

        if (
            best_result is None
            or result.score > best_result.score
        ):
            best_result = result

        if result.score >= MINIMUM_SCORE:

            print(
                f"\n✓ Using Media Library image "
                f"(Media ID {result.media_id})"
            )

            return f"media:{result.media_id}"

    if best_result:

        print(
            f"\nBest score found: "
            f"{best_result.score}"
        )

    print("\nNo suitable Media Library image found.")

    print("Generating new image...")

    return generate_image(story)


def main():

    print("=" * 60)
    print("SHOWBIZ IMAGE SELECTOR")
    print("=" * 60)

    story = {
        "headline": "Tom Cruise Returns for Mission Impossible",
        "summary": (
            "Tom Cruise returns for another "
            "Mission Impossible film."
        ),
        "category": "Movies",
    }

    image = get_featured_image(story)

    print()
    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(image)


if __name__ == "__main__":
    main()