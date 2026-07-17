# ============================================
# SHOWBIZ DAILY AUTOMATION ENGINE
# Version 4.0
# ============================================

import subprocess
import sys
import time
import traceback
from datetime import datetime

from engine.scheduler import (
    should_run_daily,
    should_run_weekly,
)


LOG_FILE = "showbiz_scheduler.log"

RUN_RESULTS = []


def log(message=""):
    """
    Write to console and scheduler log.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    line = f"[{timestamp}] {message}"

    print(line)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8",
    ) as logfile:

        logfile.write(
            line + "\n"
        )


def banner():

    log()
    log("=" * 60)
    log("SHOWBIZ DAILY AUTOMATION")
    log("=" * 60)
    log(
        f"Started: {datetime.now().strftime('%B %d, %Y %I:%M:%S %p')}"
    )
    log()


def run_step(
    name,
    script,
):
    """
    Run one automation step.
    Continue even if it fails.
    """

    log("-" * 60)
    log(f"Starting: {name}")

    start = time.time()

    try:

        #
        # Run guide modules.
        #
        if (
            script.startswith("engine/guides/")
            and script.endswith(".py")
        ):

            module = (
                script[:-3]
                .replace("/", ".")
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    module,
                ]
            )

        #
        # Run normal scripts.
        #
        else:

            result = subprocess.run(
                [
                    sys.executable,
                    script,
                ]
            )

        elapsed = (
            time.time() - start
        )

        if result.returncode == 0:

            RUN_RESULTS.append(
                (
                    name,
                    True,
                    elapsed,
                )
            )

            log(
                f"SUCCESS: {name} "
                f"({elapsed:.1f}s)"
            )

            return True

        RUN_RESULTS.append(
            (
                name,
                False,
                elapsed,
            )
        )

        log(
            f"FAILED: {name} "
            f"(exit code {result.returncode}) "
            f"({elapsed:.1f}s)"
        )

        return False

    except Exception:

        elapsed = (
            time.time() - start
        )

        RUN_RESULTS.append(
            (
                name,
                False,
                elapsed,
            )
        )

        log(
            f"EXCEPTION: {name}"
        )

        log(
            traceback.format_exc()
        )

        return False
def main():
    banner()

    today = datetime.now().strftime("%B %d, %Y")
    print(f"Today's Date: {today}")

    print("\nStarting automation...\n")

    # -----------------------------------------
    # Always publish today's Top Story
    # -----------------------------------------

    run_step(
        "Publish Top Story",
        "newsroom.py",
    )

    # -----------------------------------------
    # First run of the day
    # -----------------------------------------

    if should_run_daily():

        print("\nRunning daily automation...\n")

        run_step(
            "Update Winners & Losers",
            "newsroom_daily.py",
        )

        run_step(
            "Update Homepage Winners",
            "upload_daily_report.py",
        )

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

    else:
        print("\n✓ Daily automation already completed today.")

    # -----------------------------------------
    # First run of the week
    # -----------------------------------------

    if should_run_weekly():

        print("\nRunning weekly automation...\n")

        run_step(
            "Publish Featured Entertainer",
            "publish_featured_entertainer.py",
        )

        run_step(
            "Update Homepage Featured Entertainer",
            "update_featured_entertainer_homepage.py",
        )

    else:
        print("\n✓ Weekly automation already completed this week.")

    print()
    print("===================================")
    print("✓ SHOWBIZ DAILY COMPLETE")
    print("===================================")


if __name__ == "__main__":
    main()   
        