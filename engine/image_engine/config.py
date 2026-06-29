"""
===========================================
ShowBiz Media Engine
config.py
===========================================

Configuration for external services.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# WordPress
# --------------------------------------------------

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# --------------------------------------------------
# OpenAI
# --------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------
# NewsAPI
# --------------------------------------------------

NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")

# --------------------------------------------------
# TMDb
# --------------------------------------------------

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original"


def verify():

    print()
    print("=" * 60)
    print("SHOWBIZ CONFIG")
    print("=" * 60)

    print(f"WordPress URL      : {'✓' if WP_URL else '✗'}")
    print(f"WordPress Username : {'✓' if WP_USERNAME else '✗'}")
    print(f"WordPress Password : {'✓' if WP_APP_PASSWORD else '✗'}")
    print(f"OpenAI API Key     : {'✓' if OPENAI_API_KEY else '✗'}")
    print(f"NewsAPI Key        : {'✓' if NEWSAPI_API_KEY else '✗'}")
    print(f"TMDb API Key       : {'✓' if TMDB_API_KEY else '✗'}")


if __name__ == "__main__":
    verify()