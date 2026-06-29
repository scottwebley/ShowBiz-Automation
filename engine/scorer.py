"""
===========================================
ShowBiz Story Scorer
Version 2.1
===========================================

Assigns an editorial importance score to a story.

Version 2.1
-----------
• Uses whole-word regex matching.
• Eliminates substring bugs such as:
      Netflix -> ETF
"""

import re


KEYWORDS = {

    # Major Studios
    "comcast": 35,
    "nbcuniversal": 35,
    "disney": 30,
    "warner": 30,
    "warner bros": 35,
    "universal": 30,
    "paramount": 30,
    "sony pictures": 30,

    # Movies
    "movie": 20,
    "film": 20,
    "box office": 30,
    "trailer": 20,
    "marvel": 20,

    # Television
    "television": 20,
    "tv": 15,
    "series": 20,
    "season": 15,
    "episode": 10,

    # Streaming
    "netflix": 30,
    "streaming": 20,
    "disney+": 30,
    "prime video": 25,
    "max": 25,
    "hulu": 20,
    "peacock": 20,

    # Music
    "music": 15,
    "album": 20,
    "tour": 25,
    "concert": 20,
    "grammy": 30,
    "billboard": 20,

    # Broadway
    "broadway": 30,
    "musical": 20,
    "theatre": 20,
    "theater": 20,

    # Awards
    "oscar": 35,
    "emmy": 30,
    "golden globe": 30,

    # Celebrities
    "celebrity": 15,
    "hollywood": 20,
    "actor": 15,
    "actress": 15,
    "director": 15,
    "producer": 15,

    # Gaming
    "gaming": 15,
    "video game": 20,
    "playstation": 20,
    "xbox": 20,
    "nintendo": 20,
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


def score_story(story):
    """
    Return an editorial importance score.
    """

    text = (
        story.get("headline", "")
        + " "
        + story.get("summary", "")
    )

    score = 0

    for keyword, value in KEYWORDS.items():

        if keyword_found(keyword, text):

            score += value

    return score


if __name__ == "__main__":

    tests = [

        {
            "headline":
            "Comcast Plans Tax-Free Spin-Off Of NBCUniversal",
            "summary": ""
        },

        {
            "headline":
            "Marvel Reveals Fantastic Four Trailer",
            "summary": ""
        },

        {
            "headline":
            "Taylor Swift Announces World Tour",
            "summary": ""
        },

        {
            "headline":
            "Netflix Renews Hit Series For Season 3",
            "summary": ""
        }

    ]

    print("=" * 60)
    print("SHOWBIZ STORY SCORER 2.1")
    print("=" * 60)

    for story in tests:

        print()
        print(story["headline"])
        print("Score:", score_story(story))