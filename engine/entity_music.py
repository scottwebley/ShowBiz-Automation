"""
===========================================
ShowBiz Entity Music
Version 1.0
===========================================

Extract single-word music artist entities.

This module performs NO searching.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


def extract_music_artists(
    headline: str,
    organizations: list[str],
) -> list[str]:
    """
    Extract likely single-word music artists
    written in ALL CAPS.

    Example:

        BTS announces new tour

    becomes

        ["BTS"]
    """

    artists: list[str] = []

    excluded = {
        token.lower()
        for value in organizations
        for token in re.findall(
            r"[A-Za-z0-9']+",
            value,
        )
    }

    for word in re.findall(
        r"\b[A-Z][A-Za-z0-9']+\b",
        headline,
    ):

        if not word.isupper():
            continue

        if len(word) < 3:
            continue

        if word.lower() in excluded:
            continue

        if word not in artists:
            artists.append(word)

    return artists


if __name__ == "__main__":

    tests = [
        (
            "BTS announces new world tour",
            [],
        ),
        (
            "RIIZE releases new single",
            [],
        ),
        (
            "HBO announces documentary",
            ["HBO"],
        ),
        (
            "Taylor Swift begins tour",
            [],
        ),
    ]

    for headline, orgs in tests:

        print()
        print("=" * 60)
        print(headline)
        print("=" * 60)

        print(
            extract_music_artists(
                headline,
                orgs,
            )
        )