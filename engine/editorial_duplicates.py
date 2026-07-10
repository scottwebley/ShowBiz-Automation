"""
===========================================
ShowBiz Editorial Duplicates
Version 1.0
===========================================

Purpose:
    Detect duplicate or syndicated stories
    using deterministic headline
    normalization.

    This module contains NO workflow and
    NO scoring logic other than returning
    a duplicate penalty.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re


# ---------------------------------------------------------
# Common headline prefixes
# ---------------------------------------------------------

PREFIXES = (
    "breaking:",
    "exclusive:",
    "report:",
    "reports:",
    "opinion:",
    "review:",
    "analysis:",
    "watch:",
    "listen:",
    "photos:",
    "video:",
)


# ---------------------------------------------------------
# Noise words
# ---------------------------------------------------------

NOISE_WORDS = (
    "the",
    "a",
    "an",
)


_WORD_RE = re.compile(r"\b\w+\b")
_SPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")


def normalize_headline(headline):
    """
    Produce a deterministic normalized
    headline suitable for duplicate
    detection.
    """

    if not headline:
        return ""

    text = headline.lower().strip()

    for prefix in PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()

    text = _PUNCT_RE.sub(" ", text)

    words = [
        word
        for word in _WORD_RE.findall(text)
        if word not in NOISE_WORDS
    ]

    text = " ".join(words)

    return _SPACE_RE.sub(" ", text).strip()


def build_duplicate_groups(stories):
    """
    Return a dictionary keyed by normalized
    headline.

    Each value contains every story sharing
    that normalized headline.
    """

    groups = {}

    for story in stories:

        headline = (
            story.get("headline")
            or story.get("title")
            or ""
        )

        key = normalize_headline(headline)

        if not key:
            continue

        groups.setdefault(key, []).append(story)

    return groups


def duplicate_penalty(story, groups):
    """
    Return a deterministic penalty based on
    the number of duplicate stories.

    The preferred source selection remains
    the responsibility of
    editorial_sources.py.
    """

    headline = (
        story.get("headline")
        or story.get("title")
        or ""
    )

    key = normalize_headline(headline)

    duplicates = groups.get(key, [])

    if len(duplicates) <= 1:
        return 0

    #
    # Penalty increases with duplicate count
    #

    return (len(duplicates) - 1) * 40


if __name__ == "__main__":

    sample = [

        {
            "headline":
            "Breaking: Disney Announces New Pixar Film"
        },

        {
            "headline":
            "Disney Announces New Pixar Film"
        },

        {
            "headline":
            "Exclusive: Disney Announces New Pixar Film"
        },

        {
            "headline":
            "Warner Bros Reveals New DC Trailer"
        },
    ]

    groups = build_duplicate_groups(sample)

    for story in sample:

        print(
            normalize_headline(story["headline"]),
            duplicate_penalty(story, groups),
        )