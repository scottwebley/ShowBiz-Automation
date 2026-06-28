# ============================================
# SHOWBIZ DAILY AUTOMATION ENGINE
# Version 3.1
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

    result = subprocess.run(["python3", script])

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

    run_step("Publish Top Story", "newsroom.py")

    # -----------------------------------------
    # Update Winners & Losers page
    # -----------------------------------------

    run_step("Update Winners & Losers", "newsroom_daily.py")

    # -----------------------------------------
    # Update Homepage Winners teaser
    # -----------------------------------------

    run_step("Update Homepage Winners", "upload_daily_report.py")

    print("\n===================================")
    print("✓ SHOWBIZ DAILY COMPLETE")
    print("===================================")


if __name__ == "__main__":
    main()