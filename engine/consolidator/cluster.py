# engine/consolidator/cluster.py

"""
ShowBiz Story Consolidator
Cluster Engine v7
"""

from engine.consolidator.similarity import (
    should_cluster,
    combined_score,
    similarity_report,
)


DEBUG = False


def build_clusters(stories):
    """
    Build clusters of related stories.
    """

    used = set()
    clusters = []

    for i, story in enumerate(stories):

        if i in used:
            continue

        primary = story
        headline1 = primary.get("headline", "")

        cluster = [primary]
        used.add(i)

        for j in range(i + 1, len(stories)):

            if j in used:
                continue

            candidate = stories[j]
            headline2 = candidate.get("headline", "")

            # Compare the complete stories instead of only headlines
            report = similarity_report(
                primary,
                candidate,
            )

            if DEBUG:

                print("\n----------------------------------------")
                print("COMPARE")
                print("----------------------------------------")
                print(f"A: {headline1}")
                print(f"B: {headline2}")

                print(
                    f"Headline : {report['headline']:.2f}"
                )

                if "body" in report:
                    print(
                        f"Body     : {report['body']:.2f}"
                    )

                print(
                    f"Keyword  : {report['keyword']:.2f}"
                )

                print(
                    f"Entity   : {report['entity']:.2f}"
                )

                if "tokens" in report:
                    print(
                        f"Tokens   : {report['tokens']:.2f}"
                    )

                print(
                    f"Combined : {report['combined']:.2f}"
                )

                print(
                    f"Event    : {report['same_event']}"
                )

            if should_cluster(
                primary,
                candidate,
            ):

                if DEBUG:
                    print(">>> CLUSTERED <<<")

                cluster.append(candidate)
                used.add(j)

        clusters.append(cluster)

    return clusters


def unique_story_list(clusters):
    """
    Convert clusters into the final
    unique story list.
    """

    unique = []

    for cluster in clusters:

        if not cluster:
            continue

        primary = cluster[0]
        primary["related_stories"] = cluster[1:]

        unique.append(primary)

    return unique


def cluster_score(cluster):

    if len(cluster) < 2:
        return 1.0

    primary = cluster[0]
    headline = primary.get("headline", "")

    scores = []

    for story in cluster[1:]:

        scores.append(
    combined_score(
        primary,
        story,
    )
)

    if not scores:
        return 1.0

    return sum(scores) / len(scores)


def cluster_count(clusters):

    total = 0

    for cluster in clusters:
        if len(cluster) > 1:
            total += len(cluster) - 1

    return total


def cluster_statistics(clusters):

    largest = 0

    for cluster in clusters:
        largest = max(largest, len(cluster))

    return {
        "clusters": sum(
            1 for c in clusters if len(c) > 1
        ),
        "merged": cluster_count(clusters),
        "largest_cluster": largest,
    }