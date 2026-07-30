"""
Determine whether an entertainment story is about
a movie, TV show, or video game.

Independent module.
"""

MOVIE_KEYWORDS = {
    "movie",
    "film",
    "box office",
    "cinema",
    "theaters",
}

TV_KEYWORDS = {
    "tv",
    "television",
    "series",
    "season",
    "episode",
    "streaming",
    "netflix",
    "hulu",
    "disney+",
    "max",
    "paramount+",
    "apple tv+",
    "prime video",
    "peacock",
}

GAME_KEYWORDS = {
    "game",
    "gaming",
    "playstation",
    "xbox",
    "nintendo",
    "switch",
    "steam",
    "pc",
    "ps5",
    "ps6",
    "dlc",
    "expansion",
    "trailer gameplay",
}


def detect_content_type(headline: str, category: str = "") -> str:
    """
    Returns:

        movie
        tv
        game
        unknown
    """

    text = f"{headline} {category}".lower()

    if any(word in text for word in GAME_KEYWORDS):
        return "game"

    if any(word in text for word in TV_KEYWORDS):
        return "tv"

    if any(word in text for word in MOVIE_KEYWORDS):
        return "movie"

    return "unknown"