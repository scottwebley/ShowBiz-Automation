"""
===========================================
ShowBiz Duplicate Detector
Version 1.0
===========================================

Removes obvious duplicate stories before they
enter the editorial queue.

Current duplicate rules:

• Same URL
• Very similar headline

Future versions can add semantic similarity
using embeddings or AI.
"""

import re


HEADLINE_SIMILARITY = 0.70


def normalize(text):
    """
    Normalize text for comparison.
    """

    text = text.lower()

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    words = text.split()

    return set(words)


def headline_similarity(a, b):
    """
    Simple Jaccard similarity.
    """

    words_a = normalize(a)
    words_b = normalize(b)

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)


def is_duplicate(story, accepted):

    url = story.get("url", "")

    headline = story.get("headline", "")

    for existing in accepted:

        #
        # Same URL
        #

        if (
            url
            and url == existing.get("url", "")
        ):
            return True

        #
        # Similar headline
        #

        similarity = headline_similarity(

            headline,

            existing.get("headline", "")

        )

        if similarity >= HEADLINE_SIMILARITY:

            return True

    return False


def remove_duplicates(stories):
    """
    Keep the highest-scoring version of each story.
    """

    stories = sorted(

        stories,

        key=lambda s: s.get("score", 0),

        reverse=True

    )

    accepted = []

    for story in stories:

        if not is_duplicate(

            story,

            accepted

        ):

            accepted.append(story)

    return accepted


if __name__ == "__main__":

    stories = [

        {
            "headline":
            "Director Carl Rinsch is sentenced to prison in $11M fraud case over unfinished Netflix show",
            "score": 105,
            "url": "1"
        },

        {
            "headline":
            "Hollywood director gets two and a half years in prison for defrauding Netflix",
            "score": 95,
            "url": "2"
        },

        {
            "headline":
            "Taylor Swift Announces New Tour",
            "score": 70,
            "url": "3"
        },

        {
            "headline":
            "Marvel Releases Fantastic Four Trailer",
            "score": 65,
            "url": "4"
        },

    ]

    print("=" * 60)
    print("SHOWBIZ DUPLICATE DETECTOR")
    print("=" * 60)

    unique = remove_duplicates(stories)

    print()

    for story in unique:

        print(

            f"[{story['score']:3d}] "

            f"{story['headline']}"

        )

    print()
    print(f"Stories kept: {len(unique)}")