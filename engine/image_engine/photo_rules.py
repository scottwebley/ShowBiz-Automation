"""
===========================================
ShowBiz Image Engine
photo_rules.py
Version 1.0
===========================================

Editorial rules for selecting
the best type of image.
"""

PHOTO_RULES = {

    "Movies": {

        "preferred_photo": "movie_still",

        "preferred_source": "official_press"

    },

    "Television": {

        "preferred_photo": "tv_still",

        "preferred_source": "official_press"

    },

    "Streaming": {

        "preferred_photo": "tv_still",

        "preferred_source": "official_press"

    },

    "Music": {

        "preferred_photo": "performance",

        "preferred_source": "editorial_photo"

    },

    "Awards": {

        "preferred_photo": "red_carpet",

        "preferred_source": "editorial_photo"

    },

    "Style": {

        "preferred_photo": "portrait",

        "preferred_source": "editorial_photo"

    }

}


DEFAULT_RULE = {

    "preferred_photo": "general",

    "preferred_source": "wikimedia"

}


def get_rule(category):

    return PHOTO_RULES.get(category, DEFAULT_RULE)


if __name__ == "__main__":

    categories = [

        "Movies",

        "Television",

        "Music",

        "Awards",

        "Style",

        "Unknown"

    ]

    print()

    print("=" * 60)

    print("PHOTO RULE TEST")

    print("=" * 60)

    for category in categories:

        rule = get_rule(category)

        print(f"{category:12} -> {rule}")