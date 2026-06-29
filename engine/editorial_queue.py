"""
===========================================
ShowBiz Editorial Queue
Version 2.1
===========================================

Builds today's editorial queue from the
downloaded entertainment stories.

Version 2.1
-----------
• Removes duplicate stories
• Sorts by score
• Limits stories per category
"""

from collections import defaultdict

from engine.duplicate_detector import remove_duplicates

MAX_PER_CATEGORY = 3


def build_editorial_queue(stories):
    """
    Build an ordered editorial queue.
    """

    #
    # Remove duplicate stories first
    #

    stories = remove_duplicates(stories)

    #
    # Highest score first
    #

    stories = sorted(
        stories,
        key=lambda s: s.get("score", 0),
        reverse=True
    )

    queue = []

    category_count = defaultdict(int)

    for story in stories:

        category = story.get(
            "category",
            "Uncategorized"
        )

        if category_count[category] >= MAX_PER_CATEGORY:
            continue

        queue.append(story)

        category_count[category] += 1

    return queue


def print_queue(queue):

    print()
    print("=" * 70)
    print("TODAY'S EDITORIAL QUEUE")
    print("=" * 70)

    for i, story in enumerate(queue, start=1):

        score = story.get("score", 0)

        category = story.get(
            "category",
            "Uncategorized"
        )

        headline = story.get(
            "headline",
            "No Headline"
        )

        print(
            f"{i:2d}. "
            f"[{score:3d}] "
            f"[{category}] "
            f"{headline}"
        )

    print("=" * 70)

    print()
    print(f"Stories in queue: {len(queue)}")


def main():

    from engine.ai_news import get_top_stories

    print("Downloading stories...")

    stories = get_top_stories()

    print(f"✓ {len(stories)} stories downloaded.")

    queue = build_editorial_queue(stories)

    print_queue(queue)


if __name__ == "__main__":
    main()