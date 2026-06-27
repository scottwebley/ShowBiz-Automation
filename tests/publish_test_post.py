import requests
from requests.auth import HTTPBasicAuth
from config import WP_URL, WP_USERNAME, WP_APP_PASSWORD

headers = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

data = {
    "title": "ShowBiz Automation Test",
    "content": "<p>This post was published automatically from Python.</p>",
    "status": "draft"
}

response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
    headers=headers,
    json=data
)

print("Status:", response.status_code)

if response.status_code == 201:
    post = response.json()

    print("\nSUCCESS")
    print("Post ID:", post["id"])
    print("Title:", post["title"]["rendered"])
    print("Link:", post["link"])

else:
    print("\nFAILED")
    print(response.text)