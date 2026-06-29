"""
===========================================
ShowBiz Story Categorizer
Version 2.1
===========================================

Weighted editorial categorization using
whole-word regex matching.
"""

import re


CATEGORY_RULES = {

    "Entertainment Industry": {
        "comcast": 10,
        "nbcuniversal": 10,
        "disney": 8,
        "warner bros": 8,
        "warner": 8,
        "netflix": 8,
        "paramount": 8,
        "studio": 6,
        "executive": 6,
        "ceo": 6,
        "merger": 8,
        "acquisition": 8,
        "spin-off": 8,
        "spinoff": 8,
        "sky": 5,
    },

    "Movies": {
        "movie": 5,
        "film": 5,
        "box office": 8,
        "cinema": 5,
        "trailer": 5,
        "marvel": 6,
        "dc": 6,
        "pixar": 6,
        "universal pictures": 6,
        "paramount pictures": 6,
    },

    "Television": {
        "television": 5,
        "tv": 5,
        "series": 5,
        "season": 5,
        "episode": 5,
        "sitcom": 5,
        "drama": 4,
        "nbc": 3,
        "abc": 3,
        "cbs": 3,
        "fox": 3,
    },

    "Streaming": {
        "streaming": 8,
        "netflix": 6,
        "hulu": 6,
        "max": 6,
        "prime video": 6,
        "apple tv": 6,
        "disney+": 6,
        "peacock": 6,
        "paramount+": 6,
    },

    "Music": {
        "music": 5,
        "album": 5,
        "single": 5,
        "tour": 5,
        "concert": 5,
        "billboard": 6,
        "grammy": 6,
        "spotify": 5,
    },

    "Celebrity": {
        "celebrity": 5,
        "actor": 5,
        "actress": 5,
        "star": 3,
        "hollywood": 4,
    },

    "Gaming": {
        "gaming": 5,
        "video game": 6,
        "playstation": 6,
        "xbox": 6,
        "nintendo": 6,
        "steam": 5,
    },

    "Broadway": {
        "broadway": 8,
        "musical": 6,
        "theatre": 5,
        "theater": 5,
        "stage": 4,
        "play": 2,
    },

    "Awards": {
        "oscar": 8,
        "emmy": 8,
        "grammy": 8,
        "golden globe": 8,
        "award": 5,
        "festival": 4,
    },
}


def keyword_found(keyword, text):
    """
    Match complete words or phrases only.
    """

    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    ) is not None


def categorize_story(story):
    """
    Return the best entertainment category.
    """

    text = (
        story.get("headline", "")
        + " "
        + story.get("summary", "")
    )

    best_category = "Entertainment"
    best_score = 0

    for category, keywords in CATEGORY_RULES.items():

        score = 0

        for keyword, weight in keywords.items():

            if keyword_found(keyword, text):

                score += weight

        if score > best_score:

            best_score = score
            best_category = category

    return best_category


#
# Backward compatibility
#
def categorize(story):
    return categorize_story(story)


if __name__ == "__main__":

    tests = [

        {
            "headline":
            "Comcast Plans Tax-Free Spin-Off Of NBCUniversal And Sky",
            "summary":
            "Corporate restructuring."
        },

        {
            "headline":
            "Marvel Releases New Fantastic Four Trailer",
            "summary":
            ""
        },

        {
            "headline":
            "Taylor Swift Announces World Tour",
            "summary":
            ""
        },

        {
            "headline":
            "Netflix Renews Hit Series For Season 3",
            "summary":
            ""
        },

    ]

    print("=" * 60)
    print("SHOWBIZ STORY CATEGORIZER 2.1")
    print("=" * 60)

    for story in tests:

        print()
        print(story["headline"])
        print("→", categorize_story(story))