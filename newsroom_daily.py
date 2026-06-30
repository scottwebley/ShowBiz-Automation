import json
from datetime import datetime
from pathlib import Path

from engine.ai_news import get_top_stories
from engine.daily_report import generate_daily_report
from engine.daily_report_writer import write_daily_report
from engine.page_updater import update_page

# WordPress Page ID
DAILY_REPORT_PAGE_ID = 31190

# Local JSON used by homepage/plugin
REPORT_JSON = Path("data/daily_report.json")


def save_daily_report(report):
    """
    Save a compact JSON version of today's report.
    """

    REPORT_JSON.parent.mkdir(exist_ok=True)

    data = {
        "date": report.get("date", ""),
        "winner": report["winner"]["name"],
        "winner_reason": report["winner"]["reason"],
        "loser": report["loser"]["name"],
        "loser_reason": report["loser"]["reason"],
        "url": "https://showbiz.com/entertainment-winners-losers/"
    }

    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("✓ daily_report.json updated")


def already_published_today():
    """
    Return True if today's Winners & Losers
    has already been published.
    """

    if not REPORT_JSON.exists():
        return False

    try:

        with open(REPORT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        today = datetime.now().strftime("%B %d, %Y").replace(" 0", " ")

        return data.get("date", "") == today

    except Exception:
        return False


def main():

    print("\n==============================")
    print(" SHOWBIZ DAILY REPORT")
    print("==============================\n")

    # ------------------------------------------------
    # Skip if today's Winners & Losers already exists
    # ------------------------------------------------

    if already_published_today():

        print("Today's Winners & Losers has already been published.")
        print("Skipping update.\n")

        return

    print("STEP 1: Downloading today's entertainment news...")

    stories = get_top_stories()

    if not stories:
        print("No stories found.")
        return

    print(f"✓ {len(stories)} stories downloaded.\n")

    print("STEP 2: AI editorial analysis...")

    report = generate_daily_report(stories)

    print("✓ Daily report generated.\n")

    print("STEP 3: Writing HTML article...")

    article = write_daily_report(report)

    print("✓ HTML article created.\n")

    print("STEP 4: Updating Winners & Losers page...")

    page = update_page(
        DAILY_REPORT_PAGE_ID,
        article
    )

    if not page:
        print("\nPage update failed.\n")
        return

    # Only save today's report AFTER a successful
    # WordPress update.

    save_daily_report(report)

    print("\n==============================")
    print(" DAILY REPORT UPDATED")
    print("==============================")
    print(f"Page ID : {page['id']}")
    print(f"Title   : {page['title']['rendered']}")
    print(f"URL     : {page['link']}")
    print("==============================\n")


if __name__ == "__main__":
    main()