"""
===========================================
ShowBiz Guide Enricher
Version 1.0
===========================================

Purpose:
    Enhance AI-generated guide HTML.

This module does NOT:

    • Call OpenAI
    • Publish to WordPress
    • Find posters
    • Find trailers

Future enhancements:

    • Trailer buttons
    • Posters
    • Internal links
    • Updated dates
    • Editor's Pick styling

Author:
    ShowBiz Automation
"""

from datetime import datetime

from engine.guides.html_builder import build_page


def enrich_guide(
    title: str,
    html: str,
) -> str:
    """
    Enhance a guide before publishing.

    Args:
        title (str)
        html (str)

    Returns:
        str
    """

    updated = datetime.now().strftime(
        "%B %d, %Y"
    )

    html = html.strip()

    return build_page(
        title=title,
        body=html,
        updated=updated,
    )


if __name__ == "__main__":

    sample = """
    <p>This is a sample guide.</p>
    """

    print(
        enrich_guide(
            "Test Guide",
            sample,
        )
    )