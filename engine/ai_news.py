from eventregistry import *
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("NEWSAPI_AI_KEY")

er = EventRegistry(apiKey=API_KEY)


def get_top_stories(max_items=50):
    """
    Fetch the latest entertainment-related news.
    """

    query = QueryArticlesIter(
        keywords=QueryItems.OR([
            "movies",
            "television",
            "streaming",
            "Netflix",
            "music",
            "celebrity",
            "Hollywood",
            "gaming",
            "Broadway",
            "awards"
        ]),
        lang="eng"
    )

    stories = []

    try:

        for article in query.execQuery(
            er,
            sortBy="date",
            maxItems=max_items
        ):

            stories.append({
                "headline": article.get("title", ""),
                "summary": article.get("body", "")[:500],
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("title", ""),
                "published": article.get("dateTime", "")
            })

    except Exception as e:
        print("\nERROR")
        print(e)

    return stories


if __name__ == "__main__":

    stories = get_top_stories()

    print(f"\nFound {len(stories)} stories\n")

    for story in stories:
        print(story["headline"])