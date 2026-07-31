"""
===========================================
ShowBiz Guide Enricher
Version 4.5
===========================================

Purpose:
    Transform structured guide HTML
    into enriched ShowBiz movie layouts.

Features:
    - TMDb poster support
    - Media Library poster fallback
    - Trailer replacement
    - Movie card builder integration
    - Improved movie title matching

Author:
    ShowBiz Automation
"""

import re
from datetime import datetime

from engine.guides.html_builder import build_page
from engine.guides.trailer_finder import trailer_button
from engine.guides.tv_trailer_finder import trailer_button as tv_trailer_button
from engine.guides.poster_finder import poster_html
from engine.guides.movie_card_builder import build_movie_card


def current_date() -> str:
    return datetime.now().strftime("%B %d, %Y")


def remove_h1(html: str) -> str:
    return re.sub(
        r"<h1[^>]*>.*?</h1>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def clean_html(html: str) -> str:
    return remove_h1(
        html.strip()
    )


def normalize_title(title: str) -> str:
    """
    Normalize movie titles for matching.

    Removes:
        - punctuation
        - years
        - extra whitespace
    """

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


def find_tmdb_poster(title, movies):
    if not movies:
        print(f"[POSTER] No movie list supplied for: {title}")
        return ""

    normalized_title = normalize_title(title)

    for movie in movies:
        movie_title = normalize_title(
            movie.get("title", "")
        )

        if movie_title == normalized_title:
            print(f"[POSTER] MATCH: {title} -> {movie.get('title')}")
            return movie.get("poster", "")

    print(f"[POSTER] NO MATCH: {title}")
    print(f"[POSTER] Normalized: {normalized_title}")

    print("[POSTER] Available titles:")
    for movie in movies:
        print(f"    - {movie.get('title', '')}")

    return ""

def movie_poster(title, movies=None):
    print(f"[ENTER movie_poster] {title}")

    if movies:
        for movie in movies:
            if normalize_title(movie.get("title", "")) == normalize_title(title):

                print(f"[POSTER DATA] title={movie.get('title')}")
                print(f"[POSTER DATA] id={movie.get('id')}")
                print(f"[POSTER DATA] poster={repr(movie.get('poster'))}")

                poster = movie.get("poster", "")

                if poster:
                    return (
                        '<img '
                        f'src="{poster}" '
                        f'alt="{title}">'
                    )

                break

    print(f"[POSTER DATA] No TMDb poster for {title}")
    return poster_html(title)


def extract_content(block: str) -> str:
    """
    Remove title and trailer placeholder.
    """

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


def find_movie_id(title, movies):

    if not movies:
        return None

    normalized_title = normalize_title(
        title
    )

    for movie in movies:

        movie_title = normalize_title(
            movie.get(
                "title",
                "",
            )
        )

        if movie_title == normalized_title:

            return movie.get(
                "id"
            )

    return None


def enrich_movie_blocks(
    html: str,
    movies=None,
    guide_type="movie",
) -> str:
    """
    Convert every movie-item block into a ShowBiz movie card.
    """

    print("[ENRICH] enrich_movie_blocks called")
    print(f"[ENRICH] guide_type={guide_type}")
    print(f"[ENRICH] movies={len(movies) if movies else 0}")

    start_tag = '<div class="movie-item">'
    replacements = []

    search_pos = 0

    while True:

        start = html.find(start_tag, search_pos)

        if start == -1:
            break

        depth = 0
        pos = start
        end = None

        while pos < len(html):

            open_div = html.find("<div", pos)
            close_div = html.find("</div>", pos)

            if close_div == -1:
                break

            if open_div != -1 and open_div < close_div:
                depth += 1
                pos = open_div + 4
            else:
                depth -= 1
                pos = close_div + 6

                if depth == 0:
                    end = pos
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
            search_pos = end
            continue

        title = re.sub(
            "<.*?>",
            "",
            title_match.group(1),
        ).strip()

        print(f"[ENRICH] Processing: {title}")

        content = extract_content(block)

        poster = movie_poster(
            title,
            movies,
        )

        movie_id = find_movie_id(
            title,
            movies,
        )

        print(f"[ENRICH] movie_id={movie_id}")
        print(f"[ENRICH] poster={'YES' if poster else 'NO'}")

        if guide_type == "tv":
            trailer = tv_trailer_button(
                movie_id,
                title,
            )
        else:
            trailer = trailer_button(
                movie_id,
                title,
            )

        replacement = build_movie_card(
            title=title,
            poster=poster,
            content=content,
            trailer=trailer,
        )

        replacements.append((start, end, replacement))
        search_pos = end

    for start, end, replacement in reversed(replacements):
        html = html[:start] + replacement + html[end:]

    return html


def enrich_guide(
    title: str,
    html: str,
    movies=None,
    guide_type="movie",
) -> str:

    html = clean_html(
        html
    )

    html = enrich_movie_blocks(
        html,
        movies,
        guide_type,
    )

    return build_page(
        title=title,
        body=html,
        updated=current_date(),
    )


if __name__ == "__main__":

    print(
        enrich_guide(
            "Movies",
            """
<div class="movie-item">
<h3>Dune: Part Two (2024)</h3>
<p>Review.</p>
<div class="trailer">
TRAILER_BUTTON
</div>
</div>
""",
            [
                {
                    "id": 693134,
                    "title": "Dune: Part Two",
                    "poster": "poster.jpg",
                }
            ],
        )
    )