"""
===========================================
ShowBiz Entity Titles
Version 1.0
===========================================

Extract quoted entertainment titles from
headlines.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


def extract_quoted_titles(headline: str) -> list[str]:
    """
    Extract quoted titles.

    Example:

        RIIZE's 'Do Your Dance'

    becomes

        Do Your Dance
    """

    titles: list[str] = []

    for title in re.findall(
        r"[\"']([^\"']+)[\"']",
        headline,
    ):

        title = title.strip()

        if len(title) < 2:
            continue

        if title not in titles:
            titles.append(title)

    return titles


if __name__ == "__main__":

    tests = [
        "RIIZE's 'Do Your Dance' Dance Challenge",
        'Taylor Swift announces "Midnights"',
        "The Rock Announces Big 'Moana 3' News",
        "No quoted title here",
    ]

    for test in tests:

        print()
        print("=" * 60)
        print(test)
        print("=" * 60)

        print(extract_quoted_titles(test))