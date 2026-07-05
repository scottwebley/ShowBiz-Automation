"""
===========================================
ShowBiz Image Candidate Ranker
Version 2.0
===========================================

Purpose:
    Rank Media Library image candidates.

This module performs NO scoring.

Scoring is handled by:

    engine.image_scoring

Author:
    ShowBiz Automation
"""

from engine.image_scoring import score_candidate


def rank_candidates(story, candidates):
    """
    Returns candidates sorted best-first.
    """

    ranked = []
    seen = set()

    for candidate in candidates:

        key = (
            candidate.get("media_id"),
            candidate.get("filename", "").lower(),
        )

        if key in seen:
            continue

        seen.add(key)

        candidate = dict(candidate)

        score, reasons = score_candidate(
            story,
            candidate,
        )

        candidate["ranking_score"] = score
        candidate["ranking_reason"] = reasons

        ranked.append(candidate)

    ranked.sort(
        key=lambda c: (
            c["ranking_score"],
            c.get("title", "").lower(),
        ),
        reverse=True,
    )

    return ranked


if __name__ == "__main__":

    story = {
        "headline":
            "Taylor Swift and Travis Kelce "
            "celebrate wedding with Jay-Z",
    }

    candidates = [
        {
            "media_id": 1,
            "title": "Taylor Swift and Travis Kelce",
            "filename": "taylor-swift-travis-kelce.jpg",
        },
        {
            "media_id": 2,
            "title": "Aggregator Downloaded Image",
            "filename": "downloaded-image.jpg",
        },
        {
            "media_id": 3,
            "title": "Jay-Z",
            "filename": "jay-z.jpg",
        },
    ]

    ranked = rank_candidates(
        story,
        candidates,
    )

    print()

    for image in ranked:

        print(
            f"{image['ranking_score']:>4}  "
            f"{image['title']}"
        )

        for reason in image["ranking_reason"]:
            print(f"      • {reason}")

        print()