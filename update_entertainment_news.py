import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

PAGE_ID = 2129

headers = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

with open("content/entertainment_news.html", "r", encoding="utf-8") as f:
    content = f.read()

data = {
    "content": content
}

response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
    headers=headers,
    json=data
)

print("Status:", response.status_code)

if response.status_code == 200:
    print("SUCCESS")
    print("Entertainment News updated.")
else:
    print("FAILED")
    print(response.text)