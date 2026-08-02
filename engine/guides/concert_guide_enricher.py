"""
===========================================
ShowBiz Concert Guide Enricher
Version 2.0
===========================================

Purpose:
    Convert AI-generated Concert Guide
    HTML into ShowBiz concert cards.

Author:
    ShowBiz Automation
"""
from urllib.parse import quote

import re
from datetime import datetime
import html

from engine.guides.html_builder import build_page
from engine.guides.movie_card_builder import (
    build_movie_card,
)


def current_date():

    return datetime.now().strftime(
        "%B %d, %Y"
    )


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

    import html as html_lib

    title = html_lib.unescape(title)

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


def find_concert(
    title,
    concerts,
):

    if not concerts:

        return None

    target = normalize_title(
        title
    )

    for concert in concerts:

        if (
            normalize_title(
                concert.get(
                    "title",
                    "",
                )
            )
            == target
        ):

            return concert

    return None


def concert_poster(
    title,
    concerts,
):

    concert = find_concert(
        title,
        concerts,
    )

    if not concert:

        return ""

    poster = concert.get(
        "poster",
        "",
    )

    if not poster:

        return ""

    return (
        f'<img src="{poster}" '
        f'alt="{title}">'
    )

from urllib.parse import quote

def affiliate_ticket_url(url):
    """
    Convert a Ticketmaster URL into an Impact affiliate deep link.
    """

    if not url:
        return ""

    encoded = quote(url, safe="")

    result = (
        "https://ticketmaster.evyy.net/"
        "c/6787125/264167/4272"
        f"?subId1={encoded}"
        f"&subId2={encoded}"
        f"&u={encoded}"
    )

    print("DEBUG affiliate:", encoded)
    print("DEBUG result:", result)

    return result


def build_tour_information(concert):

    if not concert:
        return ""

    rows = []

    if concert.get("artist"):
        rows.append(("Artist", concert["artist"]))

    if concert.get("event_date"):
        rows.append(("Next Show", concert["event_date"]))

    if concert.get("venue"):
        rows.append(("Venue", concert["venue"]))

    location = ", ".join(
        part
        for part in (
            concert.get("city", ""),
            concert.get("state", ""),
        )
        if part
    )

    if location:
        rows.append(("Location", location))

    if not rows:
        return ""

    info_html = """
<div class="showbiz-tour-info">
<h4>Concert Details</h4>
<ul>
"""

    for label, value in rows:
        info_html += (
            f"<li><strong>{label}:</strong> "
            f"{value}</li>\n"
        )

    ticket_url = affiliate_ticket_url(
        concert.get("url", "").strip()
    )

    if ticket_url:
        info_html += f"""
<div class="showbiz-ticket-buttons">
    <a
        class="showbiz-ticket-button"
        href="{html.escape(ticket_url, quote=True)}"
        target="_blank"
        rel="noopener sponsored">
        🎟 Buy Tickets
    </a>
</div>
"""

    info_html += """
</div>
"""

    return info_html

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

    block = block.replace(
        "</div>",
        "",
    )

    return block.strip()


def enrich_concert_blocks(
    html,
    concerts,
):

    import html as html_lib

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
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not title_match:
            break

        title = html_lib.unescape(
            re.sub(
                "<.*?>",
                "",
                title_match.group(1),
            ).strip()
        )

        concert = find_concert(
            title,
            concerts,
        )

        poster = concert_poster(
            title,
            concerts,
        )

        content = extract_content(
            block
        )

        if concert:

            content += build_tour_information(
                concert
            )

        replacement = build_movie_card(
            title=title,
            poster=poster,
            content=content,
            trailer="",
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
    concerts,
):

    html = clean_html(
        html
    )

    html = enrich_concert_blocks(
        html,
        concerts,
    )

    page = build_page(
        title=title,
        body=html,
        updated=current_date(),
    )

    # Concert Guide gets its own CSS class so we can
    # customize image sizes without affecting Movies,
    # TV or Streaming.
    page = page.replace(
        '<section class="showbiz-guide">',
        '<section class="showbiz-guide showbiz-concert-guide">',
        1,
    )

    return page


if __name__ == "__main__":

    sample_html = """
<div class="movie-item">
<h3>Sample Concert</h3>

<p>
This is a sample concert description.
</p>

</div>
"""

    sample_concerts = [
        {
            "title": "Sample Concert",
            "poster": "https://example.com/poster.jpg",
            "tour_start_date": "May 8, 2026",
            "tour_end_date": "October 17, 2026",
            "total_tour_dates": 42,
            "next_stop": "Kansas City • July 17, 2026",
            "final_stop": "Los Angeles • October 17, 2026",
        }
    ]

    print(
        enrich_guide(
            title="Concert Guide",
            html=sample_html,
            concerts=sample_concerts,
        )
    )