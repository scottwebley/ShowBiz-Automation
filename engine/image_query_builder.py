"""
===========================================
ShowBiz Image Query Builder
Version 2.0
===========================================

Builds prioritized Media Library search
queries for the Image Engine.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

import re
from itertools import combinations

from engine.entity_extractor import extract_entities

print("USING IMAGE_QUERY_BUILDER:", __file__)
print("IMAGE_QUERY_BUILDER VERSION TEST")


#
# Entertainment companies that often have
# corresponding Media Library images.
#

KNOWN_ORGANIZATIONS = (
    "Disney",
    "Disney+",
    "Pixar",
    "Marvel",
    "Lucasfilm",
    "Star Wars",
    "Netflix",
    "Apple TV+",
    "Apple TV",
    "Amazon MGM",
    "Amazon",
    "Prime Video",
    "Warner Bros.",
    "Warner Bros",
    "Max",
    "HBO",
    "Hulu",
    "Paramount",
    "Paramount+",
    "Peacock",
    "NBC",
    "NBCUniversal",
    "Universal",
    "Sony",
    "Sony Pictures",
    "A24",
    "Lionsgate",
    "DreamWorks",
    "DC",
)


BAD_PERSON_WORDS = {
    "daily",
    "news",
    "live",
    "contest",
    "champions",
    "tournament",
    "tournaments",
    "coverage",
    "review",
    "preview",
    "guide",
    "updates",
    "today",
    "breaking",
    "independent",
}


def _unique(items):

    seen = set()
    output = []

    for item in items:

        item = item.strip()

        if not item:
            continue

        key = item.lower()

        if key in seen:
            continue

        seen.add(key)
        output.append(item)

    return output


def _clean_people(people):

    cleaned = []

    for person in people:

        words = person.split()

        #
        # Ignore one-word names.
        #

        if len(words) < 2:
            continue

        lower = person.lower()

        #
        # Reject obvious bad entities.
        #

        if any(
            bad in lower
            for bad in BAD_PERSON_WORDS
        ):
            continue

        cleaned.append(person)

    return cleaned


def _organizations_from_headline(headline):

    found = []

    lower = headline.lower()

    for org in KNOWN_ORGANIZATIONS:

        if org.lower() in lower:
            found.append(org)

    return found
def build_search_queries(
    story,
    keyword_queries=None,
):
    """
    Returns a prioritized list of editorial-quality
    Media Library search queries.

    Priority:

        1. Exact movie titles
        2. Exact TV titles
        3. Music artists
        4. Person + title combinations
        5. Entertainment companies
        6. Valid people
        7. Person pairs
        8. Events
        9. Franchise fallback
        10. Keyword fallback
    """

    headline = story.get(
        "headline",
        "",
    )

    entities = extract_entities(
        headline
    )

    queries = []

    #
    # 1. Movies first.
    #

    movie_titles = entities.get(
        "movies",
        [],
    )

    queries.extend(movie_titles)

    #
    # 2. TV shows.
    #

    tv_titles = entities.get(
        "tv_shows",
        [],
    )

    queries.extend(tv_titles)

    #
    # 3. Music artists.
    #

    music_titles = entities.get(
        "music_artists",
        [],
    )

    queries.extend(music_titles)

    #
    # Primary visual subjects.
    #

    primary_titles = (
        movie_titles
        + tv_titles
        + music_titles
    )

    #
    # Clean people.
    #

    people = _clean_people(
        entities.get(
            "people",
            [],
        )
    )

    has_primary_subject = any([
        primary_titles,
        people,
        entities.get("events"),
    ])

    #
    # 4. Person + title combinations.
    #
    # These are much more specific than
    # person-only searches and help avoid
    # matching the wrong production.
    #

    for title in primary_titles:
        for person in people:

            queries.append(
                f"{person} {title}"
            )

            queries.append(
                f"{title} {person}"
            )

        #
    # 5. Organizations.
    #
    # Only search companies if we don't
    # already have a better visual subject.
    #

    if not has_primary_subject:

        organizations = _unique(
            entities.get("organizations", [])
            + _organizations_from_headline(headline)
        )

        #
        # If two major organizations appear together,
        # search the combined phrase first.
        #

        if len(organizations) >= 2:

            queries.append(
                f"{organizations[0]} {organizations[1]}"
            )

        queries.extend(organizations)

    #
    # 6. People.
    #

    queries.extend(
        people
    )

    #
    # 7. Person pairs.
    #

    for pair in combinations(
        people,
        2,
    ):

        queries.append(
            " ".join(pair)
        )

    #
    # 8. Events.
    #

    queries.extend(
        entities.get(
            "events",
            [],
        )
    )

    #
    # 9. Franchise fallback.
    #

    franchise_hits = []

    headline_lower = headline.lower()

    for franchise in (
        "Marvel",
        "DC",
        "Star Wars",
        "Pixar",
    ):

        if franchise.lower() in headline_lower:

            franchise_hits.append(
                franchise
            )

    queries.extend(
        franchise_hits
    )

    #
    # 10. Keyword fallback.
    #

    if keyword_queries:

        queries.extend(
            keyword_queries
        )

    #
    # Final cleanup.
    #

    cleaned = []

    for query in _unique(
        queries
    ):

        query = re.sub(
            r"\s+",
            " ",
            query,
        ).strip()

        if len(query) < 2:
            continue

        cleaned.append(
            query
        )

    return cleaned
if __name__ == "__main__":

    tests = [

        {
            "headline":
                "Taylor Swift and Travis Kelce expected wedding celebrations approach"
        },

        {
            "headline":
                "Marvel Contest of Champions to Host Demos and Daily Tournaments at SDCC 2026"
        },

        {
            "headline":
                "Paramount merger gets breathing room after regulators delay decision"
        },

        {
            "headline":
                "Finn Wolfhard planning Phoenix tour stop"
        },

        {
            "headline":
                "Disney+ planning new Marvel series"
        },

    ]

    for story in tests:

        print()
        print("=" * 60)
        print(story["headline"])
        print("=" * 60)

        for query in build_search_queries(story):

            print(f"• {query}")