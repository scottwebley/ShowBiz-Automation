"""
===========================================
ShowBiz Weekly Streaming Guide
Version 1.1
===========================================

Generate and publish the
"New on Streaming" guide.

Architecture mirrors the
Weekly TV Guide.

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import write_guide
from engine.guides.streaming_guide_enricher import enrich_guide
from engine.guides.streaming_prompt import (
    TITLE,
    PROMPT,
)
from engine.guides.streaming_data import (
    get_streaming_guide,
)
from engine.publisher import publish_html


#
# WordPress Streaming Guide page.
#
PAGE_ID = 23783


def get_titles():

    return get_streaming_guide(
        limit=24
    )


def build_streaming_context(items):

    if not items:
        return ""

    context = """

CURRENT STREAMING DATA:

Use the following streaming
titles as the source for this
guide.

"""

    for item in items:

        context += f"""
Title: {item.get("title")}
Type: {item.get("media_type")}
Release Date: {item.get("release_date")}
Rating: {item.get("rating")}
Popularity: {item.get("popularity")}
Overview: {item.get("overview")}
Poster: {item.get("poster")}

"""

    return context


def build_guide():

    items = get_titles()

    streaming_context = build_streaming_context(
        items
    )

    prompt = (
        PROMPT
        + streaming_context
    )

    html = write_guide(
        title=TITLE,
        prompt=prompt,
    )

    with open(
        "streaming_ai_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(html)

    from engine.guides.streaming_trailer_finder import (
        trailer_button,
    )

    #
    # Add trailer button for each title.
    #
    for item in items:

        item["trailer"] = trailer_button(
            media_id=item["id"],
            title=item["title"],
            media_type=item["media_type"],
        )

    #
    # Enrich the guide once after
    # all trailers have been added.
    #
    enriched_html = enrich_guide(
        title=TITLE,
        html=html,
        items=items,
    )

    with open(
        "streaming_enriched_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            enriched_html
        )

    return enriched_html


def publish_guide():

    html = build_guide()

    return publish_html(
        page_id=PAGE_ID,
        html=html,
    )


def main():

    print()
    print("========================================")
    print("UPDATING STREAMING GUIDE")
    print("========================================")

    success = publish_guide()

    print()

    if success:

        print(
            "✓ Streaming Guide updated."
        )

        print(
            "✓ Saved streaming_ai_output.html"
        )

        print(
            "✓ Saved streaming_enriched_output.html"
        )

    else:

        print(
            "✗ Streaming Guide failed."
        )


if __name__ == "__main__":

    main()