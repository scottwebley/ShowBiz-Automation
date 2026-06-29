"""
===========================================
ShowBiz Editor
Version 2.0
===========================================

Final editorial decision maker.

This module provides:

- editorial_decision(story)
- should_publish(story)

The should_publish() function is retained
for backward compatibility with older
production modules.
"""

POLITICAL = [
    "president",
    "election",
    "congress",
    "senate",
    "government",
    "trump",
    "biden",
    "republican",
    "democrat",
]

SPORTS = [
    "nfl",
    "nba",
    "mlb",
    "nhl",
    "f1",
    "formula 1",
    "soccer",
    "football",
    "baseball",
    "basketball",
    "olympics",
]

CRIME = [
    "murder",
    "shooting",
    "kidnapping",
    "cartel",
]

BUSINESS = [
    "bankruptcy",
    "inflation",
    "interest rates",
]


def editorial_decision(story):
    """
    Return:
        (decision, reason)

    decision:
        PUBLISH
        REJECT
    """

    headline = story.get("headline", "")
    summary = story.get("summary", "")

    text = f"{headline} {summary}".lower()

    score = story.get("score", 0)
    category = story.get("category", "Uncategorized")

    #
    # Minimum score
    #

    if score < 30:
        return (
            "REJECT",
            "Score too low",
        )

    #
    # Politics
    #

    for word in POLITICAL:
        if word in text:
            return (
                "REJECT",
                "Political story",
            )

    #
    # Sports
    #

    for word in SPORTS:
        if word in text:
            return (
                "REJECT",
                "Sports story",
            )

    #
    # Crime
    #

    for word in CRIME:
        if word in text:
            return (
                "REJECT",
                "Crime story",
            )

    #
    # General business
    #

    for word in BUSINESS:
        if word in text:
            return (
                "REJECT",
                "Business story",
            )

    #
    # Uncategorized
    #

    if category == "Uncategorized":
        return (
            "REJECT",
            "No entertainment category",
        )

    return (
        "PUBLISH",
        "Editorial approval",
    )


def should_publish(story):
    """
    Backward compatibility.

    Older production modules expect
    should_publish(story) -> bool
    """

    decision, _ = editorial_decision(story)

    return decision == "PUBLISH"


if __name__ == "__main__":

    tests = [

        {
            "headline":
            "Comcast's NBC Spinoff Raises Questions About Businesses' Future",
            "score": 135,
            "category": "Entertainment Industry",
        },

        {
            "headline":
            "Greater Dallas County Development Alliance awards 4 small businesses grants",
            "score": 20,
            "category": "Broadway",
        },

        {
            "headline":
            "Susie Wolff explains why F1 Academy cannot be a charity project",
            "score": 50,
            "category": "Television",
        },

        {
            "headline":
            "Taylor Swift Announces World Tour",
            "score": 70,
            "category": "Music",
        },

    ]

    print("=" * 60)
    print("SHOWBIZ EDITOR")
    print("=" * 60)

    for story in tests:

        decision, reason = editorial_decision(story)

        print()
        print(story["headline"])
        print(decision)
        print(reason)