"""
===========================================
ShowBiz Homepage Guide Updater
Version 1.0
===========================================

Purpose:
    Update the Movies guide card on the
    ShowBiz homepage using the current
    Editor's Pick from movie_enriched_output.html.

Author:
    ShowBiz Automation
"""

import re
from pathlib import Path


MOVIE_GUIDE = Path("movie_enriched_output.html")
HOMEPAGE = Path("content/homepage.html")


MOVIES_LINK = (
    "https://showbiz.com/showbiz-guides/"
    "what-movies-to-see-right-now/"
)


def read_file(path: Path) -> str:

    if not path.exists():
        raise FileNotFoundError(path)

    return path.read_text(
        encoding="utf-8"
    )


def write_file(path: Path, text: str):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        text,
        encoding="utf-8",
    )


def extract_editors_pick(html: str):

    section = re.search(
        r"<h2>🎬 Editor's Pick</h2>(.*?)"
        r"<h2>🍿 Best Movies Right Now</h2>",
        html,
        flags=re.DOTALL,
    )

    if not section:
        raise ValueError(
            "Editor's Pick section not found."
        )

    block = section.group(1)

    image = re.search(
        r'<img[^>]+src="([^"]+)"',
        block,
        flags=re.DOTALL,
    )

    title = re.search(
        r"<h3>(.*?)</h3>",
        block,
        flags=re.DOTALL,
    )

    paragraphs = re.findall(
        r"<p>(.*?)</p>",
        block,
        flags=re.DOTALL,
    )

    poster = (
        image.group(1).strip()
        if image
        else ""
    )

    movie_title = (
        re.sub(
            "<.*?>",
            "",
            title.group(1),
        ).strip()
        if title
        else ""
    )

    summary = ""

    for p in paragraphs:

        text = re.sub(
            "<.*?>",
            "",
            p,
        ).strip()

        if not text:
            continue

        if text.startswith("Genre:"):
            continue

        summary = text
        break

    return {
        "poster": poster,
        "title": movie_title,
        "summary": summary,
    }
def update_movies_card(
    homepage_html: str,
    editor_pick: dict,
) -> str:

    pattern = (
    r'(<a\b[^>]*href="https://showbiz\.com/showbiz-guides/'
    r'what-movies-to-see-right-now/"[^>]*>)'
    r'(.*?)'
    r'(</a>)'
)

    match = re.search(
        pattern,
        homepage_html,
        flags=re.DOTALL,
    )

    if not match:
        raise ValueError(
            "Movies guide card not found."
        )

    card = match.group(2)

    card = re.sub(
        r'<img[^>]+src="[^"]+"',
        (
            '<img style="width: 100%; height: 220px; '
            'object-fit: cover; border-radius: 10px; '
            'margin-bottom: 15px;" '
            f'src="{editor_pick["poster"]}"'
        ),
        card,
        count=1,
        flags=re.DOTALL,
    )

    card = re.sub(
        r"<h3>.*?</h3>",
        (
            "<h3>🎬 "
            f'{editor_pick["title"]}'
            "</h3>"
        ),
        card,
        count=1,
        flags=re.DOTALL,
    )

    card = re.sub(
        r"<p>.*?</p>",
        (
            "<p>"
            f'{editor_pick["summary"]}'
            "</p>"
        ),
        card,
        count=1,
        flags=re.DOTALL,
    )

    return (
        homepage_html[:match.start()]
        + match.group(1)
        + card
        + match.group(3)
        + homepage_html[match.end():]
    )
def main():

    try:

        movie_html = read_file(
            MOVIE_GUIDE
        )

        homepage_html = read_file(
            HOMEPAGE
        )

        editor_pick = extract_editors_pick(
            movie_html
        )

        updated = update_movies_card(
            homepage_html,
            editor_pick,
        )

        write_file(
            HOMEPAGE,
            updated,
        )

        print(
            "✓ Homepage Movies card updated"
        )

        print(
            f'Title : {editor_pick["title"]}'
        )

    except Exception as e:

        print(
            "FAILED"
        )

        print(e)


if __name__ == "__main__":

    main()
