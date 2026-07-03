"""
===========================================
ShowBiz Editorial Filter
Version 3.1
===========================================

Determines whether a story belongs on ShowBiz
using editorial rules plus weighted scoring.

Version 3.1
-----------
• Whole-word regex matching
• Hard rejection of wrapper articles
• Penalties for low-value content
• Editorial rejection reasons
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
    "amazon mgm": 25,
    "apple tv+": 25,
    "a24": 25,

    # Music
    "album": 20,
    "single": 15,
    "concert": 20,
    "tour": 25,
    "grammy": 30,
    "billboard": 20,

    "singer": 20,
    "songwriter": 20,
    "musician": 20,
    "vocalist": 20,
    "recording artist": 20,
    "band": 15,
    "pop star": 20,
    "rock star": 20,

    # Celebrity News
    "wedding": 30,
    "married": 30,
    "marriage": 30,
    "engagement": 25,
    "engaged": 25,
    "dating": 15,
    "relationship": 15,
    "couple": 15,
    "romance": 15,
    "baby": 15,
    "pregnancy": 15,
    "pregnant": 15,
    "family": 10,
    "red carpet": 20,
    "premiere": 20,
    "gala": 20,
    "fashion": 15,

    # Major Franchises
    "marvel": 25,
    "dc": 20,
    "pixar": 25,
    "lucasfilm": 25,
    "star wars": 30,
    "avatar": 25,
    "harry potter": 25,

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
    "actor": 20,
    "actress": 20,
    "director": 20,
    "producer": 20,
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


# ------------------------------------------------
# Immediate editorial rejection patterns
# ------------------------------------------------

HARD_REJECT_PATTERNS = [

    r"^AP Trending SummaryBrief",
    r"\bSummaryBrief\b",
    r"\bMorning Brief\b",
    r"\bEvening Brief\b",
    r"\bRoundup\b",
    r"\bLive Updates?\b",
    r"\bLive Blog\b",
    r"\bArchive\b",
    r"\bTag\b",
]


# ------------------------------------------------
# Low-value content penalties
# ------------------------------------------------

LOW_VALUE_PATTERNS = {

    r"\bTop\s+\d+\b": -40,
    r"\bBest\b": -20,
    r"\bEverything You Need To Know\b": -40,
    r"\bExplained\b": -20,
    r"\bHow To\b": -35,
    r"\bVPN\b": -60,
    r"\bBuying Guide\b": -50,
    r"\bCoupon\b": -50,
    r"\bDeal\b": -30,
}

MINIMUM_SCORE = 20


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


def matches_hard_reject(text):
    """
    Returns (True, reason) if the story should
    immediately be rejected.
    """

    for pattern in HARD_REJECT_PATTERNS:

        if re.search(pattern, text, flags=re.IGNORECASE):

            return True, pattern

    return False, ""


def analyze_story(story):

    text = (
        story.get("headline", "")
        + " "
        + story.get("summary", "")
    )

    score = 0

    positives = []
    negatives = []

    #
    # Positive signals
    #

    for keyword, value in POSITIVE.items():

        if keyword_found(keyword, text):

            score += value
            positives.append((keyword, value))

    #
    # Negative signals
    #

    for keyword, value in NEGATIVE.items():

        if keyword_found(keyword, text):

            score += value
            negatives.append((keyword, value))

    #
    # Low-value penalties
    #

    penalties = []

    for pattern, value in LOW_VALUE_PATTERNS.items():

        if re.search(pattern, text, flags=re.IGNORECASE):

            score += value
            penalties.append((pattern, value))

    return score, positives, negatives, penalties


def keep_story(story):
    """
    Returns True if the story should
    continue through the pipeline.
    """

    text = (
        story.get("headline", "")
        + " "
        + story.get("summary", "")
    )

    rejected, reason = matches_hard_reject(text)

    if rejected:

        print(f"REJECT: Hard rule matched ({reason})")

        return False

    score, _, _, penalties = analyze_story(story)

    if penalties:

        for pattern, value in penalties:

            print(f"PENALTY: {pattern} ({value})")

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
            "AP Trending SummaryBrief at 6:28 p.m. EDT",
            "summary":
            "Actor Danny Glover reveals Alzheimer's diagnosis."
        },

        {
            "headline":
            "How To Watch Netflix Using A VPN",
            "summary": ""
        },

        {
            "headline":
            "Taylor Swift Announces New Tour",
            "summary": ""
        }

    ]

    print("=" * 60)
    print("SHOWBIZ EDITORIAL FILTER 3.0")
    print("=" * 60)

    for story in tests:

        score, pos, neg, penalties = analyze_story(story)

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

        if penalties:

            print("Penalties:")

            for item in penalties:

                print(f"   * {item[0]:20} {item[1]}")