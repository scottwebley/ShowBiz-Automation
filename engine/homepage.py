from datetime import datetime

import json
from pathlib import Path

from engine.ai_news import get_top_stories

def build_homepage():
    """Generate homepage information."""

    today = datetime.now().strftime("%B %d, %Y")

    print("Building homepage...")

    homepage = {
    "date": today,

    "hero_story": {
        "headline": "Today's Biggest Entertainment Story",
        "summary": "Lead entertainment story of the day.",
        "category": "Entertainment",
        "image_search": "Hollywood red carpet"
    },

    "top_stories": get_top_stories()
}
    
    output_file = Path("data/homepage.json")

    with open(output_file, "w") as f:
        json.dump(homepage, f, indent=4)

    print("✓ Homepage JSON saved")
    
    return homepage
