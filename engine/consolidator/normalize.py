# engine/consolidator/normalize.py

"""
ShowBiz Story Consolidator
Normalization Engine v7
"""

import re

STOP_WORDS = {
    "a","an","and","are","as","at","be","been","being",
    "by","for","from","how","if","in","into","is","it",
    "its","of","on","or","that","the","their","this",
    "to","was","were","what","when","where","which",
    "who","why","will","with","after","amid","before",
    "during","despite","latest","new","report","reports",
    "say","says","reveals","revealed","first","look",
    "review","breaking","exclusive","today","tonight",

    # Boilerplate
    "print","article","share","email","facebook","twitter",
    "threads","linkedin","reddit","copy","link","comments",
    "comment","subscribe","newsletter","login","register",
    "menu","home","search","read","more","continue"
}

EVENT_ALIASES = {

    # layoffs
    "layoff":"layoff",
    "layoffs":"layoff",
    "cuts":"layoff",
    "cut":"layoff",
    "downsizing":"layoff",
    "downsizes":"layoff",
    "downsize":"layoff",
    "staff":"layoff",
    "workforce":"layoff",
    "reduction":"layoff",
    "reductions":"layoff",
    "eliminates":"layoff",
    "eliminate":"layoff",
    "fires":"layoff",
    "fired":"layoff",

    # delays
    "delay":"delay",
    "delays":"delay",
    "delayed":"delay",
    "postpone":"delay",
    "postponed":"delay",

    # cancellations
    "cancel":"cancel",
    "cancels":"cancel",
    "cancelled":"cancel",
    "canceled":"cancel",

    # renewals
    "renew":"renew",
    "renewed":"renew",
    "renews":"renew",
    "renewal":"renew",

    # premieres
    "premiere":"premiere",
    "premieres":"premiere",
    "debut":"premiere",
    "debuts":"premiere",
    "launch":"premiere",
    "launches":"premiere",

    # acquisitions
    "acquires":"acquire",
    "acquired":"acquire",
    "acquire":"acquire",
    "buy":"acquire",
    "buys":"acquire",
    "purchase":"acquire",
    "purchases":"acquire",

    # reopenings
    "reopen":"reopen",
    "reopens":"reopen",
    "reopened":"reopen",
    "reopening":"reopen",
    "opens":"reopen",
    "opening":"reopen",

    # closures
    "close":"close",
    "closes":"close",
    "closed":"close",
    "closing":"close",

    # trailers
    "trailer":"trailer",
    "teaser":"trailer",
    "teasers":"trailer",

    # casting
    "cast":"cast",
    "casting":"cast",
    "joins":"cast",
    "join":"cast",

    # awards
    "wins":"award",
    "won":"award",
    "award":"award",
    "awards":"award",
    "nominated":"award",
    "nomination":"award",
    "nominations":"award",

    # box office
    "boxoffice":"boxoffice",
    "box-office":"boxoffice",
}

NON_ENTITY_WORDS = {
    "movie","film","show","series","season","episode",
    "actor","actress","music","album","tour","concert",
    "television","tv","streaming","video","official",
    "exclusive","breaking","photos","photo","images",
    "image","watch","watching","trailer","teaser",

    # Boilerplate
    "article","print","share","read","more","continue"
}

BOILERPLATE_PATTERNS = [
    r"\bprint article\b",
    r"\bshare (this )?article\b",
    r"\bread more\b",
    r"\bcontinue reading\b",
    r"\bclick here\b",
    r"\bsubscribe\b",
    r"\bsign up\b",
]


def normalize(text: str) -> str:

    if not text:
        return ""

    text = text.lower()

    for pattern in BOILERPLATE_PATTERNS:
        text = re.sub(pattern, " ", text)

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = []

    for word in text.split():

        if word in STOP_WORDS:
            continue

        word = EVENT_ALIASES.get(word, word)

        words.append(word)

    return " ".join(words)


def keywords(text):

    return {
        word
        for word in normalize(text).split()
        if len(word) >= 3
    }


def entities(text):
    """
    Return likely entertainment entities.
    """

    if not text:
        return set()

    original = normalize(text)

    PHRASES = [
        "warner bros",
        "warner brothers",
        "universal studios",
        "universal pictures",
        "paramount pictures",
        "sony pictures",
        "searchlight pictures",
        "20th century studios",
        "amazon mgm",

        "disney plus",
        "apple tv",
        "prime video",
        "hbo max",
        "paramount",
        "peacock",
        "netflix",
        "hulu",

        "cinerama dome",
        "radio city music hall",
        "hollywood bowl",
        "madison square garden",

        "academy awards",
        "golden globes",
        "emmy awards",
        "grammy awards",
        "tony awards",

        "warner discovery",
        "warner bros discovery",
        "disney",
        "pixar",
        "marvel",
        "lucasfilm",
        "a24",
        "apple",
        "amazon",
        "netflix",
        "paramount",
        "universal",
        "sony",
    ]

    found = set()

    for phrase in PHRASES:
        if phrase in original:
            found.add(
                phrase.replace(" ", "_")
            )

    for word in keywords(text):
        if len(word) >= 4 and word not in NON_ENTITY_WORDS:
            found.add(word)

    return found


def event_words(text):

    return [
        word
        for word in normalize(text).split()
        if word in EVENT_ALIASES.values()
    ]