"""
===========================================
ShowBiz Image Selector
Version 2.0
===========================================

Purpose:
    Select the best featured image for a story.

Workflow:
    1. Extract meaningful search terms.
    2. Search the local Media Library.
    3. Select the highest-confidence image.
    4. Otherwise generate a new editorial image.

Author:
    ShowBiz Automation
"""

import re

from engine.media_library.search import find_best_image
from engine.image_generator import generate_image


# Minimum acceptable Media Library score.
# Images below this score will be rejected.
MINIMUM_SCORE = 1000

# Words that should never influence image selection.
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "before",
    "behind",
    "by",
    "during",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "like",
    "new",
    "of",
    "on",
    "or",
    "over",
    "returns",
    "return",
    "returned",
    "reveals",
    "reveal",
    "revealed",
    "announces",
    "announce",
    "announced",
    "confirms",
    "confirm",
    "confirmed",
    "that",
    "the",
    "their",
    "this",
    "to",
    "today",
    "under",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def extract_keywords(headline):
    """
    Extract meaningful keywords from a headline.

    Removes punctuation, stop words and
    very short words.
    """

    words = re.findall(r"[A-Za-z0-9']+", headline)

    keywords = []

    for word in words:

        clean = word.strip()

        if len(clean) < 3:
            continue

        if clean.lower() in STOP_WORDS:
            continue

        keywords.append(clean)

    return keywords


def build_search_queries(story):
    """
    Build progressively broader search queries.

    Example:

        Why Supergirl Crashed at the Box Office

    becomes

        Supergirl Crashed Box Office
        Supergirl Crashed
        Supergirl
        Box Office
        Supergirl
        Crashed
        Box
        Office
    """

    headline = story.get("headline", "")

    keywords = extract_keywords(headline)

    queries = []

    #
    # Full cleaned headline
    #

    if keywords:
        queries.append(" ".join(keywords))

    #
    # First three keywords
    #

    if len(keywords) >= 3:
        queries.append(" ".join(keywords[:3]))

    #
    # First two keywords
    #

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[:2]))

    #
    # Last two keywords
    #

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[-2:]))

    #
    # Individual keywords
    #

    queries.extend(keywords)

    #
    # Remove duplicates while preserving order
    #

    seen = set()
    final_queries = []

    for query in queries:

        query = query.strip()

        if not query:
            continue

        key = query.lower()

        if key in seen:
            continue

        seen.add(key)
        final_queries.append(query)

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

    print("\n========================================")
    print("IMAGE SEARCH")
    print("========================================")

    print(f"\nHeadline:\n{story.get('headline', '')}")

    print("\nSearch Queries:")

    for query in queries:
        print(f"  • {query}")

    print()

    for query in queries:

        print(f"Searching: {query}")

        result = find_best_image(query)

        if not result:
            continue

        print(
            f"   Match: {result.title} "
            f"(Score {result.score})"
        )

        if (
            best_result is None
            or result.score > best_result.score
        ):
            best_result = result

        if result.score >= MINIMUM_SCORE:

            print("\n========================================")
            print("MEDIA LIBRARY MATCH")
            print("========================================")
            print(f"Title      : {result.title}")
            print(f"Media ID   : {result.media_id}")
            print(f"Score      : {result.score}")
            print(f"Reason     : {result.reason}")

            print("\n✓ Using Media Library image.\n")

            return f"media:{result.media_id}"

    print("\n========================================")

    if best_result:

        print("BEST MATCH FOUND")
        print("----------------------------------------")
        print(f"Title    : {best_result.title}")
        print(f"Score    : {best_result.score}")
        print(f"Required : {MINIMUM_SCORE}")

    else:

        print("No Media Library matches found.")

    print("\nGenerating new editorial image...\n")

    return generate_image(story)


def main():

    print("=" * 60)
    print("SHOWBIZ IMAGE SELECTOR")
    print("=" * 60)

    story = {
        "headline": "Why Supergirl Crashed at the Box Office",
        "summary": (
            "Analysis of the film's opening weekend."
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