from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

WP_URL = os.getenv("WP_URL", "https://showbiz.com")

WP_USERNAME = os.getenv("WP_USERNAME", "admin")

WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")