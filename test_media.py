import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

r = requests.get(
    f"{WP_URL}/wp-json/wp/v2/media/41012",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
)

print("Status:", r.status_code)
print(r.text)