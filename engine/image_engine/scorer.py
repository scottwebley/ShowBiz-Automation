"""
===========================================
ShowBiz Image Engine
scorer.py
Version 2.0
===========================================

Scores candidate images returned by providers.
"""

import os
import sys

# Allow scorer.py to import from providers/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROVIDERS_DIR = os.path.join(CURRENT_DIR, "providers")

if PROVIDERS_DIR not in sys.path:
    sys.path.insert(0, PROVIDERS_DIR)

from config import MIN_WIDTH, MIN_HEIGHT
from wikimedia import WikimediaProvider


def score_image(image):

    score = 0

    # Resolution

    if image.width >= MIN_WIDTH:
        score += 30
    else:
        score += 10

    if image.height >= MIN_HEIGHT:
        score += 20
    else:
        score += 5

    # Metadata

    if image.license:
        score += 10

    if image.source:
        score += 10

    if image.page_url:
        score += 10

    if image.image_url:
        score += 20

    return score


def score_images(images):

    for image in images:
        image.score = score_image(image)

    return sorted(
        images,
        key=lambda img: img.score,
        reverse=True
    )


def main():

    provider = WikimediaProvider()

    images = provider.search("Taylor Swift")

    ranked = score_images(images)

    print()
    print("=" * 60)
    print("IMAGE SCORES")
    print("=" * 60)

    for image in ranked:

        print(f"Score : {image.score}")
        print(f"Title : {image.title}")
        print(f"Size  : {image.width} x {image.height}")
        print(f"Source: {image.source}")
        print("-" * 60)


if __name__ == "__main__":
    main()