#!/usr/bin/env python3
"""
test_featured_image.py

Standalone WordPress Featured Image Test

Creates a temporary post using an existing Media Library image,
then verifies whether WordPress actually attached the featured image.

Usage:
    python3 test_featured_image.py
"""

import json
import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

# -------------------------------------------------------
# CHANGE THIS IF YOU WANT TO TEST ANOTHER MEDIA ITEM
# -------------------------------------------------------

MEDIA_ID = 41396

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

AUTH = HTTPBasicAuth(
    WP_USERNAME,
    WP_APP_PASSWORD
)


def print_json(title, obj):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(json.dumps(obj, indent=4))


# -------------------------------------------------------
# STEP 1
# Create Post
# -------------------------------------------------------

print("\nCreating test post...")

payload = {
    "title": "Featured Image Test",
    "content": "<p>Testing featured image attachment.</p>",
    "status": "draft",
    "featured_media": MEDIA_ID,
}

response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    auth=AUTH,
    headers=HEADERS,
    json=payload,
    timeout=60,
)

print("Create Status :", response.status_code)

try:
    create_json = response.json()
except Exception:
    print(response.text)
    raise SystemExit

print_json("CREATE RESPONSE", create_json)

if response.status_code not in (200, 201):
    raise SystemExit("Create failed.")

post_id = create_json["id"]

# -------------------------------------------------------
# STEP 2
# Read Post Back
# -------------------------------------------------------

print("\nReading post back...")

response = requests.get(
    f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
    auth=AUTH,
    headers=HEADERS,
    timeout=60,
)

print("Read Status :", response.status_code)

read_json = response.json()

print_json("READ RESPONSE", read_json)

print("\nfeatured_media =", read_json.get("featured_media"))

# -------------------------------------------------------
# STEP 3
# Try Updating Featured Image
# -------------------------------------------------------

print("\nUpdating featured image...")

response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
    auth=AUTH,
    headers=HEADERS,
    json={
        "featured_media": MEDIA_ID
    },
    timeout=60,
)

print("Update Status :", response.status_code)

update_json = response.json()

print_json("UPDATE RESPONSE", update_json)

# -------------------------------------------------------
# STEP 4
# Read Again
# -------------------------------------------------------

print("\nReading updated post...")

response = requests.get(
    f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
    auth=AUTH,
    headers=HEADERS,
    timeout=60,
)

final_json = response.json()

print_json("FINAL RESPONSE", final_json)

print("\nFINAL featured_media =", final_json.get("featured_media"))

# -------------------------------------------------------
# STEP 5
# Cleanup
# -------------------------------------------------------

print("\nDeleting test post...")

response = requests.delete(
    f"{WP_URL}/wp-json/wp/v2/posts/{post_id}?force=true",
    auth=AUTH,
    headers=HEADERS,
    timeout=60,
)

print("Delete Status :", response.status_code)

print("\nDone.")