"""
Featured Entertainer scheduling helpers.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


FEATURED_JSON = Path(
    "data/featured_entertainer.json"
)


def current_editorial_week():
    """
    Return the current editorial week string.
    """

    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    return (
        f"Week of "
        f"{monday.strftime('%B')} "
        f"{monday.day}, "
        f"{monday.year}"
    )


def already_published_this_week():
    """
    Return True if this week's Featured Entertainer
    has already been published.
    """

    #
    # Temporary override while testing.
    #
    # Change to:
    #
    #     return _already_published()
    #
    # when weekly scheduling is re-enabled.
    #

    return False


def _already_published():
    """
    Production version.
    """

    if not FEATURED_JSON.exists():
        return False

    try:

        with open(
            FEATURED_JSON,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

    except Exception:

        return False

    return (
        data.get("week")
        == current_editorial_week()
    )