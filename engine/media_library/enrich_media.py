"""
===========================================
ShowBiz Media Enrichment
Version 1.0
===========================================

Purpose:
    Coordinate AI enrichment of a single
    Media Library attachment.

Workflow:

    needs_enrichment()
            │
            ▼
        enrich()
            │
            ▼
    confidence >= threshold?
            │
      Yes ─────► update_attachment()
            │
      No
            ▼
         Skip

Author:
    ShowBiz Automation
"""

from engine.media_library.enricher import (
    enrich,
)

from engine.media_library.updater import (
    update_attachment,
)


MIN_CONFIDENCE = 90


def enrich_media(item):
    """
    Enrich one media item.

    Args:
        item (dict)

    Returns:
        dict
    """

    result = enrich(item)

    if result.get("skipped"):

        print()
        print("Skipping media item.")
        print(result["reason"])

        return result

    confidence = result.get(
        "confidence",
        0,
    )

    if confidence < MIN_CONFIDENCE:

        print()
        print(
            "Confidence too low."
        )
        print(
            f"Confidence : {confidence}"
        )

        result["updated"] = False

        return result

    media_id = item.get("id")

    updated = update_attachment(
        media_id,
        result,
    )

    result["updated"] = updated

    return result