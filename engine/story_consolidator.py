"""
story_consolidator.py
ShowBiz Story Consolidator v5.0

Version 5 improvements

• Event normalization
• Event fingerprinting
• Better entertainment duplicate detection
• Preserves Version 4 public API
"""

import re

from difflib import SequenceMatcher

# ----------------------------------------------------------
# Weights
# ----------------------------------------------------------

ENTITY_WEIGHT = 0.50
HEADLINE_WEIGHT = 0.25
KEYWORD_WEIGHT = 0.25

ENTITY_THRESHOLD = 0.30
KEYWORD_THRESHOLD = 0.45
FINAL_THRESHOLD = 0.65

# ----------------------------------------------------------
# Common stop words
# ----------------------------------------------------------

STOP_WORDS = {

    "a","an","and","are","as","at","be","been",
    "being","by","for","from","how","if","in",
    "into","is","it","its","of","on","or",
    "that","the","their","this","to","was",
    "were","what","when","where","which","who",
    "why","will","with",

    "after",
    "amid",
    "before",
    "despite",
    "during",

    "latest",
    "new",

    "report",
    "reports",

    "say",
    "says",

    "reveals",
    "revealed",

    "first",
    "look",
    "review",

    "breaking",
    "exclusive",
}

# ----------------------------------------------------------
# Event normalization
# ----------------------------------------------------------

EVENT_ALIASES = {

    #
    # layoffs
    #

    "layoff":"layoff",
    "layoffs":"layoff",

    "job":"job",
    "jobs":"job",

    "cuts":"layoff",
    "cut":"layoff",

    "downsizing":"layoff",
    "downsizes":"layoff",
    "downsize":"layoff",

    "workforce":"layoff",
    "staff":"layoff",

    "reduction":"layoff",
    "reductions":"layoff",

    "eliminates":"layoff",
    "eliminate":"layoff",

    "fired":"layoff",
    "fires":"layoff",

    #
    # cancellations
    #

    "cancelled":"cancel",
    "canceled":"cancel",
    "cancel":"cancel",
    "cancels":"cancel",

    "called":"cancel",

    #
    # delays
    #

    "delay":"delay",
    "delays":"delay",

    "delayed":"delay",

    "postponed":"delay",
    "postpone":"delay",

    #
    # renewals

    "renewed":"renew",
    "renews":"renew",
    "renewal":"renew",

    #
    # premieres

    "premiere":"premiere",
    "premieres":"premiere",

    "debut":"premiere",
    "debuts":"premiere",

    "launch":"premiere",
    "launches":"premiere",

}

# ----------------------------------------------------------

def _normalize(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
    )

    words = []

    for word in text.split():

        if word in STOP_WORDS:
            continue

        word = EVENT_ALIASES.get(
            word,
            word,
        )

        words.append(word)

    return " ".join(words)

# ----------------------------------------------------------

def _keywords(text):

    return {

        word

        for word in _normalize(text).split()

        if len(word) >= 3

    }

# ----------------------------------------------------------

def _headline_similarity(a,b):

    return SequenceMatcher(

        None,

        _normalize(a),

        _normalize(b),

    ).ratio()

# ----------------------------------------------------------

def _keyword_similarity(a,b):

    a_words = _keywords(a)

    b_words = _keywords(b)

    if not a_words or not b_words:
        return 0.0

    overlap = len(
        a_words & b_words
    )

    union = len(
        a_words | b_words
    )

    return overlap / union

# ----------------------------------------------------------

def _entity_similarity(a,b):

    entities_a = {

        w

        for w in _keywords(a)

        if len(w) > 4

    }

    entities_b = {

        w

        for w in _keywords(b)

        if len(w) > 4

    }

    if not entities_a or not entities_b:
        return 0.0

    overlap = len(
        entities_a & entities_b
    )

    union = len(
        entities_a | entities_b
    )

    return overlap / union
# ----------------------------------------------------------

def _event_fingerprint(text):

    """
    Extract a normalized event fingerprint.

    Example:

        Pixar Announces Layoffs
            -> ("pixar", "layoff")

        Disney Delays Avatar
            -> ("disney", "delay")
    """

    words = _normalize(text).split()

    entities = [
        w for w in words
        if len(w) > 4
    ]

    events = [
        w for w in words
        if w in {
            "layoff",
            "delay",
            "cancel",
            "renew",
            "premiere",
        }
    ]

    entity = entities[0] if entities else None
    event = events[0] if events else None

    return entity, event


