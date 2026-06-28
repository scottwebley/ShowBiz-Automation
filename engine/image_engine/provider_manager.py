"""
===========================================
ShowBiz Image Engine
provider_manager.py
Version 2.0
===========================================

Coordinates all image providers.
"""

from engine.image_engine.providers.wikimedia import WikimediaProvider


class ProviderManager:

    def __init__(self):

        self.providers = [
            WikimediaProvider()
        ]

    def search(self, query):

        all_results = []

        print()
        print("=" * 60)
        print("SEARCHING IMAGE PROVIDERS")
        print("=" * 60)

        for provider in self.providers:

            print(f"\nProvider: {provider.provider_name}")

            try:

                results = provider.search(query)

                print(f"Found {len(results)} images")

                all_results.extend(results)

            except Exception as error:

                print(f"Provider failed: {error}")

        print()
        print(f"Total Images Found: {len(all_results)}")

        return all_results


def main():

    manager = ProviderManager()

    images = manager.search("Taylor Swift")

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    for image in images:

        print(image.title)
        print(image.source)
        print()


if __name__ == "__main__":
    main()