# ============================================
# SHOWBIZ DAILY AUTOMATION ENGINE
# Version 2.0
# ============================================
from engine.homepage import build_homepage

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
        exit()


def main():
    banner()

    today = datetime.now().strftime("%B %d, %Y")
    print(f"Today's Date: {today}")

    print("\nStarting automation...\n")

    homepage = build_homepage()

    run_step("Generate Content", "generate_content.py")

    print("\n===================================")
    print("✓ ALL TASKS COMPLETED SUCCESSFULLY")
    print("===================================")

if __name__ == "__main__":
    main()