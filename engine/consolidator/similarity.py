from difflib import SequenceMatcher

from engine.consolidator.normalize import (
    normalize,
    keywords,
    entities,
)

from engine.consolidator.fingerprint import same_event


def _get(story, *fields):
    """
    Return the first non-empty field.
    """

    for field in fields:
        value = story.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def _text(story):
    """
    Build the largest useful text block available.

    Different feeds use different field names.
    """

    return normalize(
        " ".join(
            filter(
                None,
                [
                    _get(story, "headline", "title", "name"),
                    _get(story, "summary", "excerpt", "dek"),
                    _get(story, "description"),
                    _get(story, "content"),
                    _get(story, "body"),
                    _get(story, "text"),
                ],
            )
        )
    )


def _headline(story):
    return normalize(
        _get(story, "headline", "title", "name")
    )


def similarity_report(story1, story2):

    headline1 = _headline(story1)
    headline2 = _headline(story2)

    text1 = _text(story1)
    text2 = _text(story2)

    headline_score = SequenceMatcher(None, headline1, headline2).ratio()
    body_score = SequenceMatcher(None, text1, text2).ratio()

    kw1 = keywords(text1)
    kw2 = keywords(text2)

    keyword_score = (
        len(kw1 & kw2) / len(kw1 | kw2)
        if (kw1 or kw2)
        else 0.0
    )

    ent1 = entities(text1)
    ent2 = entities(text2)

    entity_score = (
        len(ent1 & ent2) / len(ent1 | ent2)
        if (ent1 or ent2)
        else 0.0
    )

    same = same_event(text1, text2)

    score = (
        headline_score * 0.20 +
        body_score * 0.40 +
        keyword_score * 0.20 +
        entity_score * 0.20
    )

    if same:
        score += 0.15

    score = min(score, 1.0)

    return {
        "headline": headline_score,
        "body": body_score,
        "keyword": keyword_score,
        "entity": entity_score,
        "combined": score,
        "same_event": same,
    }


def combined_score(story1, story2):
    return similarity_report(story1, story2)["combined"]


def should_cluster(story1, story2):
    return combined_score(story1, story2) >= 0.60