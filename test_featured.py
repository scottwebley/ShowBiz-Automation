import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

POST_ID = 54342        # Existing post
MEDIA_ID = 54385      # Existing media

headers = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

auth = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)

print("=" * 60)
print("SETTING FEATURED IMAGE")
print("=" * 60)

r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
    auth=auth,
    headers=headers,
    json={
        "featured_media": MEDIA_ID
    },
    timeout=60,
)

print("POST Status:", r.status_code)

try:
    print("POST featured_media:", r.json().get("featured_media"))
except Exception:
    print(r.text)

print()

r = requests.get(
    f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
    auth=auth,
    headers=headers,
    timeout=60,
)

print("GET Status:", r.status_code)

try:
    print("GET featured_media:", r.json().get("featured_media"))
except Exception:
    print(r.text)