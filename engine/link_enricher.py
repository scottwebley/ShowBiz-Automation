"""
===========================================
ShowBiz Link Enricher
Version 1.2
===========================================

Purpose:
    Add safe internal links to generated
    ShowBiz articles.

This module does NOT:

    - Call AI
    - Query WordPress
    - Add external links
    - Guess company destinations

It only enriches HTML when approved
internal mappings are available.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

import re
from html import escape


# --------------------------------------------------
# APPROVED INTERNAL LINKS
# --------------------------------------------------

# Only include destinations that are known
# to be correct.
#
# Do NOT add companies, people, movies,
# or organizations here unless a verified
# ShowBiz destination exists.

INTERNAL_LINKS = {
    "Oscars": "/awards-and-events/",
    "Emmys": "/awards-and-events/",
    "Emmy Awards": "/awards-and-events/",
    "Grammy Awards": "/awards-and-events/",
    "Tony Awards": "/awards-and-events/",
}


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def _already_linked(html):
    """
    Return existing anchor tags.
    """

    return re.findall(
        r"<a\b[^>]*>.*?</a>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def _has_anchor_around(
    html,
    term,
):
    """
    Prevent duplicate links.
    """

    anchors = _already_linked(html)

    term = term.lower()

    for anchor in anchors:

        if term in anchor.lower():

            return True

    return False


def _replace_first(
    html,
    term,
    url,
):
    """
    Replace first standalone phrase.
    """

    pattern = re.compile(
        rf"(?<![\w']){re.escape(term)}(?![\w'])",
        flags=re.IGNORECASE,
    )

    replacement = (
        f'<a href="{escape(url)}">'
        f'\\g<0>'
        f"</a>"
    )

    return pattern.sub(
        replacement,
        html,
        count=1,
    )


# --------------------------------------------------
# PUBLIC API
# --------------------------------------------------

def enrich_links(html):
    """
    Add approved internal links to article HTML.

    Returns:
        Updated HTML string
    """

    if not html:

        return html

    updated = html

    added = 0

    # Longest phrases first.

    links = sorted(
        INTERNAL_LINKS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for term, url in links:

        if added >= 3:

            break

        if _has_anchor_around(
            updated,
            term,
        ):

            continue

        pattern = re.compile(
            rf"(?<![\w']){re.escape(term)}(?![\w'])",
            flags=re.IGNORECASE,
        )

        if not pattern.search(updated):

            continue

        updated = _replace_first(
            updated,
            term,
            url,
        )

        added += 1

    return updated


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample = """
    <p>
    Disney announced a new project.
    The Emmys revealed this year's nominees.
    Marvel and Netflix also shared updates.
    </p>
    """

    print(
        enrich_links(sample)
    )