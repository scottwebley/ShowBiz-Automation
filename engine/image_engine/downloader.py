"""
===========================================
ShowBiz Image Engine
downloader.py
Version 1.0
===========================================

Downloads an image selected by the
Image Engine.

This is a prototype.

It attempts to download the image_url
contained in an ImageResult.
"""

import os
import requests

from config import TEST_IMAGE_FOLDER


def ensure_folder():

    os.makedirs(TEST_IMAGE_FOLDER, exist_ok=True)


def download_image(image):

    ensure_folder()

    filename = image.title.lower().replace(" ", "_") + ".jpg"

    destination = os.path.join(TEST_IMAGE_FOLDER, filename)

    print()
    print("Downloading:")
    print(image.image_url)

    try:

        response = requests.get(
            image.image_url,
            timeout=15
        )

        response.raise_for_status()

        with open(destination, "wb") as file:
            file.write(response.content)

        print(f"✓ Saved: {destination}")

        return destination

    except Exception as error:

        print()
        print("Download failed.")
        print(error)

        return None


def main():

    from scorer import score_images
    from providers.wikimedia import WikimediaProvider

    provider = WikimediaProvider()

    images = provider.search("Taylor Swift")

    ranked = score_images(images)

    best = ranked[0]

    print()
    print("=" * 60)
    print("BEST IMAGE")
    print("=" * 60)

    print(best.title)
    print(best.image_url)

    download_image(best)


if __name__ == "__main__":
    main()