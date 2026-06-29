"""
===========================================
ShowBiz Editorial Filter
Version 2.1
===========================================

Determines whether a story belongs on ShowBiz
using weighted editorial scoring.

Version 2.1
-----------
• Uses whole-word regex matching.
• Eliminates substring bugs such as:
      Netflix -> ETF
"""

import re


# ------------------------------------------------
# Positive entertainment signals
# ------------------------------------------------

POSITIVE = {

    # Movies
    "movie": 20,
    "film": 20,
    "cinema": 20,
    "box office": 30,
    "trailer": 20,

    # Television
    "television": 20,
    "tv": 15,
    "series": 20,
    "season": 15,
    "episode": 10,

    # Streaming
    "netflix": 30,
    "disney+": 30,
    "prime video": 25,
    "max": 25,
    "hulu": 20,
    "peacock": 20,

    # Studios
    "disney": 25,
    "warner": 25,
    "warner bros": 30,
    "universal": 25,
    "paramount": 25,
    "sony pictures": 25,
    "nbcuniversal": 30,
    "comcast": 25,

    # Music
    "album": 20,
    "single": 15,
    "concert": 20,
    "tour": 25,
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
    "festival": 20,

    # Entertainment people
    "actor": 15,
    "actress": 15,
    "director": 15,
    "producer": 15,
    "celebrity": 15,
    "hollywood": 20,

    # Gaming
    "video game": 20,
    "playstation": 20,
    "xbox": 20,
    "nintendo": 20,

    # Industry
    "streaming": 20,
    "entertainment": 15,
}


# ------------------------------------------------
# Negative signals
# ------------------------------------------------

NEGATIVE = {

    # Politics
    "election": -50,
    "president": -40,
    "senate": -40,
    "congress": -40,
    "parliament": -40,
    "minister": -30,
    "government": -30,

    # Courts
    "supreme court": -50,
    "court": -30,
    "judge": -25,
    "lawsuit": -20,

    # Crime
    "murder": -50,
    "shooting": -50,
    "arrest": -30,
    "kidnapping": -40,
    "cartel": -50,
    "prison": -30,
    "jail": -30,

    # Immigration
    "immigration": -40,
    "immigrant": -40,
    "refugee": -30,

    # War
    "war": -50,
    "military": -40,
    "missile": -40,
    "ukraine": -30,
    "gaza": -30,

    # Finance
    "stock": -30,
    "stocks": -30,
    "etf": -30,
    "inflation": -30,
    "bank": -30,

    # Weather
    "earthquake": -40,
    "hurricane": -40,
    "tornado": -40,
    "storm": -25,
    "flood": -25,

    # Sports
    "nfl": -20,
    "nba": -20,
    "mlb": -20,
    "nhl": -20,
    "world cup": -30,
    "olympics": -20,
}


MINIMUM_SCORE = 20


def keyword_found(keyword, text):
    """
    Match complete words or phrases only.

    Prevents:
        Netflix -> ETF

    while still matching:

        Netflix
        Supreme Court
        Prime Video
    """

    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def analyze_story(story):

    text = (
        story.get("headline", "")
        + " "
        + story.get("summary", "")
    )

    score = 0

    positives = []
    negatives = []

    for keyword, value in POSITIVE.items():

        if keyword_found(keyword, text):

            score += value
            positives.append((keyword, value))

    for keyword, value in NEGATIVE.items():

        if keyword_found(keyword, text):

            score += value
            negatives.append((keyword, value))

    return score, positives, negatives


def keep_story(story):

    score, _, _ = analyze_story(story)

    return score >= MINIMUM_SCORE


if __name__ == "__main__":

    tests = [

        {
            "headline":
            "Netflix Renews Hit Series For Season 3",
            "summary": ""
        },

        {
            "headline":
            "Marvel Releases Fantastic Four Trailer",
            "summary": ""
        },

        {
            "headline":
            "Supreme Court Issues New Decision",
            "summary": ""
        },

        {
            "headline":
            "Taylor Swift Announces New Tour",
            "summary": ""
        },

        {
            "headline":
            "World Cup Final Ends In Penalty Shootout",
            "summary": ""
        }

    ]

    print("=" * 60)
    print("SHOWBIZ EDITORIAL FILTER 2.1")
    print("=" * 60)

    for story in tests:

        score, pos, neg = analyze_story(story)

        print()
        print(story["headline"])
        print("Score:", score)
        print("KEEP :", keep_story(story))

        if pos:

            print("Positive Matches:")

            for item in pos:

                print(f"   + {item[0]:20} {item[1]}")

        if neg:

            print("Negative Matches:")

            for item in neg:

                print(f"   - {item[0]:20} {item[1]}")