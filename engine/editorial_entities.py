"""
===========================================
ShowBiz Editorial Entities
Version 1.0
===========================================

Purpose:
    Central repository of major entertainment
    entities used by the editorial scoring
    engine.

    This module contains NO scoring logic.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


# ---------------------------------------------------------
# Major film / television stars
# ---------------------------------------------------------

MAJOR_ACTORS = (
    "tom cruise",
    "leonardo dicaprio",
    "brad pitt",
    "george clooney",
    "dwayne johnson",
    "ryan reynolds",
    "timothée chalamet",
    "timothee chalamet",
    "keanu reeves",
    "chris hemsworth",
    "chris evans",
    "robert downey jr",
    "robert downey jr.",
    "harrison ford",
    "matt damon",
    "ben affleck",
    "will smith",
    "michael b. jordan",
    "pedro pascal",
    "cillian murphy",
)

MAJOR_ACTRESSES = (
    "meryl streep",
    "scarlett johansson",
    "zendaya",
    "emma stone",
    "margot robbie",
    "jennifer lawrence",
    "cate blanchett",
    "angelina jolie",
    "nicole kidman",
    "sandra bullock",
    "anne hathaway",
    "julia roberts",
    "viola davis",
    "anya taylor-joy",
    "florence pugh",
)


# ---------------------------------------------------------
# Music
# ---------------------------------------------------------

MAJOR_MUSICIANS = (
    "taylor swift",
    "beyoncé",
    "beyonce",
    "drake",
    "billie eilish",
    "ed sheeran",
    "dua lipa",
    "bruno mars",
    "olivia rodrigo",
    "lady gaga",
    "the weeknd",
    "post malone",
    "kendrick lamar",
    "morgan wallen",
    "bad bunny",
)


# ---------------------------------------------------------
# Directors / producers
# ---------------------------------------------------------

MAJOR_DIRECTORS = (
    "steven spielberg",
    "christopher nolan",
    "james cameron",
    "quentin tarantino",
    "martin scorsese",
    "greta gerwig",
    "denis villeneuve",
    "ridley scott",
    "taika waititi",
    "ryan coogler",
)


# ---------------------------------------------------------
# Television personalities
# ---------------------------------------------------------

MAJOR_HOSTS = (
    "jimmy fallon",
    "jimmy kimmel",
    "stephen colbert",
    "seth meyers",
    "john oliver",
    "trevor noah",
)


# ---------------------------------------------------------
# Awards
# ---------------------------------------------------------

MAJOR_AWARDS = (
    "academy awards",
    "oscars",
    "emmys",
    "grammys",
    "golden globes",
    "tony awards",
    "cannes",
    "venice film festival",
    "toronto international film festival",
)


# ---------------------------------------------------------
# Helper collections
# ---------------------------------------------------------

MAJOR_ENTITIES = (
    MAJOR_ACTORS
    + MAJOR_ACTRESSES
    + MAJOR_MUSICIANS
    + MAJOR_DIRECTORS
    + MAJOR_HOSTS
    + MAJOR_AWARDS
)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def contains_major_entity(text: str) -> bool:
    """
    True if any major entertainment entity
    appears in the text.
    """

    text = text.lower()

    return any(
        entity in text
        for entity in MAJOR_ENTITIES
    )


def count_major_entities(text: str) -> int:
    """
    Count the number of unique major
    entertainment entities found.
    """

    text = text.lower()

    return sum(
        1
        for entity in MAJOR_ENTITIES
        if entity in text
    )