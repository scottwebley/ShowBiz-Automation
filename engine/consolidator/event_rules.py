# engine/consolidator/event_rules.py

"""
ShowBiz Story Consolidator
Event Rules

Normalized event detection used by the story consolidator.
"""

EVENT_ALIASES = {
    # Layoffs
    "layoff": "layoff",
    "layoffs": "layoff",
    "cut": "layoff",
    "cuts": "layoff",
    "downsizing": "layoff",
    "downsize": "layoff",
    "downsizes": "layoff",
    "staff": "layoff",
    "workforce": "layoff",
    "reduction": "layoff",
    "reductions": "layoff",
    "eliminate": "layoff",
    "eliminates": "layoff",
    "fired": "layoff",
    "fires": "layoff",

    # Delays
    "delay": "delay",
    "delays": "delay",
    "delayed": "delay",
    "postpone": "delay",
    "postponed": "delay",

    # Cancellations
    "cancel": "cancel",
    "cancels": "cancel",
    "cancelled": "cancel",
    "canceled": "cancel",

    # Renewals
    "renew": "renew",
    "renewed": "renew",
    "renews": "renew",
    "renewal": "renew",

    # Premieres
    "premiere": "premiere",
    "premieres": "premiere",
    "debut": "premiere",
    "debuts": "premiere",
    "launch": "premiere",
    "launches": "premiere",

    # Acquisitions
    "acquire": "acquire",
    "acquires": "acquire",
    "acquired": "acquire",
    "buy": "acquire",
    "buys": "acquire",
    "purchase": "acquire",
    "purchases": "acquire",

    # Reopenings
    "reopen": "reopen",
    "reopens": "reopen",
    "reopened": "reopen",
    "reopening": "reopen",
    "opens": "reopen",
    "opening": "reopen",

    # Closures
    "close": "close",
    "closes": "close",
    "closed": "close",
    "closing": "close",

    # Trailers
    "trailer": "trailer",
    "teaser": "trailer",
    "teasers": "trailer",

    # Casting
    "cast": "cast",
    "casting": "cast",
    "join": "cast",
    "joins": "cast",

    # Awards
    "award": "award",
    "awards": "award",
    "wins": "award",
    "won": "award",
    "nominated": "award",
    "nomination": "award",
    "nominations": "award",

    # Box Office
    "boxoffice": "boxoffice",
    "box-office": "boxoffice",
}


def event_words(text, normalize):
    """
    Return normalized event words from text.

    normalize() is injected from normalize.py to avoid
    circular imports.
    """
    if not text:
        return []

    events = []

    for word in normalize(text).split():
        if word in EVENT_ALIASES.values():
            events.append(word)

    return events