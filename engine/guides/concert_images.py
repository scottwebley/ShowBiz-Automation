"""
===========================================
ShowBiz Concert Images
Version 1.0
===========================================

Purpose:
    Handle all Ticketmaster image
    selection for the ShowBiz
    Concert Guide.
"""

from concert_api import request_ticketmaster


def score_image(image):
    """
    Score a Ticketmaster image.
    Higher scores are preferred.
    """

    url = image.get(
        "url",
        ""
    )

    width = image.get(
        "width",
        0,
    )

    height = image.get(
        "height",
        0,
    )

    score = width * height

    if "_SOURCE" in url:

        score += 1000000000

    elif "_TABLET_LANDSCAPE_LARGE" in url:

        score += 500000000

    elif "_TABLET_LANDSCAPE" in url:

        score += 250000000

    elif "_ARTIST_PAGE" in url:

        score += 100000000

    elif "_RETINA_LANDSCAPE" in url:

        score += 75000000

    elif "_RETINA_PORTRAIT" in url:

        score += 50000000

    elif "_EVENT_DETAIL_PAGE" in url:

        score += 25000000

    return score


def select_best_event_image(
    images,
):
    """
    Return the best image from an
    event's image list.
    """

    best_url = ""

    best_score = -1

    for image in images:

        score = score_image(
            image
        )

        if score > best_score:

            best_score = score

            best_url = image.get(
                "url",
                ""
            )

    return best_url


def get_attraction_image(
    attraction_ids,
):
    """
    Return the highest quality
    attraction artwork.
    """

    if not attraction_ids:

        return ""

    attraction_id = attraction_ids[0]

    endpoint = (
        "https://app.ticketmaster.com/"
        f"discovery/v2/attractions/"
        f"{attraction_id}.json"
    )

    data = request_ticketmaster(
        endpoint=endpoint,
    )

    images = data.get(
        "images",
        []
    )

    return select_best_event_image(
        images
    )


if __name__ == "__main__":

    print()

    print(
        "ShowBiz Concert Images"
    )

    print(
        "Module loaded."
    )