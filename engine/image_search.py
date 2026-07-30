"""
===========================================
ShowBiz Image Search
Version 3.2
===========================================

Purpose:
    Search the local Media Library for the
    best matching featured image.

Workflow:
    1. Extract entertainment entities.
    2. Build search queries.
    3. Search Media Library.
    4. Remove invalid candidates.
    5. Rank candidates.
    6. Return best candidates.

Author:
    ShowBiz Automation
"""

from engine.entity_extractor import extract_entities
from engine.image_query_builder import build_search_queries
from engine.image_candidate_ranker import rank_candidates
from engine.media_library.search import find_best_images


MINIMUM_SCORE = 175


BLOCKED_MEDIA_TERMS = (
    "agreement",
    "contract",
    "signature",
    "invoice",
    "receipt",
    "proposal",
    "application",
    "document",
    "legal",
    "purchase",
    "sale",
    ".pdf",
)


def is_valid_candidate(result, story):
    """
    Reject non-editorial media candidates.
    """

    text = " ".join(
        [
            str(result.title),
            str(result.filename),
            str(
                result.raw.get(
                    "caption",
                    "",
                )
            ),
        ]
    ).lower()

    for term in BLOCKED_MEDIA_TERMS:

        if term in text:

            return False

    #
    # Avoid weak common-name collisions.
    #

    headline = (
        story.get("headline", "")
        .lower()
    )

    title = (
        str(result.title)
        .lower()
    )

    words = headline.split()

    if len(words) > 1:

        first_name = words[0]

        if (
            first_name in title
            and not any(
                word in title
                for word in words[1:]
            )
        ):

            return False

    return True


def search_media_library(story):

    print("\n>>> IMAGE_SEARCH DEBUG BUILD 2026-07-09 <<<")

    queries = build_search_queries(story)

    print("\n========================================")
    print("IMAGE SEARCH")
    print("========================================")

    print(
        f"\nHeadline:\n"
        f"{story.get('headline', '')}"
    )

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

    all_results = []

    seen_media = set()

    print()

    for query in queries:

        print(f"Searching: {query}")

        results = find_best_images(
            query=query,
            limit=10,
        )

        for result in results:

            print(
                f"   Match: {result.title} "
                f"(Score {result.score})"
            )

            if not is_valid_candidate(
                result,
                story,
            ):

                print(
                    "   ✗ Rejected invalid media"
                )

                continue

            existing = next(
                (
                    r
                    for r in all_results
                    if r.media_id
                    == result.media_id
                ),
                None,
            )

            if existing:

                if result.score > existing.score:

                    existing.score = result.score
                    existing.reason = (
                        result.reason
                    )

                continue

            all_results.append(result)

    all_results.sort(
        key=lambda r: r.score,
        reverse=True,
    )

    candidates = []

    for result in all_results:

        if result.score < MINIMUM_SCORE:
            continue

        if result.media_id in seen_media:
            continue

        seen_media.add(
            result.media_id
        )

        print(
            "\n========================================"
        )
        print(
            "MEDIA LIBRARY MATCH"
        )
        print(
            "========================================"
        )

        print(
            f"Title      : {result.title}"
        )

        print(
            f"Media ID   : {result.media_id}"
        )

        print(
            f"Score      : {result.score}"
        )

        print(
            f"Reason     : {result.reason}"
        )

        candidates.append(
            {
                "media_id": result.media_id,
                "title": result.title,
                "caption": result.raw.get("caption", ""),
                "filename": result.filename,
                "score": result.score,
                "reason": result.reason,
            }
        )

    print(
        "\n>>> ENTERING rank_candidates() <<<"
    )

    candidates = rank_candidates(
        story,
        candidates,
    )

    print(
        "\n>>> RETURNED FROM rank_candidates() <<<"
    )

    print(
        "\n========================================"
    )
    print(
        "FINAL RANKED ORDER"
    )
    print(
        "========================================"
    )

    if candidates:

        for i, candidate in enumerate(
            candidates,
            1,
        ):

            print(
                f"{i:2d}. "
                f"{candidate['media_id']:>6}  "
                f"{candidate['title']}"
            )

    else:

        print(
            "No candidates."
        )

    print(
        "\n========================================"
    )

    return candidates


def main():
    import sys

    if len(sys.argv) > 1:
        headline = " ".join(sys.argv[1:])
    else:
        headline = input("Headline: ").strip()

    story = {
        "headline": headline,
        "summary": "",
        "category": "Celebrity",
    }

    results = search_media_library(story)

    print()

    if results:
        print("MATCHES FOUND")
        print(f"Candidates : {len(results)}")

        for image in results:
            print(f"- {image['media_id']}: {image['title']}")
    else:
        print("NO MATCH")

    print()

    if results:

        print(
            "MATCHES FOUND"
        )

        print(
            f"Candidates : {len(results)}"
        )

        for image in results:

            print(
                f"- {image['media_id']}: "
                f"{image['title']}"
            )

    else:

        print(
            "NO MATCH"
        )


if __name__ == "__main__":
    main()