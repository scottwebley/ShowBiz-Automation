import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

r = requests.get(
    f"{WP_URL}/wp-json/wp/v2/types/post",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
)

print("Status:", r.status_code)

try:
    data = r.json()
    print(data.get("supports"))
except Exception:
    print(r.text)