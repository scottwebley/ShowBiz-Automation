"""
===========================================
ShowBiz Image Query Builder
Version 1.0
===========================================

Builds prioritized Media Library search
queries for the Image Engine.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from itertools import combinations

from engine.entity_extractor import extract_entities


def _unique(items):
    seen = set()
    result = []

    for item in items:
        item = item.strip()

        if not item:
            continue

        key = item.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def build_search_queries(story, keyword_queries=None):
    """
    Returns a prioritized list of search queries.

    Priority:

        1. Individual people
        2. Person pairs
        3. Three-person combination
        4. Movies
        5. TV
        6. Music
        7. Organizations
        8. Events
        9. Keyword fallback
    """

    headline = story.get("headline", "")

    entities = extract_entities(headline)

    queries = []

    #
    # Individual people
    #

    people = entities["people"]

    queries.extend(people)

    #
    # Person pairs
    #

    for pair in combinations(people, 2):
        queries.append(" ".join(pair))

    #
    # Three-person combination
    #

    if len(people) >= 3:
        queries.append(" ".join(people[:3]))

    #
    # Movies
    #

    queries.extend(entities["movies"])

    #
    # TV
    #

    queries.extend(entities["tv_shows"])

    #
    # Music
    #

    queries.extend(entities["music_artists"])

    #
    # Organizations
    #

    queries.extend(entities["organizations"])

    #
    # Events
    #

    queries.extend(entities["events"])

    #
    # Keyword fallback
    #

    if keyword_queries:
        queries.extend(keyword_queries)

    return _unique(queries)


if __name__ == "__main__":

    story = {
        "headline":
            "Taylor Swift and Travis Kelce "
            "expected wedding celebrations approach"
    }

    print()

    for query in build_search_queries(
        story,
        keyword_queries=[
            "Taylor Swift Travis Kelce wedding"
        ],
    ):
        print(query)