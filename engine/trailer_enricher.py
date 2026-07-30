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
print(">>> LOADED trailer_enricher.py v2 <<<")


TRAILER_KEYWORDS = (
    "trailer",
    "teaser",
    "first look",
    "official trailer",
    "official teaser",
    "sneak peek",
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

    print(f"HEADLINE: {headline!r}")

    return any(
        keyword in headline
        for keyword in TRAILER_KEYWORDS
    )


def extract_title(headline):
    """
    Extract movie/TV title from trailer headlines while preserving
    titles that legitimately contain a colon.
    """

    if not headline:
        return ""

    headline = headline.strip(" '\"“”‘’")

    patterns = [

        # Jumanji: Open World Trailer Takes...
        r"^(.*?)\s+Trailer\s+(?:Takes|Brings|Drops|Debuts|Launches|Reveals)",

        # Superman Official Trailer
        r"^(.*?)\s+(Official\s+)?Trailer",

        # Superman Official Teaser
        r"^(.*?)\s+(Official\s+)?Teaser",

        # Gets New Trailer
        r"^(.*?)\s+Gets?\s+New\s+Trailer",

        # First Look
        r"^(.*?)\s+First\s+Look",

        # Releases Trailer
        r"^(.*?)\s+Releases?\s+Trailer",

        # Debuts Trailer
        r"^(.*?)\s+Debuts?\s+Trailer",
    ]

    for pattern in patterns:
        match = re.search(pattern, headline, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" '\"“”‘’:-")

    words = headline.split()
    return " ".join(words[:6]).strip(" '\"“”‘’:-")
def enrich_article(article, story):
    """
    Add an embedded trailer to trailer stories.
    """

    print(">>> ENTERING enrich_article() <<<", flush=True)

    try:

        if not article or not isinstance(article, dict):
            return article

        if not isinstance(story, dict):
            return article

        if not is_trailer_story(story):
            return article

        headline = story.get("headline", "").strip()

        if not headline:
            return article

        title = extract_title(headline)

        if not title:
            return article

        print(f"Trailer search title: {title}")

        trailer = find_trailer(title=title)

        if not trailer:
            return article

        if not trailer.get("embed_url"):
            return article

        content = article.get("content", "")

        if not content:
            return article

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

        end_p = content.find("</p>")

        if end_p != -1:
            article["content"] = (
                content[: end_p + 4]
                + "\n\n"
                + trailer_html
                + "\n\n"
                + content[end_p + 4 :]
            )
        else:
            article["content"] = trailer_html + "\n\n" + content

        return article

    except Exception as exc:

        print("Trailer enrichment failed:", exc)

        return article


if __name__ == "__main__":

    sample_story = {
        "headline": "Clayface Trailer Teases Why It's Getting an R-Rating",
    }

    sample_article = {
        "content": "<p>Opening paragraph.</p><p>Second paragraph.</p>",
    }

    result = enrich_article(sample_article, sample_story)

    print("\n==============================")
    print("RESULT")
    print("==============================")
    print(result["content"])