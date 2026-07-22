"""
story_consolidator.py
ShowBiz Story Consolidator v3.0

Version 3 consolidates duplicate entertainment stories
into a single primary story while preserving related
coverage for the AI Writer.
"""

import re
from difflib import SequenceMatcher

SIMILARITY_THRESHOLD = 0.72
KEYWORD_THRESHOLD = 0.45

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been",
    "being", "by", "for", "from", "how", "if", "in",
    "into", "is", "it", "its", "of", "on", "or",
    "that", "the", "their", "this", "to", "was",
    "were", "what", "when", "where", "which", "who",
    "why", "will", "with",

    "after",
    "amid",
    "before",
    "despite",
    "during",
    "explains",
    "explained",
    "latest",
    "new",
    "report",
    "reports",
    "says",
    "say",
    "reveals",
    "revealed",
    "first",
    "look",
    "review",
    "exclusive",
    "breaking"
}


def _normalize(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[^\w\s]", " ", text)

    words = []

    for word in text.split():

        if word not in STOP_WORDS:

            words.append(word)

    return " ".join(words)


def _keywords(text):

    words = set()

    for word in _normalize(text).split():

        if len(word) >= 3:

            words.add(word)

    return words


def _headline_similarity(a, b):

    return SequenceMatcher(
        None,
        _normalize(a),
        _normalize(b)
    ).ratio()


def _keyword_similarity(a, b):

    a_words = _keywords(a)
    b_words = _keywords(b)

    if not a_words or not b_words:
        return 0.0

    overlap = len(a_words & b_words)

    union = len(a_words | b_words)

    return overlap / union


def _combined_score(a, b):

    headline = _headline_similarity(a, b)

    keyword = _keyword_similarity(a, b)

    return (
        headline * 0.45 +
        keyword * 0.55
    )


def analyze_story_duplicates(stories):

    print("\n===================================")
    print("      STORY CONSOLIDATOR")
    print("      Version 3.0")
    print("===================================\n")

    print(f"Stories downloaded: {len(stories)}\n")

    used = set()

    clusters = []

    for i, story in enumerate(stories):

        if i in used:
            continue

        headline1 = story.get("headline", "")

        cluster = [story]

        used.add(i)

        for j in range(i + 1, len(stories)):

            if j in used:
                continue

            headline2 = stories[j].get("headline", "")

            headline_score = _headline_similarity(
                headline1,
                headline2
            )

            keyword_score = _keyword_similarity(
                headline1,
                headline2
            )

            combined = _combined_score(
                headline1,
                headline2
            )

            if (
                combined >= SIMILARITY_THRESHOLD
                or keyword_score >= KEYWORD_THRESHOLD
            ):

                cluster.append(stories[j])

                used.add(j)

        if len(cluster) > 1:

            clusters.append(cluster)

    if not clusters:

        print("No related story clusters found.")

    else:

        print("STORY CLUSTERS")
        print("-----------------------------------\n")

        for number, cluster in enumerate(clusters, start=1):

            print(f"Cluster {number}")
            print("-----------------------------------")

            for story in cluster:

                print(f"• {story.get('headline', '')}")

            scores = []

            first = cluster[0].get("headline", "")

            for story in cluster[1:]:

                score = _combined_score(
                    first,
                    story.get("headline", "")
                )

                scores.append(score)

            if scores:

                confidence = (
                    sum(scores) / len(scores)
                ) * 100

                print(
                    f"\nConfidence: "
                    f"{confidence:.1f}%"
                )

            print()
            print("===================================\n")

    # ----------------------------------------------------------
    # Version 3:
    # Build the final unique story list
    # ----------------------------------------------------------

    unique_stories = []
    clustered_ids = set()

    # Keep one primary story from each cluster
    for cluster in clusters:

        if not cluster:
            continue

        primary = cluster[0]

        primary["related_stories"] = cluster[1:]

        unique_stories.append(primary)

        for story in cluster:

            clustered_ids.add(id(story))

    # Add stories that never appeared in a cluster
    for story in stories:

        if id(story) not in clustered_ids:

            story["related_stories"] = []

            unique_stories.append(story)

    print("===================================")
    print("STORY CONSOLIDATOR RESULTS")
    print("===================================")
    print(f"Original stories : {len(stories)}")
    print(f"Unique stories   : {len(unique_stories)}")
    print(f"Merged stories   : {len(stories) - len(unique_stories)}")
    print("===================================\n")

    return unique_stories