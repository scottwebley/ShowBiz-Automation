import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

headers = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

response = requests.get(
    f"{WP_URL}/wp-json/wp/v2/users/me",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
    headers=headers
)

print("Status:", response.status_code)
print(response.text)