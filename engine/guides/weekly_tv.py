"""
===========================================
ShowBiz Weekly TV Guide
Version 2.0
===========================================

Generate and publish the
"What To Watch Right Now" guide.

Architecture mirrors the
Weekly Movies Guide.

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import write_guide
from engine.guides.guide_enricher import enrich_guide
from engine.guides.tv_prompt import (
    TITLE,
    PROMPT,
)
from engine.guides.tv_data import (
    get_tv_guide,
)
from engine.publisher import publish_html


#
# Replace with the WordPress
# TV Guide page ID.
#
PAGE_ID = 23699


def get_shows():

    return get_tv_guide(
        limit=24
    )


def build_tv_context(shows):

    if not shows:
        return ""

    context = """

CURRENT TV DATA:

Use the following television
shows as the source for this
guide.

"""

    for show in shows:

        context += f"""
Title: {show.get("title")}
First Air Date: {show.get("release_date")}
Rating: {show.get("rating")}
Popularity: {show.get("popularity")}
Overview: {show.get("overview")}
Poster: {show.get("poster")}

"""

    return context


def build_guide():

    shows = get_shows()

    tv_context = build_tv_context(
        shows
    )

    prompt = (
        PROMPT
        + tv_context
    )

    html = write_guide(
        title=TITLE,
        prompt=prompt,
    )

    with open(
        "tv_ai_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            html
        )

        #
    # Add TV trailers
    #
    from engine.guides.trailer_finder import (
        trailer_button,
    )

    for show in shows:

        show["trailer"] = trailer_button(
            movie_id=show["id"],
            title=show["title"],
            media_type="tv",
        )

    enriched_html = enrich_guide(
    title=TITLE,
    html=html,
    movies=shows,
    guide_type="tv",
)

    with open(
        "tv_enriched_output.html",
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
    print("UPDATING TV GUIDE")
    print("========================================")

    success = publish_guide()

    print()

    if success:

        print(
            "✓ TV Guide updated."
        )

        print(
            "✓ Saved tv_ai_output.html"
        )

        print(
            "✓ Saved tv_enriched_output.html"
        )

    else:

        print(
            "✗ TV Guide failed."
        )


if __name__ == "__main__":

    main()