# engine/consolidator/fingerprint.py

"""
ShowBiz Story Consolidator
Fingerprint Engine v6
"""

from engine.consolidator.normalize import normalize, entities, event_words


def extract_entity(text):
    """
    Return the strongest entity candidate.
    """

    entity_list = sorted(entities(text), key=len, reverse=True)

    if not entity_list:
        return None

    return entity_list[0]


def extract_event(text):
    """
    Return the first normalized event.
    """

    events = event_words(text)

    if not events:
        return None

    return events[0]


def event_fingerprint(text):
    """
    Create a normalized event fingerprint.

    Example:
        Disney delays Avatar
            -> ("disney", "delay")

        Cinerama Dome reopens
            -> ("cinerama", "reopen")
    """

    return (
        extract_entity(text),
        extract_event(text),
    )


def same_event(headline1, headline2):
    """
    True if both headlines describe
    the same normalized entertainment event.
    """

    entity1, event1 = event_fingerprint(headline1)
    entity2, event2 = event_fingerprint(headline2)

    return (
        entity1 is not None
        and entity2 is not None
        and event1 is not None
        and event2 is not None
        and entity1 == entity2
        and event1 == event2
    )


def fingerprint_string(text):
    """
    Human-readable fingerprint for logging.
    """

    entity, event = event_fingerprint(text)

    if not entity and not event:
        return "unknown"

    if not entity:
        return event

    if not event:
        return entity

    return f"{entity}:{event}"


def print_fingerprint(text):
    """
    Debug helper.
    """

    print(f"{text}")
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