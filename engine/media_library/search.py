"""
===========================================
ShowBiz Media Library Search
Version 4.5
===========================================

Purpose:
    Fast local search of the WordPress
    Media Library.

Uses:
    media_cache.json

Public Functions:
    find_best_image(query)
    find_best_images(query, limit=10)
    search(query)

Author:
    ShowBiz Automation
"""

import json

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


from engine.media_library.normalize import (
    normalize,
    safe,
)

from engine.media_library.scorer import (
    score_item,
)

from engine.media_library.search_filters import (
    clean_reasons,
    valid_candidate,
)


CACHE_FILE = (
    Path(__file__).parent / "media_cache.json"
)


_MEDIA_CACHE = None


@dataclass
class MediaResult:

    media_id: int
    score: int
    title: str
    filename: str
    url: str
    reason: str
    raw: dict



def load_media():

    global _MEDIA_CACHE

    if _MEDIA_CACHE is not None:

        return _MEDIA_CACHE


    print(
        "\nLoading media cache..."
    )


    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        _MEDIA_CACHE = json.load(f)


    print(
        f"Loaded {len(_MEDIA_CACHE)} media items.\n"
    )


    return _MEDIA_CACHE



def _wordpress_title(item):

    title = item.get(
        "title",
        ""
    )


    if isinstance(
        title,
        dict,
    ):

        return safe(
            title.get(
                "rendered"
            )
        )


    return safe(
        title
    )



def _display_title(item):

    image_meta = (
        item.get(
            "media_details",
            {}
        )
        .get(
            "image_meta",
            {}
        )
    )


    if isinstance(
        image_meta,
        dict,
    ):

        title = safe(
            image_meta.get(
                "title"
            )
        )

        if title:

            return title


    return _wordpress_title(
        item
    )



def find_best_images(
    query: str,
    limit: int = 10,
) -> List[MediaResult]:


    query = normalize(
        query
    )


    if not query:

        return []


    words = query.split()


    media = load_media()


    results = []


    for item in media:


        score, reasons = score_item(
            item,
            query,
            words,
        )


        if not valid_candidate(
            item,
            score,
            reasons,
        ):

            continue


        cleaned_reasons = clean_reasons(
            reasons
        )


        results.append(
            MediaResult(

                media_id=item.get(
                    "id"
                ),

                score=score,

                title=_display_title(
                    item
                ),

                filename=safe(
                    item.get(
                        "filename"
                    )
                ),

                url=safe(
                    item.get(
                        "source_url"
                    )
                ),

                reason=", ".join(
                    cleaned_reasons
                ),

                raw=item,
            )
        )


    results.sort(
        key=lambda result: (
            result.score,
            len(result.title),
        ),
        reverse=True,
    )


    return results[:limit]



def find_best_image(
    query: str,
) -> Optional[MediaResult]:


    results = find_best_images(
        query=query,
        limit=1,
    )


    if not results:

        return None


    return results[0]



def search(
    query: str,
):

    results = find_best_images(
        query=query,
        limit=10,
    )


    if not results:

        print(
            "\nNo matching image found."
        )

        return


    print()

    print(
        "=" * 60
    )

    print(
        "TOP MEDIA MATCHES"
    )

    print(
        "=" * 60
    )


    for index, result in enumerate(
        results,
        start=1,
    ):

        print()

        print(
            f"#{index}"
        )

        print(
            "-" * 60
        )

        print(
            f"Media ID   : {result.media_id}"
        )

        print(
            f"Score      : {result.score}"
        )

        print(
            f"Title      : {result.title}"
        )

        print(
            f"Filename   : {result.filename}"
        )

        print(
            f"URL        : {result.url}"
        )

        print(
            f"Matched On : {result.reason}"
        )



def main():

    print()

    print(
        "=" * 60
    )

    print(
        "SHOWBIZ MEDIA SEARCH"
    )

    print(
        "=" * 60
    )


    while True:

        query = input(
            "\nSearch (blank to quit): "
        ).strip()


        if not query:

            break


        search(
            query
        )



if __name__ == "__main__":

    main()