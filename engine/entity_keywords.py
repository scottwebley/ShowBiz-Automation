"""
===========================================
ShowBiz Entity Keywords
Version 1.0
===========================================

Extract generic search keywords from
entertainment headlines.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


def extract_keywords(
    headline: str,
    excluded_values: list[str],
    ignore_keywords: set[str],
) -> list[str]:
    """
    Extract generic keywords after excluding
    entities already identified.
    """

    excluded = set()

    for value in excluded_values:

        for token in re.findall(
            r"[A-Za-z0-9']+",
            value,
        ):
            excluded.add(token.lower())

    skip_words = {
        *ignore_keywords,
        "your",
        "their",
        "listeners",
        "listener",
        "surpasses",
        "decoding",
        "views",
        "view",
        "challenge",
        "challenges",
        "announces",
        "announced",
        "expected",
        "breaking",
        "latest",
        "more",
        "also",
        "has",
        "have",
        "had",
    }

    keywords: list[str] = []

    for word in re.findall(
        r"[A-Za-z0-9']+",
        headline,
    ):

        clean = word.strip(
            ".,:;!?()[]{}\"'"
        )

        if not clean:
            continue

        lower = clean.lower()

        if len(lower) < 4:
            continue

        if lower in excluded:
            continue

        if lower in skip_words:
            continue

        if clean not in keywords:
            keywords.append(clean)

    return keywords


if __name__ == "__main__":

    headline = (
        "Taylor Swift announces new concert "
        "after Netflix documentary"
    )

    excluded = [
        "Taylor Swift",
        "Netflix",
    ]

    ignore = {
        "after",
        "news",
        "movie",
        "show",
        "today",
    }

    print(
        extract_keywords(
            headline,
            excluded,
            ignore,
        )
    )