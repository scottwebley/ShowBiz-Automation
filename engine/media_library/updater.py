"""
===========================================
ShowBiz Media Library Updater
Version 1.1
===========================================

Purpose:
    Update WordPress attachment metadata
    after AI enrichment.

Author:
    ShowBiz Automation
"""

import requests

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)


def update_attachment(media_id, metadata):
    """
    Update one WordPress attachment.

    Args:
        media_id (int)
        metadata (dict)

    Returns:
        bool
    """

    url = (
        f"{WP_URL}"
        f"/wp-json/wp/v2/media/{media_id}"
    )

    payload = {
        "title": metadata.get("title", ""),
        "alt_text": metadata.get("alt", ""),
        "caption": metadata.get("caption", ""),
    }

    response = requests.post(
        url,
        auth=(
            WP_USERNAME,
            WP_APP_PASSWORD,
        ),
        json=payload,
        timeout=30,
    )

    if response.status_code not in (200, 201):

        print()
        print("Media update failed.")
        print(
            f"Status : {response.status_code}"
        )
        print(response.text)

        return False

    print()
    print("Media updated successfully.")
    print(f"Media ID : {media_id}")

    return True