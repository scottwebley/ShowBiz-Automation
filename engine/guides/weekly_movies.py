"""
===========================================
ShowBiz Weekly Movies Guide
Version 1.2
===========================================

Generate and publish the
"What Movies To See Right Now"
guide.

Workflow:

    Prompt
        ↓
    AI Writer
        ↓
    Guide Enricher
        ↓
    Publisher

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import write_guide
from engine.guides.guide_enricher import enrich_guide
from engine.guides.movie_prompt import (
    TITLE,
    PROMPT,
)
from engine.publisher import publish_html


PAGE_ID = 23240


def build_guide():
    """
    Generate and enrich the Movies Guide.
    """

    html = write_guide(
        title=TITLE,
        prompt=PROMPT,
    )

    return enrich_guide(
        title=TITLE,
        html=html,
    )


def publish_guide():
    """
    Publish the Movies Guide.
    """

    html = build_guide()

    return publish_html(
        page_id=PAGE_ID,
        html=html,
    )


def main():

    print()
    print("========================================")
    print("UPDATING MOVIES GUIDE")
    print("========================================")

    success = publish_guide()

    print()

    if success:
        print("✓ Movies Guide updated.")
    else:
        print("✗ Movies Guide failed.")


if __name__ == "__main__":
    main()