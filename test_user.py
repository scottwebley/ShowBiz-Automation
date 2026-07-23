import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

response = requests.get(
    f"{WP_URL}/wp-json/wp/v2/users/me",
    auth=HTTPBasicAuth(
        WP_USERNAME,
        WP_APP_PASSWORD,
    ),
    timeout=30,
)

print("=" * 60)
print("STATUS:", response.status_code)
print("=" * 60)

try:
    user = response.json()

    print("ID       :", user.get("id"))
    print("Username :", user.get("slug"))
    print("Name     :", user.get("name"))
    print("Roles    :", user.get("roles"))

except Exception:
    print(response.text)