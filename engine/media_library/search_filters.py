"""
===========================================
ShowBiz Media Search Filters
Version 1.2
===========================================

Purpose:
    Candidate filtering helpers for Media
    Library search.

This module does NOT:
    - Search
    - Score
    - Load cache

Author:
    ShowBiz Automation
"""

from engine.media_library.normalize import (
    safe,
)


BLOCKED_TERMS = (
    "agreement",
    "contract",
    "signature",
    "invoice",
    "receipt",
    "proposal",
    "application",
    "document",
    "legal",
    "purchase",
    "sale",
    ".pdf",
)


GENERIC_MEDIA_TERMS = (
    "aggregator downloaded",
    "imported item",
    "mcdhefo",
    "zx001",
)


WEAK_REASON_TERMS = {
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
    "heart",
}



def clean_reasons(reasons):
    """
    Remove weak scoring reasons.
    """

    cleaned = []


    for reason in reasons:

        lower = reason.lower()

        blocked = False


        for word in WEAK_REASON_TERMS:

            if lower.endswith(
                f":{word}"
            ):

                blocked = True
                break


        if not blocked:

            cleaned.append(
                reason
            )


    return cleaned



def _metadata_fields(item):
    """
    Return useful WordPress image metadata.
    """

    values = []


    details = item.get(
        "media_details",
        {},
    )


    if isinstance(
        details,
        dict,
    ):

        image_meta = details.get(
            "image_meta",
            {},
        )


        if isinstance(
            image_meta,
            dict,
        ):

            values.extend(
                [
                    safe(
                        image_meta.get(
                            "title"
                        )
                    ),

                    safe(
                        image_meta.get(
                            "caption"
                        )
                    ),

                    safe(
                        image_meta.get(
                            "alt"
                        )
                    ),
                ]
            )


    return values



def _metadata_text(item):

    return " ".join(
        _metadata_fields(
            item
        )
    ).lower()



def _has_real_metadata(item):
    """
    Determine if image has useful
    photographer/media metadata.
    """

    for value in _metadata_fields(
        item
    ):

        if value.strip():

            return True


    return False



def _attachment_title(item):

    title = item.get(
        "title",
        "",
    )


    if isinstance(
        title,
        dict,
    ):

        return safe(
            title.get(
                "rendered"
            )
        ).lower()


    return safe(
        title
    ).lower()



def candidate_text(item):
    """
    Build searchable candidate text.

    Real image metadata is preferred.
    """

    values = []


    metadata = _metadata_text(
        item
    )


    if metadata:

        values.append(
            metadata
        )


    values.extend(
        [
            safe(
                item.get(
                    "filename"
                )
            ),

            safe(
                item.get(
                    "alt_text"
                )
            ),

        ]
    )


    return " ".join(
        values
    ).lower()



def is_blocked_candidate(item):
    """
    Reject documents and junk imports.

    Imported images with real metadata
    are allowed.
    """

    text = candidate_text(
        item
    )


    for term in BLOCKED_TERMS:

        if term in text:

            return True


    title = _attachment_title(
        item
    )


    has_metadata = _has_real_metadata(
        item
    )


    for term in GENERIC_MEDIA_TERMS:

        if term in title:

            if not has_metadata:

                return True


    return False



def valid_candidate(
    item,
    score,
    reasons,
):
    """
    Final candidate validation.
    """

    if score <= 0:

        return False


    if is_blocked_candidate(
        item
    ):

        return False


    cleaned = clean_reasons(
        reasons
    )


    if not cleaned:

        return False


    return True