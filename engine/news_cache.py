"""
===========================================
ShowBiz News Cache
Version 1.0
===========================================

Caches today's downloaded stories so every
editorial component uses the same data.
"""

import json
from pathlib import Path

CACHE_DIR = Path("data")
CACHE_DIR.mkdir(exist_ok=True)

CACHE_FILE = CACHE_DIR / "todays_news.json"


def save_news(stories):
    """
    Save today's stories.
    """

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            stories,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"✓ Cached {len(stories)} stories.")


def load_news():
    """
    Load today's stories.
    """

    if not CACHE_FILE.exists():
        return []

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def cache_exists():

    return CACHE_FILE.exists()


if __name__ == "__main__":

    print(load_news())