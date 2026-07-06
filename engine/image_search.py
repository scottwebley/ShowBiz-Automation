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

from engine.entity_extractor import extract_entities
from engine.image_query_builder import build_search_queries
from engine.image_candidate_ranker import rank_candidates
from engine.media_library.search import find_best_images


MINIMUM_SCORE = 175


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

        candidates = rank_candidates(
        story,
        candidates,
    )

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