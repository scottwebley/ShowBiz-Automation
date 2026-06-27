from engine.news_fetcher import fetch_news


def select_story():
    """
    Return the most important entertainment story.
    This is version 1. Later we'll score all stories.
    """

    stories = fetch_news()

    if not stories:
        raise Exception("No entertainment stories were returned.")

    return stories[0]