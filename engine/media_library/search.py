"""
===========================================
ShowBiz Media Library Search
Version 3.0
===========================================

Purpose:
    Fast local search of the WordPress Media Library.

Uses:
    media_cache.json

Public Functions:
    find_best_image(query)
    search(query)

Author:
    ShowBiz Automation
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


CACHE_FILE = (
    Path(__file__).parent / "media_cache.json"
)


@dataclass
class MediaResult:
    media_id: int
    score: int
    title: str
    filename: str
    url: str
    reason: str
    raw: dict


def _safe(value):

    if value is None:
        return ""

    if isinstance(value, dict):
        return str(value.get("rendered", ""))

    return str(value)


def normalize(text):

    text = _safe(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def load_media():

    print("\nLoading media cache...")

    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        media = json.load(f)

    print(f"Loaded {len(media)} media items.\n")

    return media


def score_item(item, query, words):

    score = 0
    reasons = []

    image_meta = (
        item.get("media_details", {})
        .get("image_meta", {})
    )

    fields = {
        "title": normalize(image_meta.get("title")),
        "caption": normalize(image_meta.get("caption")),
        "filename": normalize(item.get("filename")),
        "wp_title": normalize(_safe(item.get("title"))),
        "alt": normalize(item.get("alt_text")),
    }

    weights = {
        "title": 100,
        "caption": 90,
        "filename": 80,
        "wp_title": 70,
        "alt": 60,
    }

    # Exact phrase match

    for name, value in fields.items():

        if query and query in value:

            score += weights[name] * 20
            reasons.append(f"{name}:exact")

    # All words present

    for name, value in fields.items():

        if words and all(word in value for word in words):

            score += weights[name] * 8
            reasons.append(f"{name}:all_words")

    # Individual words

    for word in words:

        for name, value in fields.items():

            if word in value:

                score += weights[name]
                reasons.append(f"{name}:{word}")

    return score, reasons
def find_best_image(query: str) -> Optional[MediaResult]:

    query = normalize(query)

    if not query:
        return None

    words = query.split()

    media = load_media()

    results: List[MediaResult] = []

    for item in media:

        score, reasons = score_item(
            item,
            query,
            words,
        )

        if score == 0:
            continue

        title = (
            item.get("media_details", {})
            .get("image_meta", {})
            .get("title", "")
        )

        if not title:
            title = _safe(item.get("title"))

        results.append(
            MediaResult(
                media_id=item.get("id"),
                score=score,
                title=title,
                filename=item.get("filename", ""),
                url=item.get("source_url", ""),
                reason=", ".join(reasons),
                raw=item,
            )
        )

    if not results:
        return None

    results.sort(
        key=lambda r: (
            r.score,
            len(r.title),
        ),
        reverse=True,
    )

    return results[0]


def search(query: str):

    result = find_best_image(query)

    if result is None:

        print("\nNo matching image found.")

        return

    print()
    print("=" * 60)
    print("BEST MEDIA MATCH")
    print("=" * 60)

    print(f"Query      : {query}")
    print(f"Media ID   : {result.media_id}")
    print(f"Score      : {result.score}")
    print(f"Title      : {result.title}")
    print(f"Filename   : {result.filename}")
    print(f"URL        : {result.url}")
    print(f"Matched On : {result.reason}")


def main():

    print()
    print("=" * 60)
    print("SHOWBIZ MEDIA SEARCH")
    print("=" * 60)

    while True:

        query = input("\nSearch (blank to quit): ").strip()

        if not query:
            break

        search(query)


if __name__ == "__main__":
    main()