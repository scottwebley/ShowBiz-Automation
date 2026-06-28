import os
import sys
import mimetypes
import requests
from requests.auth import HTTPBasicAuth

# --------------------------------------------------
# Allow importing config.py from the project root
# --------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

# --------------------------------------------------

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}


def upload_image(image_path):
    """
    Upload an image to the WordPress Media Library.

    Returns:
        media_id (int) if successful
        None if failed
    """

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    filename = os.path.basename(image_path)

    mime_type = mimetypes.guess_type(filename)[0]

    if mime_type is None:
        mime_type = "image/png"

    with open(image_path, "rb") as f:
        image_data = f.read()

    headers = HEADERS.copy()

    headers["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    headers["Content-Type"] = mime_type

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD
        ),
        headers=headers,
        data=image_data,
        timeout=60
    )

    print("Upload Status:", response.status_code)

    if response.status_code not in (200, 201):
        print(response.text)
        return None

    media = response.json()

    print(f"✓ Uploaded Media ID: {media['id']}")

    return media["id"]


if __name__ == "__main__":

    image = "images/christopher-nolan-announces-new-epic-film.png"

    media_id = upload_image(image)

    print()

    print("Returned Media ID:", media_id)