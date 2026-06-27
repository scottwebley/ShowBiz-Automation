import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

wp_url = os.getenv("WP_URL")
wp_user = os.getenv("WP_USERNAME")
wp_password = os.getenv("WP_APP_PASSWORD")

response = requests.get(
    f"{wp_url}/wp-json/wp/v2/users/me",
    auth=HTTPBasicAuth(wp_user, wp_password),
    headers={"User-Agent": "Mozilla/5.0"}
)

print("Status:", response.status_code)
print(response.text[:500])