"""
===========================================
ShowBiz Image Selector
Version 3.1
===========================================

Purpose:
    Coordinate the featured image workflow.

Workflow:
    1. Search the Media Library.
    2. Ask the AI Image Verifier to choose
       the best candidate.
    3. Use the approved Media Library image.
    4. Otherwise generate a new editorial image.

Author:
    ShowBiz Automation
"""

from engine.image_generator import generate_image
from engine.image_search import search_media_library
from engine.image_verifier import verify_image


def get_featured_image(story):
    """
    Returns either:

        media:<id>

    or

        path/to/generated/image.png
    """

    candidates = search_media_library(story)

    if candidates:

        print("\n========================================")
        print("IMAGE VERIFICATION")
        print("========================================")

        decision = verify_image(story, candidates)

        if decision and decision.get("media_id"):

            print("\n✓ Image approved.\n")
            print(f"Media ID   : {decision['media_id']}")
            print(f"Confidence : {decision.get('confidence', '?')}")
            print(f"Reason     : {decision.get('reason', '')}")

            return f"media:{decision['media_id']}"

        print("\nImage rejected by verifier.")

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