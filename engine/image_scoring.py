"""
===========================================
ShowBiz Image Scoring
Version 1.0
===========================================

Scores Media Library image candidates.

This module performs NO searching,
ranking or verification.

Author:
    ShowBiz Automation
"""

from engine.entity_extractor import extract_entities


PERSON_MATCH = 40
MULTI_PERSON_MATCH = 100
MOVIE_MATCH = 35
TV_MATCH = 35
MUSIC_MATCH = 30
ORGANIZATION_MATCH = 20
GENERIC_TITLE_PENALTY = 50


GENERIC_TITLE_PATTERNS = (
    "aggregator downloaded",
    "downloaded image",
    "img_",
    "dsc_",
    "image",
)


def _contains(text, phrase):
    return phrase.lower() in text.lower()


def _count_matches(text, phrases):
    return sum(
        1
        for phrase in phrases
        if _contains(text, phrase)
    )


def score_candidate(story, candidate):
    """
    Returns:

        (score, reasons)
    """

    headline = story.get("headline", "")
    entities = extract_entities(headline)

    title = candidate.get("title", "")
    filename = candidate.get("filename", "")

    searchable = f"{title} {filename}"

    score = 0
    reasons = []

    #
    # People
    #

    people_matches = _count_matches(
        searchable,
        entities["people"],
    )

    if people_matches >= 2:
        score += MULTI_PERSON_MATCH
        reasons.append(
            f"Matched {people_matches} people "
            f"(+{MULTI_PERSON_MATCH})"
        )

    elif people_matches == 1:
        score += PERSON_MATCH
        reasons.append(
            f"Matched headline person "
            f"(+{PERSON_MATCH})"
        )

    #
    # Movies
    #

    for movie in entities["movies"]:
        if _contains(searchable, movie):
            score += MOVIE_MATCH
            reasons.append(
                f"Movie match (+{MOVIE_MATCH})"
            )

    #
    # TV
    #

    for show in entities["tv_shows"]:
        if _contains(searchable, show):
            score += TV_MATCH
            reasons.append(
                f"TV match (+{TV_MATCH})"
            )

    #
    # Music
    #

    for artist in entities["music_artists"]:
        if _contains(searchable, artist):
            score += MUSIC_MATCH
            reasons.append(
                f"Music match (+{MUSIC_MATCH})"
            )

    #
    # Organizations
    #

    for organization in entities["organizations"]:
        if _contains(searchable, organization):
            score += ORGANIZATION_MATCH
            reasons.append(
                f"Organization match "
                f"(+{ORGANIZATION_MATCH})"
            )

    #
    # Generic title
    #

    lower_title = title.lower()

    if any(
        pattern in lower_title
        for pattern in GENERIC_TITLE_PATTERNS
    ):
        score -= GENERIC_TITLE_PENALTY
        reasons.append(
            f"Generic title "
            f"(-{GENERIC_TITLE_PENALTY})"
        )

    return score, reasons