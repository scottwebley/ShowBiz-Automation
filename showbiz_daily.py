# ============================================
# SHOWBIZ DAILY AUTOMATION ENGINE
# Version 3.0
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

    run_step("Publish Top Story", "newsroom.py")

    run_step("Update Winners & Losers", "newsroom_daily.py")

    print("\n===================================")
    print("✓ SHOWBIZ DAILY COMPLETE")
    print("===================================")


if __name__ == "__main__":
    main()