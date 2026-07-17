"""
===========================================
ShowBiz Streaming Guide Enricher
Version 1.0
===========================================

Purpose:
    Transform Streaming Guide HTML
    into enriched ShowBiz cards.

Uses trailer HTML already generated
by streaming_trailer_finder.py.

Author:
    ShowBiz Automation
"""

import re
from datetime import datetime

from engine.guides.html_builder import build_page
from engine.guides.poster_finder import poster_html
from engine.guides.movie_card_builder import build_movie_card


def current_date():
    return datetime.now().strftime("%B %d, %Y")


def remove_h1(html):

    return re.sub(
        r"<h1[^>]*>.*?</h1>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def clean_html(html):

    return remove_h1(
        html.strip()
    )


def normalize_title(title):

    if not title:
        return ""

    title = title.lower()

    title = re.sub(
        r"\(\d{4}\)",
        "",
        title,
    )

    title = re.sub(
        r"\b\d{4}\b",
        "",
        title,
    )

    title = re.sub(
        r"[^a-z0-9]+",
        " ",
        title,
    )

    return " ".join(
        title.split()
    )


def find_item(title, items):

    if not items:
        return None

    normalized = normalize_title(
        title
    )

    for item in items:

        if (
            normalize_title(
                item.get(
                    "title",
                    "",
                )
            )
            == normalized
        ):

            return item

    return None


def movie_poster(
    title,
    items=None,
):

    item = find_item(
        title,
        items,
    )

    if item:

        poster = item.get(
            "poster",
            "",
        )

        if poster:

            return (
                '<img '
                f'src="{poster}" '
                f'alt="{title}">'
            )

    return poster_html(
        title
    )
def extract_content(block):

    block = re.sub(
        r"<h3>.*?</h3>",
        "",
        block,
        flags=re.IGNORECASE | re.DOTALL,
    )

    block = re.sub(
        r'<div[^>]*class=["\']movie-item["\'][^>]*>',
        "",
        block,
        flags=re.IGNORECASE | re.DOTALL,
    )

    block = re.sub(
        r'<div[^>]*class=["\']trailer["\'][^>]*>\s*'
        r'(?:TRAILER_BUTTON)?\s*</div>',
        "",
        block,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return block.strip()


def enrich_movie_blocks(
    html,
    items=None,
):

    start_tag = '<div class="movie-item">'

    while start_tag in html:

        start = html.find(
            start_tag
        )

        depth = 0
        end = None
        position = start

        while position < len(html):

            open_div = html.find(
                "<div",
                position,
            )

            close_div = html.find(
                "</div>",
                position,
            )

            if close_div == -1:
                break

            if (
                open_div != -1
                and open_div < close_div
            ):

                depth += 1
                position = open_div + 4

            else:

                depth -= 1
                position = close_div + 6

                if depth == 0:

                    end = position
                    break

        if end is None:
            break

        block = html[start:end]

        title_match = re.search(
            r"<h3>(.*?)</h3>",
            block,
            re.IGNORECASE | re.DOTALL,
        )

        if not title_match:
            break

        title = re.sub(
            "<.*?>",
            "",
            title_match.group(1),
        ).strip()

        item = find_item(
            title,
            items,
        )

        poster = movie_poster(
            title,
            items,
        )

        trailer = ""
        platform = ""
        platform_logo = ""
        trailer_url = ""
        watch_url = ""

        if item:

            trailer = item.get(
                "trailer",
                "",
            )

            platform = item.get(
                "platform",
                "",
            )

            platform_logo = item.get(
                "platform_logo",
                "",
            )

            trailer_url = item.get(
                "trailer_url",
                "",
            )

            watch_url = item.get(
                "watch_url",
                "",
            )

        replacement = build_movie_card(
            title=title,
            poster=poster,
            content=extract_content(
                block
            ),
            trailer=trailer,
            platform=platform,
            platform_logo=platform_logo,
            trailer_url=trailer_url,
            watch_url=watch_url,
        )

        html = (
            html[:start]
            + replacement
            + html[end:]
        )

    return html
def enrich_guide(
    title,
    html,
    items=None,
):

    html = clean_html(
        html
    )

    html = enrich_movie_blocks(
        html,
        items,
    )

    return build_page(
        title=title,
        body=html,
        updated=current_date(),
    )


if __name__ == "__main__":

    print(
        enrich_guide(
            title="Streaming",
            html="""
<div class="movie-item">
<h3>The Odyssey</h3>
<p>Example description.</p>
<div class="trailer">
TRAILER_BUTTON
</div>
</div>
""",
            items=[
                {
                    "title": "The Odyssey",
                    "poster": "poster.jpg",
                    "trailer": '<a href="#">Trailer</a>',
                }
            ],
        )
    )