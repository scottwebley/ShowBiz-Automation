"""
===========================================
ShowBiz Local Story Selector
Version 2.0
===========================================

Purpose:
    Offline fallback story selector.

This selector NEVER calls OpenAI.

It is used only when both the Homepage
Ranker and AI Story Selector fail.

Returns the ORIGINAL story object so that
all metadata is preserved.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


# ---------------------------------------------------------
# Editorial scoring
#
# Higher score = better candidate.
#
# Category is intentionally LOW priority.
# Story quality should dominate.
# ---------------------------------------------------------

CATEGORY_PRIORITY = {
    "Entertainment Industry": 25,
    "Movies": 24,
    "Movie": 24,
    "Television": 23,
    "TV": 23,
    "Celebrity": 22,
    "Awards": 21,
    "Music": 20,
    "Streaming": 12,
    "Style": 8,
}


def _contains(text, phrases):
    text = text.lower()
    return any(p in text for p in phrases)


def _headline(story):
    return (
        story.get("headline")
        or story.get("title")
        or ""
    ).strip()


def _category_score(story):
    category = story.get("category", "")
    return CATEGORY_PRIORITY.get(category, 10)


def _editorial_story_score(story):
    """
    Main editorial scoring.

    This is designed to imitate a human
    entertainment editor.

    Story quality matters far more than
    category.
    """

    headline = _headline(story)
    text = headline.lower()

    score = 0

    #
    # Reject garbage.
    #

    if not headline:
        return -100000

    #
    # Hard penalties
    #

    hard_penalties = [
        "happy ending massage",
        "massage",
        "porn",
        "pornhub",
        "onlyfans",
        "sex",
        "sexual",
        "adult",
        "escort",
        "dating",
        "hookup",
        "nude",
        "nsfw",
    ]

    if _contains(text, hard_penalties):
        score -= 1000

    #
    # SEO / evergreen penalties
    #

    evergreen = [
        "best ",
        "top 10",
        "top ten",
        "watch guide",
        "watching guide",
        "how to",
        "everything streaming",
        "streaming guide",
        "where to watch",
        "what to watch",
        "shopping",
        "buy ",
        "gift guide",
        "ranking every",
        "ranked",
        "explained",
        "review:",
        "reviews:",
        "list of",
    ]

    if _contains(text, evergreen):
        score -= 250

    #
    # Streaming recommendation penalties
    #

    streaming_penalties = [
        "streaming",
        "binge",
        "binge-watch",
        "watch now",
        "must watch",
        "must-watch",
        "available now",
        "now streaming",
    ]

    if _contains(text, streaming_penalties):
        score -= 120

    #
    # Major entertainment news
    #

    strong_news = [
        "breaking",
        "announces",
        "announced",
        "announcement",
        "trailer",
        "teaser",
        "premiere",
        "release date",
        "cast",
        "casting",
        "joins",
        "starring",
        "renewed",
        "renewal",
        "cancelled",
        "canceled",
        "box office",
        "wins",
        "winner",
        "award",
        "emmy",
        "oscar",
        "grammy",
        "golden globe",
        "tour",
        "concert",
        "festival",
        "obituary",
        "dies",
        "dead",
        "acquires",
        "acquisition",
        "merger",
        "deal",
        "lawsuit",
    ]

    for phrase in strong_news:
        if phrase in text:
            score += 120

    #
    # Major studios
    #

    studios = [
        "disney",
        "marvel",
        "pixar",
        "dc",
        "warner bros",
        "warner",
        "universal",
        "paramount",
        "sony",
        "lionsgate",
        "netflix",
        "netflix original",
        "hbo",
        "max",
        "apple tv",
        "amazon mgm",
        "amazon studios",
        "a24",
    ]

    for phrase in studios:
        if phrase in text:
            score += 90

    #
    # Industry significance
    #

    industry = [
        "ceo",
        "studio",
        "executive",
        "media",
        "industry",
        "earnings",
        "revenue",
        "shares",
        "ipo",
        "streamer",
        "broadcast",
    ]

    for phrase in industry:
        if phrase in text:
            score += 45

    #
    # Longer specific headlines
    #

    score += min(len(headline) // 5, 20)

    return score


def _story_score(story):
    """
    Deterministic ranking tuple.

    Priority:

    1. Story quality
    2. Editorial score
    3. Feed score
    4. Category
    5. Headline length
    """

    headline = _headline(story)

    return (
        _editorial_story_score(story),
        story.get("editorial_score", 0),
        story.get("score", 0),
        _category_score(story),
        len(headline),
        headline.lower(),
    )


def select_local_story(stories):
    """
    Select the best story using only
    local information.

    Never calls OpenAI.
    """

    if not stories:
        return None

    valid = []

    for story in stories:

        headline = _headline(story)

        if not headline:
            continue

        valid.append(story)

    if not valid:
        return stories[0]

    ranked = sorted(
        valid,
        key=_story_score,
        reverse=True,
    )

    print()
    print("=" * 50)
    print("LOCAL STORY SELECTOR V2")
    print("=" * 50)
    print()

    print("Top Candidates:")

    for i, story in enumerate(ranked[:10], 1):

        print(
            f"{i:2d}. "
            f"[{story.get('category','')}] "
            f"quality={_editorial_story_score(story):4d} "
            f"editorial={story.get('editorial_score',0):3} "
            f"feed={story.get('score',0):3} :: "
            f"{_headline(story)}"
        )

    print()

    winner = ranked[0]

    print("✓ Local Story Selector chose:")
    print(f"  {_headline(winner)}")

    return winner


#
# Test
#

if __name__ == "__main__":

    sample = [

        {
            "headline": "I'm A Middle-Aged Woman. This Is What Happened When I Got A Happy Ending Massage.",
            "category": "Streaming",
            "score": 100,
        },

        {
            "headline": "Disney Announces New Pixar Film Release Date",
            "category": "Movies",
            "score": 61,
        },

        {
            "headline": "Warner Bros. Reveals First Trailer For Major DC Movie",
            "category": "Movies",
            "score": 59,
        },
    ]

    winner = select_local_story(sample)

    print()
    print("Winner:")
    print(_headline(winner))