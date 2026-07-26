from eventregistry import *
from dotenv import load_dotenv
import os
from pprint import pprint

from engine.categorizer import categorize
from engine.editorial_filter import keep_story
from engine.news_cache import save_news
from engine.scorer import score_story
from engine.duplicate_detector import remove_duplicates
from engine.editor import editorial_decision

load_dotenv()

API_KEY = os.getenv("NEWSAPI_AI_KEY")

er = EventRegistry(apiKey=API_KEY)


def get_top_stories(max_items=50):
    """
    Fetch, filter, categorize, score,
    remove duplicates, perform editorial review,
    and cache today's entertainment news.
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
            "awards",
        ]),
        lang="eng",
    )

    stories = []
    seen = set()

    try:

        print("Downloading stories...")

        debug_printed = False

        for article in query.execQuery(
            er,
            sortBy="date",
            maxItems=max_items * 3,
        ):

            #
            # DEBUG - print the first raw article returned
            #
            if not debug_printed:
                print("\n" + "=" * 80)
                print("RAW EVENT REGISTRY ARTICLE")
                print("=" * 80)

                print("\nAVAILABLE KEYS:\n")
                pprint(sorted(article.keys()))

                print("\nTITLE:\n")
                print(article.get("title"))

                print("\nBODY LENGTH:")
                print(len(article.get("body", "") or ""))

                print("\nBODY (first 1000 chars):\n")
                print((article.get("body", "") or "")[:1000])

                print("\nFULL RAW ARTICLE:\n")
                pprint(article)

                print("=" * 80 + "\n")

                debug_printed = True

            story = {
                "headline": article.get("title", "").strip(),
                "summary": article.get("body", "")[:500],
                "body": article.get("body", ""),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("title", ""),
                "published": article.get("dateTime", ""),
            }

            if not story["headline"]:
                continue

            #
            # Editorial filter
            #

            if not keep_story(story):
                continue

            #
            # Remove exact duplicate headlines
            #

            key = story["headline"].lower()

            if key in seen:
                continue

            seen.add(key)

            #
            # Categorize
            #

            story["category"] = categorize(story)

            #
            # Score
            #

            story["score"] = score_story(story)

            stories.append(story)

    except Exception as e:

        print("\nERROR")
        print(e)

    #
    # Remove duplicate stories
    #

    stories = remove_duplicates(stories)

    #
    # Final editorial approval
    #

    approved = []

    for story in stories:

        decision, reason = editorial_decision(story)

        story["editor_decision"] = decision
        story["editor_reason"] = reason

        if decision == "PUBLISH":
            approved.append(story)

    #
    # Highest score first
    #

    approved.sort(
        key=lambda s: s["score"],
        reverse=True
    )

    approved = approved[:max_items]

    print("\nHEADLINES BEFORE CACHE")
    print("=" * 60)

    for i, story in enumerate(approved, 1):
        print(f"{i:02d}. {story.get('headline')}")

    # Stop here so we can inspect the headlines.

    print(f"✓ Cached {len(approved)} stories.")

    return approved


if __name__ == "__main__":

    stories = get_top_stories()

    print()
    print("=" * 70)
    print("TODAY'S STORIES")
    print("=" * 70)

    for story in stories:

        print(
            f"[{story['score']:>3}] "
            f"[{story['category']}] "
            f"{story['headline']}"
        )