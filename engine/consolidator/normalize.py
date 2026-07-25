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


def entities(text: str) -> set[str]:
    """
    Extract entertainment entities from headlines and article bodies.

    Designed to recognize:
    - People (Ian Diaz, Michelle Hadley)
    - Titles ("A Toxic Love Story", Heartstopper: Forever)
    - Companies/brands (Netflix, Disney+, Marvel Studios)
    """

    import re

    if not text:
        return set()

    text = text.replace("\n", " ")

    entities = set()

    #
    # 1. Quoted titles
    #
    for m in re.finditer(r"[\"']([^\"']{3,80})[\"']", text):
        title = m.group(1).strip()

        title = re.sub(r"\s+", " ", title)
        title = title.strip(" .,:;!?")

        if len(title.split()) <= 8:
            entities.add(title)

    #
    # 2. Capitalized phrases
    #
    pattern = re.compile(
        r"\b[A-Z][A-Za-z0-9'&:+.-]*"
        r"(?:\s+[A-Z][A-Za-z0-9'&:+.-]*){0,5}"
    )

    bad_start = {
        "A","An","And","As","At","By","For","From",
        "Get","Here's","How","In","Into","Its",
        "Last","Latest","New","On","Published",
        "Press","Report","Reports","Senior",
        "The","This","To","Updated","Via",
        "What","When","Where","Why","Will","With"
    }

    bad_phrase = {
        "Breaking News",
        "Latest News",
        "Read More",
        "Press Association",
        "Senior Entertainment Reporter",
        "Entertainment Reporter",
    }

    for match in pattern.finditer(text):

        phrase = match.group(0).strip(" ,.:;!?()[]{}")

        words = phrase.split()

        if not words:
            continue

        if words[0] in bad_start:
            continue

        if phrase in bad_phrase:
            continue

        phrase = re.sub(r"\s+", " ", phrase)

        entities.add(phrase)

    #
    # 3. Normalize punctuation
    #
    cleaned = set()

    for entity in entities:

        entity = entity.replace("’", "'")
        entity = re.sub(r"\s+", " ", entity)
        entity = entity.strip(" .,:;!?")

        if len(entity) >= 3:
            cleaned.add(entity)

    #
    # 4. Remove only obvious supersets
    #
    final = set(cleaned)

    for a in cleaned:
        for b in cleaned:

            if a == b:
                continue

            if (
                len(a.split()) > len(b.split())
                and a.endswith(b)
            ):
                final.discard(a)

    return final


def event_words(text):

    return [
        word
        for word in normalize(text).split()
        if word in EVENT_ALIASES.values()
    ]