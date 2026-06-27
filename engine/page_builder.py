import json
from pathlib import Path

from engine.template import page_header, page_footer


def load_news():
    with open("data/daily_news.json", "r") as f:
        return json.load(f)


def build_home_page(news):
    html = page_header("Today's Entertainment News")

    html += f"""
<p><strong>Generated:</strong> {news["generated_at"]}</p>
"""

    for story in news["stories"][:5]:
        html += f"""
<div class="story">
    <h2>{story["headline"]}</h2>

    <p>{story["summary"]}</p>

    <p><strong>Category:</strong> {story["category"]}</p>
</div>
"""

    html += page_footer()

    Path("content").mkdir(exist_ok=True)

    with open("content/homepage.html", "w") as f:
        f.write(html)


def build_entertainment_page(news):
    html = page_header("Entertainment News")

    for story in news["stories"]:
        html += f"""
<div class="story">
    <h2>{story["headline"]}</h2>

    <p>{story["summary"]}</p>

    <p><strong>Category:</strong> {story["category"]}</p>
</div>
"""

    html += page_footer()

    Path("content").mkdir(exist_ok=True)

    with open("content/entertainment_news.html", "w") as f:
        f.write(html)


def build_all_pages():
    news = load_news()

    build_home_page(news)
    build_entertainment_page(news)

    print("✓ Pages built")