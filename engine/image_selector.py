"""
===========================================
ShowBiz Image Selector
Version 3.4
===========================================

Purpose:
    Coordinate the featured image workflow.

Workflow:
    1. Search the Media Library.
    2. Remove invalid document/legal candidates.
    3. Ask the AI Image Verifier to choose
       the best candidate.
    4. Use the approved Media Library image.
    5. If no valid Media Library image exists,
       generate an AI image.

Author:
    ShowBiz Automation
"""

from engine.image_generator import generate_image
from engine.image_search import search_media_library
from engine.image_verifier import verify_image
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

    candidates = search_media_library(story)

    candidates = [
        candidate
        for candidate in candidates
        if is_valid_media_candidate(candidate)
    ]

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
        # Only fallback to a valid editorial image.
        #

        fallback = candidates[0]

        print(
            "\n⚠ Verifier did not approve a candidate."
        )
        print(
            "Using highest-ranked valid Media Library image."
        )
        print(
            f"Media ID : {fallback['media_id']}"
        )
        print(
            f"Title    : {fallback['title']}"
        )

        return f"media:{fallback['media_id']}"
        #
    # No valid Media Library candidates.
    #

    print("\nNo valid Media Library candidates found.")

    #
    # Second choice:
    # Download a legal editorial image from Unsplash.
    #

    print("Searching Unsplash...\n")

    unsplash_image = get_unsplash_image(story)

    if unsplash_image:

        print("✓ Using Unsplash image.")
        return unsplash_image

    #
    # Final fallback:
    # Generate an AI editorial image.
    #

    print("No Unsplash image found.")
    print("Generating new editorial image...\n")

    generated = generate_image(story)

    if generated:
        return generated

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