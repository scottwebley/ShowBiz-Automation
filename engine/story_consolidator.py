# engine/story_consolidator.py

"""
ShowBiz Story Consolidator v7
Public API unchanged.
"""

from engine.consolidator.cluster import (
    build_clusters,
    unique_story_list,
)

from engine.consolidator.report import (
    print_clusters,
    print_summary,
)


def analyze_story_duplicates(stories):

    print("\n===================================")
    print("      STORY CONSOLIDATOR")
    print("      Version 7.0")
    print("===================================\n")

    print(f"Stories downloaded: {len(stories)}\n")

    if not stories:
        print("No stories supplied.\n")
        return []

    print("===================================")
    print("INPUT STORIES")
    print("===================================")

    for i, story in enumerate(stories, 1):

        if isinstance(story, dict):
            headline = (
                story.get("headline")
                or story.get("title")
                or story.get("name")
                or "(no headline)"
            )

            source = (
                story.get("source")
                or story.get("publisher")
                or story.get("site")
                or story.get("feed")
                or "Unknown"
            )
        else:
            headline = str(story)
            source = "Unknown"

        print(f"{i:02d}. [{source}] {headline}")

    print("===================================")
    print(f"Total stories loaded: {len(stories)}")
    print("===================================\n")

    clusters = build_clusters(stories)

    duplicate_clusters = [
        cluster
        for cluster in clusters
        if len(cluster) > 1
    ]

    print_clusters(duplicate_clusters)

    unique_stories = unique_story_list(clusters)

    print_summary(
        len(stories),
        unique_stories,
    )

    return unique_stories


if __name__ == "__main__":

    from engine.ai_news import get_top_stories

    stories = get_top_stories()

    analyze_story_duplicates(stories)