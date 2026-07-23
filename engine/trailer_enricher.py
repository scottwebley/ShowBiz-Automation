"""
===========================================
Trailer Enricher
Version 2.0
===========================================

Adds an official YouTube trailer to
movie and TV trailer stories.

If no trailer is found, the article
is returned unchanged.
"""

import re

from engine.trailer_finder import find_trailer


TRAILER_KEYWORDS = (
    " trailer",
    " teaser",
    " first look",
    " official trailer",
    " official teaser",
    " sneak peek",
)


def is_trailer_story(story):
    """
    Determine whether this is a trailer story.
    """

    headline = (
        story.get("headline", "")
        if isinstance(story, dict)
        else ""
    ).lower()

    return any(
        keyword in headline
        for keyword in TRAILER_KEYWORDS
    )


def extract_title(headline):
    """
    Extract movie/TV title from headline.
    """

    if not headline:
        return ""

    headline = re.sub(
        r":.*$",
        "",
        headline,
        flags=re.IGNORECASE,
    )

    patterns = [

        r"^(.*?)\s+(Official\s+)?Trailer",

        r"^(.*?)\s+(Official\s+)?Teaser",

        r"^(.*?)\s+Gets?\s+New\s+Trailer",

        r"^(.*?)\s+First\s+Look",

        r"^(.*?)\s+Releases?\s+Trailer",

        r"^(.*?)\s+Debuts?\s+Trailer",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            headline,
            flags=re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

    words = headline.split()

    return " ".join(words[:4]).strip()
def enrich_article(article_html, story):
    """
    Add an embedded trailer to trailer stories.
    """

    try:

        if not article_html:
            return article_html

        if not isinstance(story, dict):
            return article_html

        if not is_trailer_story(story):
            return article_html

        headline = story.get("headline", "").strip()

        if not headline:
            return article_html

        title = extract_title(headline)

        if not title:
            return article_html

        trailer = find_trailer(title=title)

        if not trailer:
            return article_html

        if not trailer.get("embed_url"):
            return article_html

        trailer_html = f"""
<div class="showbiz-trailer-box">

<h2>🎬 Watch the Official Trailer</h2>

<div class="showbiz-trailer-video">

<iframe
    width="100%"
    height="500"
    src="{trailer['embed_url']}"
    title="{trailer['title']}"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
</iframe>

</div>

<p class="showbiz-trailer-credit">
Watch the official trailer on YouTube.
</p>

</div>
"""

        end_p = article_html.find("</p>")

        if end_p != -1:

            return (
                article_html[: end_p + 4]
                + "\n\n"
                + trailer_html
                + "\n\n"
                + article_html[end_p + 4 :]
            )

        return trailer_html + "\n\n" + article_html

    except Exception as exc:

        print("Trailer enrichment failed:", exc)

        return article_html


if __name__ == "__main__":

    sample_story = {
        "headline": "Clayface Trailer Teases Why It's Getting an R-Rating",
    }

    print(
        enrich_article(
            "<p>Opening paragraph.</p><p>Second paragraph.</p>",
            sample_story,
        )
    )