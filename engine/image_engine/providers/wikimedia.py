"""
===========================================
ShowBiz Image Engine
providers/wikimedia.py
Version 3.0
===========================================

Prototype Wikimedia provider.

Returns sample ImageResult objects.

Uses package imports.
"""

from engine.image_engine.providers.base import (
    ImageProvider,
    ImageResult,
)


class WikimediaProvider(ImageProvider):

    provider_name = "Wikimedia Commons"

    def search(self, query):

        print(f"\nSearching {self.provider_name} for: {query}")

        return [

            ImageResult(
                title=f"{query} Image 1",
                image_url="https://example.org/image1.jpg",
                page_url="https://commons.wikimedia.org",
                width=2400,
                height=1600,
                source=self.provider_name,
                license="CC BY-SA 4.0"
            ),

            ImageResult(
                title=f"{query} Image 2",
                image_url="https://example.org/image2.jpg",
                page_url="https://commons.wikimedia.org",
                width=1800,
                height=1200,
                source=self.provider_name,
                license="CC BY-SA 4.0"
            ),

            ImageResult(
                title=f"{query} Image 3",
                image_url="https://example.org/image3.jpg",
                page_url="https://commons.wikimedia.org",
                width=1200,
                height=800,
                source=self.provider_name,
                license="CC BY-SA 4.0"
            )

        ]


def main():

    provider = WikimediaProvider()

    images = provider.search("Taylor Swift")

    print()
    print("=" * 60)
    print("WIKIMEDIA PROVIDER TEST")
    print("=" * 60)

    for image in images:

        print(f"Title      : {image.title}")
        print(f"Image URL  : {image.image_url}")
        print(f"Page URL   : {image.page_url}")
        print(f"Resolution : {image.width} x {image.height}")
        print(f"Source     : {image.source}")
        print(f"License    : {image.license}")
        print("-" * 60)


if __name__ == "__main__":
    main()