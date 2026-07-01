"""
===========================================
ShowBiz Image Search
Version 1.0
===========================================

Purpose:
    Search the local Media Library for the
    best matching featured image.

Workflow:
    1. Extract meaningful search terms.
    2. Build progressively broader queries.
    3. Search the Media Library.
    4. Return qualifying image candidates.

Author:
    ShowBiz Automation
"""

import re

from engine.media_library.search import find_best_images


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
    """

    headline = story.get("headline", "")

    keywords = extract_keywords(headline)

    queries = []

    if keywords:
        queries.append(" ".join(keywords))

    if len(keywords) >= 3:
        queries.append(" ".join(keywords[:3]))

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[:2]))

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[-2:]))

    queries.extend(keywords)

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


def search_media_library(story):
    """
    Search the Media Library.

    Returns:

        list[dict]
            Qualifying image candidates.

        []
            If no qualifying images are found.
    """

    queries = build_search_queries(story)

    best_result = None
    candidates = []
    seen_media = set()

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

        results = find_best_images(query, limit=10)

        if not results:
            continue

        for result in results:

            print(
                f"   Match: {result.title} "
                f"(Score {result.score})"
            )

            if (
                best_result is None
                or result.score > best_result.score
            ):
                best_result = result

            if result.score < MINIMUM_SCORE:
                continue

            if result.media_id in seen_media:
                continue

            seen_media.add(result.media_id)

            print("\n========================================")
            print("MEDIA LIBRARY MATCH")
            print("========================================")
            print(f"Title      : {result.title}")
            print(f"Media ID   : {result.media_id}")
            print(f"Score      : {result.score}")
            print(f"Reason     : {result.reason}")

            print("\n✓ Using Media Library image.\n")

            candidates.append(
                {
                    "media_id": result.media_id,
                    "title": result.title,
                    "caption": result.raw.get("caption", ""),
                    "filename": result.filename,
                }
            )

    print("\n========================================")

    if best_result:

        print("BEST MATCH FOUND")
        print("----------------------------------------")
        print(f"Title    : {best_result.title}")
        print(f"Score    : {best_result.score}")
        print(f"Required : {MINIMUM_SCORE}")

    else:

        print("No Media Library matches found.")

    return candidates


def main():

    story = {
        "headline": "Why Supergirl Crashed at the Box Office",
        "summary": "Analysis of the film's opening weekend.",
        "category": "Movies",
    }

    results = search_media_library(story)

    print()

    if results:

        print("MATCHES FOUND")
        print(f"Candidates : {len(results)}")

        for image in results:
            print(
                f"- {image['media_id']}: "
                f"{image['title']}"
            )

    else:

        print("NO MATCH")


if __name__ == "__main__":
    main()