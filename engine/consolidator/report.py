# engine/consolidator/report.py

"""
ShowBiz Story Consolidator
Reporting Engine v7
"""

from engine.consolidator.cluster import cluster_score
from engine.consolidator.similarity import similarity_report
from engine.consolidator.fingerprint import fingerprint_string


def print_clusters(clusters):

    if not clusters:
        print("No related story clusters found.")
        return

    print("\n===================================")
    print("STORY CLUSTERS")
    print("===================================\n")

    number = 1

    for cluster in clusters:

        if len(cluster) < 2:
            continue

        primary = cluster[0]
        primary_headline = primary.get("headline", "")

        print(f"Cluster {number}")
        print("-----------------------------------")
        print(f"Primary : {primary_headline}")
        print(f"Fingerprint : {fingerprint_string(primary_headline)}")
        print()

        for story in cluster[1:]:

            headline = story.get("headline", "")

            scores = similarity_report(
                primary,
                story,
            )

            print(f"• {headline}")
            print(f"  Fingerprint : {fingerprint_string(headline)}")

            print(
                f"  Headline={scores['headline']:.2f}  "
                f"Body={scores['body']:.2f}  "
                f"Keyword={scores['keyword']:.2f}  "
                f"Entity={scores['entity']:.2f}  "
                f"Combined={scores['combined']:.2f}  "
                f"SameEvent={scores['same_event']}"
            )

            print()

        print(
            f"Cluster Confidence : {cluster_score(cluster) * 100:.1f}%"
        )

        print()

        number += 1


def print_summary(original_count, unique_stories):

    merged = original_count - len(unique_stories)

    print("===================================")
    print("STORY CONSOLIDATOR RESULTS")
    print("===================================")
    print(f"Original stories : {original_count}")
    print(f"Unique stories   : {len(unique_stories)}")
    print(f"Merged stories   : {merged}")
    print("===================================\n")