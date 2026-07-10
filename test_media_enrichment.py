"""
===========================================
ShowBiz Media Enrichment Test
Version 1.0
===========================================

Purpose:
    Test AI enrichment on one Media
    Library attachment.
"""

import json

from engine.media_library.enrich_media import (
    enrich_media,
)
from engine.media_library.search import (
    load_media,
)


def main():

    media = load_media()

    #
    # Find the first generic image.
    #

    for item in media:

        title = str(
            item.get("title", {})
        ).lower()

        if (
            "aggregator downloaded image"
            in title
        ):

            print()
            print("=" * 60)
            print("TEST IMAGE")
            print("=" * 60)
            print(f"Media ID : {item['id']}")
            print(f"Title    : {item['title']}")
            print()

            result = enrich_media(item)

            print()
            print("=" * 60)
            print("RESULT")
            print("=" * 60)

            print(
                json.dumps(
                    result,
                    indent=4,
                )
            )

            return

    print(
        "No generic media item found."
    )


if __name__ == "__main__":
    main()