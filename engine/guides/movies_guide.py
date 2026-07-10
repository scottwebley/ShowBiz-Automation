"""
===========================================
ShowBiz Movies Guide
Version 1.0
===========================================

Purpose:
    Generate and publish the
    "What Movies To See Right Now"
    guide.

This module does NOT:

    • Talk directly to OpenAI
    • Talk directly to WordPress

Those responsibilities belong to:

    guide_writer.py
    guide_publisher.py

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import write_guide
from engine.guides.guide_publisher import publish_page


PAGE_ID = 23240

TITLE = "What Movies To See Right Now"


PROMPT = """
Write a premium ShowBiz guide page.

Requirements:

- Return HTML only.
- Do not return Markdown.
- Write in the ShowBiz editorial style.
- Mention that the guide is updated weekly.
- Write a short introduction.

Then recommend the 10 best movies currently
playing in theaters.

For each movie include:

<h2>Movie Title</h2>

A short editorial review explaining why
it's worth seeing.

End with a short conclusion encouraging
readers to return next week.

Do not invent release dates.

Do not include HTML, HEAD or BODY tags.

Return only the page content.
"""


def build_movies_guide():
    """
    Generate guide HTML.
    """

    return write_guide(
        title=TITLE,
        prompt=PROMPT,
    )


def publish_movies_guide():
    """
    Publish the Movies Guide.
    """

    html = build_movies_guide()

    return publish_page(
        page_id=PAGE_ID,
        title=TITLE,
        html=html,
    )


def main():

    print()
    print("========================================")
    print("SHOWBIZ MOVIES GUIDE")
    print("========================================")

    success = publish_movies_guide()

    print()

    if success:
        print("Movies Guide updated.")
    else:
        print("Movies Guide update failed.")


if __name__ == "__main__":
    main()