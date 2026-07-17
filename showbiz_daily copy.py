# ============================================
# SHOWBIZ DAILY AUTOMATION ENGINE
# Version 3.3
# ============================================

import subprocess
from datetime import datetime


def banner():
    print()
    print("=" * 50)
    print("        SHOWBIZ DAILY AUTOMATION")
    print("=" * 50)
    print()


def run_step(name, script):
    print(f"\n▶ {name}")

    # Run guide modules as Python modules
    if script.startswith("engine/guides/") and script.endswith(".py"):

        module = script[:-3].replace("/", ".")

        result = subprocess.run(
            ["python3", "-m", module]
        )

    # Run top-level scripts normally
    else:

        result = subprocess.run(
            ["python3", script]
        )

    if result.returncode == 0:
        print(f"✓ {name} completed")
    else:
        print(f"✗ {name} failed")
        raise SystemExit(1)


def main():
    banner()

    today = datetime.now().strftime("%B %d, %Y")
    print(f"Today's Date: {today}")

    print("\nStarting automation...\n")

    # -----------------------------------------
    # Publish today's Top Story
    # -----------------------------------------

    run_step(
        "Publish Top Story",
        "newsroom.py",
    )

    # -----------------------------------------
    # Update Winners & Losers page
    # -----------------------------------------

    run_step(
        "Update Winners & Losers",
        "newsroom_daily.py",
    )

    # -----------------------------------------
    # Update Homepage Winners teaser
    # -----------------------------------------

    run_step(
        "Update Homepage Winners",
        "upload_daily_report.py",
    )

    # -----------------------------------------
    # Publish Featured Entertainer of the Week
    # -----------------------------------------

    run_step(
        "Publish Featured Entertainer",
        "publish_featured_entertainer.py",
    )

    # -----------------------------------------
    # Update Homepage Featured Entertainer
    # -----------------------------------------

    run_step(
        "Update Homepage Featured Entertainer",
        "update_featured_entertainer_homepage.py",
    )

    # =========================================
    # SHOWBIZ GUIDES
    # =========================================

    run_step(
        "Update Movies Guide",
        "engine/guides/weekly_movies.py",
    )

    run_step(
        "Update TV Guide",
        "engine/guides/weekly_tv.py",
    )

    run_step(
        "Update Streaming Guide",
        "engine/guides/weekly_streaming.py",
    )

    run_step(
        "Update Concert Guide",
        "engine/guides/weekly_concerts.py",
    )

    print()
    print("===================================")
    print("✓ SHOWBIZ DAILY COMPLETE")
    print("===================================")


if __name__ == "__main__":
    main()