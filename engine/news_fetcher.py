import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSAPI_AI_KEY")

API_URL = "https://eventregistry.org/api/v1/article/getArticles"


def fetch_news():
    """
    Fetch today's entertainment news from NewsAPI.ai (Event Registry).
    Returns a list of stories in the format expected by the newsroom.
    """

    if not API_KEY:
        raise Exception("NEWSAPI_AI_KEY not found in .env")

    payload = {
        "apiKey": API_KEY,
        "query": {
            "$query": {
                "$and": [
                    {
                        "categoryUri": "dmoz/Arts/Entertainment"
                    },
                    {
                        "lang": "eng"
                    }
                ]
            }
        },
        "resultType": "articles",
        "articlesSortBy": "date",
        "articlesCount": 10,
        "includeArticleBody": False
    }

    response = requests.post(API_URL, json=payload, timeout=30)

    response.raise_for_status()

    data = response.json()

    results = []

    for article in data.get("articles", {}).get("results", []):

        results.append({
            "headline": article.get("title", ""),
            "summary": article.get("body", "")[:400] if article.get("body") else "",
            "category": "Entertainment",
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("title", "")
        })

    return results