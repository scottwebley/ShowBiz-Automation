"""
===========================================
ShowBiz Image Selector
Version 3.6 (Debug)
===========================================

Purpose:
    Coordinate the featured image workflow.

Workflow:
    1. Search the Media Library.
    2. Remove invalid document/legal candidates.
    3. Ask the AI Image Verifier to choose
       the best candidate.
    4. Use the approved Media Library image.
    5. Search TMDb for official movie/TV artwork.
    6. Search Unsplash.
    7. Generate an AI image.
"""

from engine.image_generator import generate_image
from engine.image_search import search_media_library
from engine.image_verifier import verify_image
from engine.image_providers.tmdb import get_movie_poster
from engine.image_providers.unsplash import get_unsplash_image


BLOCKED_IMAGE_TERMS = (
    "agreement",
    "contract",
    "signature",
    "invoice",
    "receipt",
    "proposal",
    "application",
    "form",
    "document",
    "legal",
    "purchase",
    "sale",
)


def is_valid_media_candidate(candidate):
    """
    Reject non-editorial files.
    """

    text = " ".join(
        [
            str(candidate.get("title", "")),
            str(candidate.get("filename", "")),
            str(candidate.get("url", "")),
        ]
    ).lower()

    for term in BLOCKED_IMAGE_TERMS:
        if term in text:
            return False

    return True


def get_featured_image(story):
    """
    Returns either:

        media:<id>

    or

        path/to/generated/image.png
    """

    print("\n" + "=" * 60)
    print("MEDIA LIBRARY SEARCH")
    print("=" * 60)
    print(f"Headline : {story.get('headline', '')}")
    print(f"Category : {story.get('category', '')}")
    print()

    candidates = search_media_library(story)

    print(f"Candidates returned : {len(candidates)}")

    if candidates:
        print("\nTop candidates:")
        for i, candidate in enumerate(candidates[:10], 1):
            print(
                f"{i:2d}. "
                f"{candidate.get('title', '(no title)')} "
                f"(ID: {candidate.get('id', '?')})"
            )

    candidates = [
        candidate
        for candidate in candidates
        if is_valid_media_candidate(candidate)
    ]

    print(f"\nValid candidates : {len(candidates)}")

    #
    # First choice:
    # AI-approved Media Library image.
    #

    if candidates:

        print("\n========================================")
        print("IMAGE VERIFICATION")
        print("========================================")

        decision = verify_image(story, candidates)

        if decision and decision.get("media_id"):

            print("\n✓ Image approved.\n")
            print(f"Media ID   : {decision['media_id']}")
            print(
                f"Confidence : "
                f"{decision.get('confidence', '?')}"
            )
            print(
                f"Reason     : "
                f"{decision.get('reason', '')}"
            )

            return f"media:{decision['media_id']}"

        #
        # No Media Library image was approved.
        #

        print("\n⚠ Verifier rejected all Media Library candidates.")
        print("Continuing to other providers...\n")

    else:

        print("\n⚠ No valid Media Library candidates.")

    #
    # Second choice:
    # TMDb
    #

    print("\n========================================")
    print("TMDb SEARCH")
    print("========================================")

    tmdb_image = get_movie_poster(story)

    if tmdb_image:

        print("✓ Using TMDb poster.")
        return tmdb_image

    print("No TMDb image found.")

    #
    # Third choice:
    # Unsplash
    #

    print("\n========================================")
    print("UNSPLASH SEARCH")
    print("========================================")

    unsplash_image = get_unsplash_image(story)

    if unsplash_image:

        print("✓ Using Unsplash image.")
        return unsplash_image

    print("No Unsplash image found.")

    #
    # Final fallback:
    #

    print("\n========================================")
    print("AI IMAGE GENERATION")
    print("========================================")

    generated = generate_image(story)

    if generated:

        print("✓ AI image generated.")
        return generated

    print("✗ AI image generation failed.")

    return None


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