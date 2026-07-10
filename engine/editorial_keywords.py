"""
===========================================
ShowBiz Editorial Keywords
Version 1.0
===========================================

Purpose:
    Central editorial keyword lists used by
    the Local Story Selector.

    This module contains NO ranking logic.

Author:
    ShowBiz Automation
"""

from __future__ import annotations


# ---------------------------------------------------------
# Hard rejection terms
# ---------------------------------------------------------

HARD_REJECTION_TERMS = (
    "happy ending massage",
    "massage",
    "porn",
    "pornhub",
    "onlyfans",
    "sex",
    "sexual",
    "adult",
    "escort",
    "dating",
    "hookup",
    "nude",
    "nsfw",
)


# ---------------------------------------------------------
# Evergreen / SEO content
# ---------------------------------------------------------

EVERGREEN_PENALTIES = (
    "best ",
    "top 10",
    "top ten",
    "watch guide",
    "watching guide",
    "how to",
    "everything streaming",
    "streaming guide",
    "where to watch",
    "what to watch",
    "shopping",
    "buy ",
    "gift guide",
    "ranking every",
    "ranked",
    "explained",
    "review:",
    "reviews:",
    "list of",
)


# ---------------------------------------------------------
# Streaming recommendation headlines
# ---------------------------------------------------------

STREAMING_PENALTIES = (
    "streaming",
    "binge",
    "binge-watch",
    "watch now",
    "must watch",
    "must-watch",
    "available now",
    "now streaming",
)


# ---------------------------------------------------------
# Breaking entertainment news
# ---------------------------------------------------------

BREAKING_NEWS_TERMS = (
    "breaking",
    "announces",
    "announced",
    "announcement",
    "trailer",
    "teaser",
    "premiere",
    "release date",
    "cast",
    "casting",
    "joins",
    "starring",
    "renewed",
    "renewal",
    "cancelled",
    "canceled",
    "box office",
    "wins",
    "winner",
    "award",
    "emmy",
    "oscar",
    "grammy",
    "golden globe",
    "tour",
    "concert",
    "festival",
    "obituary",
    "dies",
    "dead",
    "acquires",
    "acquisition",
    "merger",
    "deal",
    "lawsuit",
)


# ---------------------------------------------------------
# Major studios / streamers
# ---------------------------------------------------------

MAJOR_STUDIOS = (
    "disney",
    "marvel",
    "pixar",
    "lucasfilm",
    "warner bros",
    "warner",
    "dc",
    "universal",
    "paramount",
    "sony",
    "lionsgate",
    "netflix",
    "hbo",
    "max",
    "apple tv",
    "apple tv+",
    "amazon mgm",
    "amazon studios",
    "prime video",
    "peacock",
    "hulu",
    "a24",
)


# ---------------------------------------------------------
# Major franchises
# ---------------------------------------------------------

MAJOR_FRANCHISES = (
    "star wars",
    "marvel",
    "dc",
    "avengers",
    "batman",
    "superman",
    "spider-man",
    "jurassic",
    "avatar",
    "mission impossible",
    "harry potter",
    "lord of the rings",
    "james bond",
    "fast & furious",
    "fast and furious",
)


# ---------------------------------------------------------
# Industry news
# ---------------------------------------------------------

INDUSTRY_TERMS = (
    "ceo",
    "studio",
    "executive",
    "media",
    "industry",
    "earnings",
    "revenue",
    "shares",
    "ipo",
    "streamer",
    "broadcast",
)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def contains_any(text: str, phrases) -> bool:
    """Return True if any phrase exists in text."""
    text = text.lower()
    return any(p in text for p in phrases)


def count_matches(text: str, phrases) -> int:
    """Count matching editorial phrases."""
    text = text.lower()
    return sum(1 for p in phrases if p in text)