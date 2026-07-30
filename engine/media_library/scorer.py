"""
===========================================
ShowBiz Media Scorer
Version 4.1
===========================================

Purpose:
    Score Media Library candidates.

Scoring priority:

    1. image_meta.title exact match
    2. image_meta.caption exact match
    3. image_meta title/caption full-name match
    4. filename fallback
    5. WordPress title fallback

Version 4.1
-----------
• Prevents single-word organization searches
  (Disney, Pixar, Sony, Netflix, etc.)
  from being dominated by weak caption matches.
• Multi-word searches continue to behave exactly
  as before.

Ignored:
    - SEO fields
    - attachment descriptions
    - rendered HTML
    - imported article text

Author:
    ShowBiz Automation
"""

from engine.media_library.normalize import (
    normalize,
    safe,
)
print("USING SCORER:", __file__)

STOP_WORDS = {
    "the",
    "of",
    "and",
    "a",
    "an",
    "for",
    "in",
    "on",
    "at",
    "with",
}


def _tokens(text):

    return [
        word
        for word in normalize(text).split()
        if len(word) >= 3
        and word not in STOP_WORDS
    ]


def _clean_words(text):

    return [
        word.lower()
        for word in _tokens(text)
    ]


def _metadata_field(
    item,
    key,
):

    details = item.get(
        "media_details",
        {},
    )

    if not isinstance(
        details,
        dict,
    ):
        return ""

    image_meta = details.get(
        "image_meta",
        {},
    )

    if not isinstance(
        image_meta,
        dict,
    ):
        return ""

    return normalize(
        safe(
            image_meta.get(
                key
            )
        )
    )


def _wordpress_title(
    item,
):

    title = item.get(
        "title",
        "",
    )

    if isinstance(
        title,
        dict,
    ):

        return normalize(
            safe(
                title.get(
                    "rendered"
                )
            )
        )

    return normalize(
        safe(
            title
        )
    )


def _filename(
    item,
):

    return normalize(
        safe(
            item.get(
                "filename"
            )
        )
    )


def score_item(item, query, query_words):
    print(">>> SCORE_ITEM CALLED <<<")

    score = 0
    reasons = []

    try:
        title = _metadata_field(item, "title")
        caption = _metadata_field(item, "caption")
        filename = _filename(item)
        wp_title = _wordpress_title(item)

        parent_title = normalize(
            safe(item.get("parent_post_title"))
        )

        parent_slug = normalize(
            safe(item.get("parent_post_slug"))
        )

        parent_excerpt = normalize(
            safe(item.get("parent_post_excerpt"))
        )

        print(f"ITEM {item.get('id')}")
        print(f"  query        : {query}")
        print(f"  title        : {title}")
        print(f"  caption      : {caption}")
        print(f"  filename     : {filename}")
        print(f"  wp_title     : {wp_title}")
        print(f"  parent_title : {parent_title}")
        print(f"  parent_slug  : {parent_slug}")

        query_words = [w.lower() for w in query_words if w]

        title_tokens = set(_clean_words(title))
        caption_tokens = set(_clean_words(caption))
        filename_tokens = set(_clean_words(filename))
        wp_tokens = set(_clean_words(wp_title))

        parent_title_tokens = set(_clean_words(parent_title))
        parent_slug_tokens = set(_clean_words(parent_slug))
        parent_excerpt_tokens = set(_clean_words(parent_excerpt))

        # Exact matches

        if query_words and all(w in title_tokens for w in query_words):
            score += 500
            reasons.append("meta_title")

        if query_words and all(w in caption_tokens for w in query_words):
            score += 400
            reasons.append("meta_caption")

        if query_words and all(w in filename_tokens for w in query_words):
            score += 300
            reasons.append("filename")

        if query_words and all(w in wp_tokens for w in query_words):
            score += 200
            reasons.append("wp_title")

        if query_words and all(w in parent_title_tokens for w in query_words):
            score += 450
            reasons.append("parent_title")

        if query_words and all(w in parent_slug_tokens for w in query_words):
            score += 425
            reasons.append("parent_slug")

        if query_words and all(w in parent_excerpt_tokens for w in query_words):
            score += 150
            reasons.append("parent_excerpt")

        # Partial matches

        for word in query_words:

            if word in filename_tokens:
                score += 50

            if word in title_tokens:
                score += 40

            if word in caption_tokens:
                score += 30

            if word in wp_tokens:
                score += 20

            if word in parent_title_tokens:
                score += 60

            if word in parent_slug_tokens:
                score += 50

            if word in parent_excerpt_tokens:
                score += 10

        print(f"  SCORE={score} REASONS={reasons}")

        return score, reasons

    except Exception as e:
        print(f"SCORE ERROR: {e}")
        return 0, []