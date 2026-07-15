"""
===========================================
ShowBiz Media Scorer
Version 4.0
===========================================

Purpose:
    Score Media Library candidates.

Scoring priority:

    1. image_meta.title exact match
    2. image_meta.caption exact match
    3. image_meta title/caption full-name match
    4. filename fallback
    5. WordPress title fallback

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



def score_item(
    item,
    query,
    words=None,
):

    reasons = []

    query_phrase = normalize(
        query
    )

    query_words = _clean_words(
        query
    )

    if not query_words:
        return 0, reasons

    metadata_title = _metadata_field(
        item,
        "title",
    )

    metadata_caption = _metadata_field(
        item,
        "caption",
    )

    filename = _filename(
        item
    )

    wp_title = _wordpress_title(
        item
    )

    #
    # Exact metadata matches
    #

    if metadata_title == query_phrase:

        return (
            10000,
            [
                "metadata_title:exact"
            ],
        )

    if metadata_caption == query_phrase:

        return (
            9000,
            [
                "metadata_caption:exact"
            ],
        )

    score = 0

    #
    # Strong full-name matching.
    #
    # Only award these large bonuses when the
    # query contains TWO OR MORE meaningful words.
    #

    if len(query_words) >= 2:

        for field_name, value, weight in (

            (
                "metadata_title",
                metadata_title,
                7000,
            ),

            (
                "metadata_caption",
                metadata_caption,
                6000,
            ),

        ):

            tokens = set(
                _clean_words(
                    value
                )
            )

            if all(
                word in tokens
                for word in query_words
            ):

                score += weight

                reasons.append(
                    f"{field_name}:full_name"
                )

    #
    # Partial metadata matching.
    # Lower weight so single-word searches like
    # "Sony" don't dominate unrelated images.
    #

    if query_phrase in metadata_title:

        score += 1000

        reasons.append(
            "metadata_title:contains"
        )

    if query_phrase in metadata_caption:

        score += 800

        reasons.append(
            "metadata_caption:contains"
        )

    #
    # Filename fallback
    #

    filename_tokens = set(
        _clean_words(
            filename
        )
    )

    if all(
        word in filename_tokens
        for word in query_words
    ):

        score += 500

        reasons.append(
            "filename:match"
        )

    #
    # WordPress title fallback
    #

    wp_tokens = set(
        _clean_words(
            wp_title
        )
    )

    if (
        "aggregator downloaded"
        not in wp_title
        and all(
            word in wp_tokens
            for word in query_words
        )
    ):

        score += 300

        reasons.append(
            "wordpress_title:match"
        )

    if score <= 0:
        return 0, reasons

    return score, reasons