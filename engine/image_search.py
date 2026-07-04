"""
===========================================
ShowBiz Image Search
Version 2.1
===========================================

Purpose:
    Search the local Media Library for the
    best matching featured image.

Workflow:
    1. Extract entertainment entities.
    2. Search people first.
    3. Search movies / TV / music.
    4. Fall back to keyword phrases.
    5. Return qualifying image candidates.

Author:
    ShowBiz Automation
"""

import re

from engine.entity_extractor import extract_entities
from engine.media_library.search import find_best_images


MINIMUM_SCORE = 1000


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
    Build prioritized search queries.

    Entity searches are performed first.

    Keyword fallback intentionally uses only
    meaningful multi-word phrases to avoid
    noisy searches such as:
        Mad
        star
        dies
        known
        AOL
    """

    headline = story.get("headline", "")

    entities = extract_entities(headline)

    queries = []

    #
    # Highest priority:
    # People
    #

    queries.extend(entities["people"])

    #
    # Movies
    #

    queries.extend(entities["movies"])

    #
    # TV
    #

    queries.extend(entities["tv_shows"])

    #
    # Music
    #

    queries.extend(entities["music_artists"])

    #
    # Organizations
    #

    queries.extend(entities["organizations"])

    #
    # Events
    #

    queries.extend(entities["events"])

    #
    # Keyword phrase fallback
    #

    keywords = extract_keywords(headline)

    if keywords:
        queries.append(" ".join(keywords))

    if len(keywords) >= 3:
        queries.append(" ".join(keywords[:3]))

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[:2]))

    if len(keywords) >= 2:
        queries.append(" ".join(keywords[-2:]))

    #
    # NOTE:
    #
    # We intentionally DO NOT search every
    # individual keyword anymore.
    #
    # This prevents searches such as:
    #
    #   Mad
    #   star
    #   dies
    #   known
    #   AOL
    #
    # which produced many irrelevant Media
    # Library matches.
    #

    #
    # Remove duplicates
    #

    seen = set()
    final = []

    for query in queries:

        query = query.strip()

        if not query:
            continue

        key = query.lower()

        if key in seen:
            continue

        seen.add(key)
        final.append(query)

    return final
def search_media_library(story):

    queries = build_search_queries(story)

    best_result = None
    candidates = []
    seen_media = set()

    print("\n========================================")
    print("IMAGE SEARCH")
    print("========================================")

    print(f"\nHeadline:\n{story.get('headline', '')}")

    entities = extract_entities(
        story.get("headline", "")
    )

    print("\nEntities:")

    if entities["people"]:
        print("  People:")
        for person in entities["people"]:
            print(f"    • {person}")

    if entities["movies"]:
        print("  Movies:")
        for movie in entities["movies"]:
            print(f"    • {movie}")

    print("\nSearch Queries:")

    for query in queries:
        print(f"  • {query}")

    print()

    for query in queries:

        print(f"Searching: {query}")

        results = find_best_images(
            query,
            limit=10,
        )

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
                    "caption": result.raw.get(
                        "caption",
                        "",
                    ),
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
        "headline": (
            "Taylor Swift and Travis Kelce's "
            "expected wedding celebrations "
            "approach"
        ),
        "summary": "",
        "category": "Celebrity",
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