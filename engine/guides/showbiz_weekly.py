"""
===========================================
ShowBiz Weekly
Version 1.0
===========================================

Runs all weekly ShowBiz guides.
"""

from engine.guides.weekly_movies import main as movies


def main():

    print()
    print("========================================")
    print("SHOWBIZ WEEKLY")
    print("========================================")

    movies()

    print()
    print("Weekly update complete.")


if __name__ == "__main__":
    main()