# ----------------------------------------------------------

def _same_event(a, b):

    entity1, event1 = _event_fingerprint(a)
    entity2, event2 = _event_fingerprint(b)

    if (
        entity1
        and entity2
        and event1
        and event2
        and entity1 == entity2
        and event1 == event2
    ):
        return True

    return False


# ----------------------------------------------------------

def _combined_score(a, b):

    entity = _entity_similarity(a, b)

    headline = _headline_similarity(a, b)

    keyword = _keyword_similarity(a, b)

    score = (

        entity * ENTITY_WEIGHT +

        headline * HEADLINE_WEIGHT +

        keyword * KEYWORD_WEIGHT

    )

    #
    # Strong bonus for matching
    # normalized entertainment event.
    #

    if _same_event(a, b):

        score += 0.20

    return min(score, 1.0)


# ----------------------------------------------------------

def _should_cluster(headline1, headline2):

    entity_score = _entity_similarity(
        headline1,
        headline2,
    )

    keyword_score = _keyword_similarity(
        headline1,
        headline2,
    )

    combined = _combined_score(
        headline1,
        headline2,
    )

    #
    # Exact event match wins.
    #

    if _same_event(
        headline1,
        headline2,
    ):
        return True

    #
    # Existing Version 4 logic.
    #

    if combined >= FINAL_THRESHOLD:
        return True

    if (
        entity_score >= ENTITY_THRESHOLD
        and keyword_score >= KEYWORD_THRESHOLD
    ):
        return True

    return False


# ----------------------------------------------------------

def _print_clusters(clusters):

    if not clusters:

        print(
            "No related story clusters found."
        )

        return

    print("STORY CLUSTERS")
    print("-----------------------------------\n")

    for number, cluster in enumerate(
        clusters,
        start=1,
    ):

        print(f"Cluster {number}")
        print("-----------------------------------")

        primary = cluster[0]

        print(
            f"Primary : {primary.get('headline','')}"
        )

        print("\nRelated:")

        scores = []

        for story in cluster[1:]:

            print(
                f"  • {story.get('headline','')}"
            )

            score = _combined_score(
                primary.get("headline",""),
                story.get("headline",""),
            )

            scores.append(score)

        if scores:

            confidence = (
                sum(scores) / len(scores)
            ) * 100

            print(
                f"\nConfidence : {confidence:.1f}%"
            )

        print()
 # ----------------------------------------------------------

def analyze_story_duplicates(stories):

    print("\n===================================")
    print("      STORY CONSOLIDATOR")
    print("      Version 5.0")
    print("===================================\n")

    print(f"Stories downloaded: {len(stories)}\n")

    used = set()

    clusters = []

    for i, story in enumerate(stories):

        if i in used:
            continue

        headline1 = story.get(
            "headline",
            "",
        )

        cluster = [story]

        used.add(i)

        for j in range(
            i + 1,
            len(stories),
        ):

            if j in used:
                continue

            headline2 = stories[j].get(
                "headline",
                "",
            )

            if _should_cluster(
                headline1,
                headline2,
            ):

                cluster.append(
                    stories[j]
                )

                used.add(j)

        if len(cluster) > 1:

            clusters.append(cluster)

    _print_clusters(clusters)

    print("===================================\n")

    #
    # Build final unique story list
    #

    unique_stories = []

    clustered_ids = set()

    for cluster in clusters:

        if not cluster:
            continue

        primary = cluster[0]

        primary["related_stories"] = cluster[1:]

        unique_stories.append(primary)

        for story in cluster:

            clustered_ids.add(
                id(story)
            )

    for story in stories:

        if id(story) in clustered_ids:
            continue

        story["related_stories"] = []

        unique_stories.append(story)

    print("===================================")
    print("STORY CONSOLIDATOR RESULTS")
    print("===================================")

    print(
        f"Original stories : {len(stories)}"
    )

    print(
        f"Unique stories   : {len(unique_stories)}"
    )

    print(
        f"Merged stories   : "
        f"{len(stories) - len(unique_stories)}"
    )

    print("===================================\n")

    return unique_stories


# ----------------------------------------------------------

if __name__ == "__main__":

    from engine.ai_news import get_top_stories

    stories = get_top_stories()

    analyze_story_duplicates(
        stories
    )       
