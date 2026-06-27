import sys
import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

PAGE_ID = sys.argv[1]
CONTENT_FILE = sys.argv[2]

with open(CONTENT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
    headers={
        "User-Agent": "ShowBiz-Automation/1.0"
    },
    json={
        "content": content
    }
)

print("Status:", response.status_code)

if response.status_code == 200:
    print("SUCCESS")
else:
    print(response.text)