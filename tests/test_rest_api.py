import requests

url = "https://showbiz.com/wp-json/wp/v2/"

headers = {
    "User-Agent": "ShowBiz-Automation/1.0"
}

response = requests.get(
    url,
    headers=headers
)

print("Status:", response.status_code)
print(response.text[:500])