import json
import requests
from requests.auth import HTTPBasicAuth

from config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
)

HEADERS = {
    "User-Agent": "ShowBiz-Automation/1.0"
}


def upload_daily_report(report):
    """
    Upload today's Winners & Losers report to WordPress.
    """

    response = requests.post(
        f"{WP_URL}/wp-json/showbiz/v1/daily-report",
        auth=HTTPBasicAuth(
            WP_USERNAME,
            WP_APP_PASSWORD
        ),
        headers=HEADERS,
        json=report,
        timeout=60
    )

    print("\nREST Status:", response.status_code)
    print(response.text)

    return response.status_code in (200, 201)


def upload_daily_report_from_file():
    """
    Read data/daily_report.json and upload it.
    """

    with open("data/daily_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    return upload_daily_report(report)


if __name__ == "__main__":

    success = upload_daily_report_from_file()

    if success:
        print("\n✅ Daily report uploaded successfully.")
    else:
        print("\n❌ Upload failed.")