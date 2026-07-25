# engine/consolidator/fingerprint.py

"""
ShowBiz Story Consolidator
Fingerprint Engine v7
"""

from difflib import SequenceMatcher

from engine.consolidator.normalize import (
    normalize,
    keywords,
    entities,
    event_words,
)


def extract_entity(text):
    entity_list = sorted(
        entities(text),
        key=lambda e: (len(e.split()), len(e)),
        reverse=True,
    )

    for entity in entity_list:
        if len(entity) >= 3:
            return entity

    return None


def extract_event(text):
    events = event_words(text)
    return events[0] if events else None


def event_fingerprint(text):
    return (
        extract_entity(text),
        extract_event(text),
    )


def same_event(story1, story2):
    """
    Compare two complete story dictionaries.
    """

    def headline(item):
        if isinstance(item, dict):
            return (
                item.get("headline")
                or item.get("title")
                or item.get("name")
                or ""
            )
        return str(item)

    def full_text(item):
        if not isinstance(item, dict):
            return str(item)

        fields = [
            "headline",
            "title",
            "name",
            "summary",
            "excerpt",
            "dek",
            "description",
            "body",
            "content",
            "text",
        ]

        parts = []

        for field in fields:
            value = item.get(field)
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())

        return " ".join(parts)

    h1 = headline(story1)
    h2 = headline(story2)

    t1 = full_text(story1)
    t2 = full_text(story2)

    headline_similarity = SequenceMatcher(
        None,
        normalize(h1),
        normalize(h2),
    ).ratio()

    words1 = set(keywords(t1))
    words2 = set(keywords(t2))

    keyword_overlap = (
        len(words1 & words2)
        / max(1, len(words1 | words2))
    )

    entity1 = set(entities(t1))
    entity2 = set(entities(t2))

    entity_overlap = (
        len(entity1 & entity2)
        / max(1, len(entity1 | entity2))
    )

    event1 = set(event_words(t1))
    event2 = set(event_words(t2))

    event_match = 1.0 if (event1 & event2) else 0.0

    score = (
        headline_similarity * 0.25
        + keyword_overlap * 0.35
        + entity_overlap * 0.30
        + event_match * 0.10
    )

    entity_match = (
    extract_entity(t1) is not None
    and extract_entity(t1) == extract_entity(t2)
)

    same = (
        headline_similarity >= 0.92
        or score >= 0.55
        or (
            event_match == 1.0
            and entity_match
            and (
                headline_similarity >= 0.20
                or keyword_overlap >= 0.03
            )
        )
    )

    print("\n========== FINGERPRINT DEBUG ==========")
    print(h1)
    print(h2)
    print(f"Headline : {headline_similarity:.2f}")
    print(f"Keywords : {keyword_overlap:.2f}")
    print(f"Entities : {entity_overlap:.2f}")
    print(f"Events   : {event_match:.2f}")
    print(f"Score    : {score:.2f}")
    print(f"Same     : {same}")

    return same


def fingerprint_string(text):
    entity, event = event_fingerprint(text)

    if not entity and not event:
        return "unknown"

    if not entity:
        return event

    if not event:
        return entity

    return f"{entity}:{event}"


def print_fingerprint(text):
    print(text)
    print(f" -> {fingerprint_string(text)}")


if __name__ == "__main__":

    samples = [
        "Cinerama Dome Reopens in Hollywood",
        "Hollywood's Cinerama Dome reopening announced",
        "Disney delays Avatar release",
        "Disney postpones Avatar movie",
        "Netflix renews Wednesday",
        "Wednesday renewed by Netflix",
    ]

    for sample in samples:
        print_fingerprint(sample)
        print()