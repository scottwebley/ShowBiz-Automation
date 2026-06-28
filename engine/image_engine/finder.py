"""
===========================================
ShowBiz Image Engine
finder.py
Version 2.0
===========================================

Converts the AI Editor's decision into
search requests for different image sources.

This module NEVER downloads images.

It only decides HOW to search.
"""

from dataclasses import dataclass


# ============================================
# Search Request
# ============================================

@dataclass
class SearchRequest:

    source: str
    query: str


# ============================================
# Finder
# ============================================

def build_requests(editor_result):

    subject = editor_result["subject"]

    photo_type = editor_result["preferred_photo"]

    requests = []

    # ----------------------------------------
    # Official Press
    # ----------------------------------------

    if photo_type == "performance":

        requests.append(
            SearchRequest(
                "official_press",
                f"{subject} performance publicity photo"
            )
        )

    elif photo_type == "portrait":

        requests.append(
            SearchRequest(
                "official_press",
                f"{subject} publicity portrait"
            )
        )

    elif photo_type == "movie_still":

        requests.append(
            SearchRequest(
                "official_press",
                f"{subject} official promotional still"
            )
        )

    else:

        requests.append(
            SearchRequest(
                "official_press",
                subject
            )
        )

    # ----------------------------------------
    # Wikimedia Commons
    # ----------------------------------------

    requests.append(

        SearchRequest(
            "wikimedia",
            subject
        )

    )

    # ----------------------------------------
    # Unsplash
    # ----------------------------------------

    requests.append(

        SearchRequest(
            "unsplash",
            subject
        )

    )

    # ----------------------------------------
    # Pexels
    # ----------------------------------------

    requests.append(

        SearchRequest(
            "pexels",
            subject
        )

    )

    return requests


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    sample = {

        "subject": "Taylor Swift",

        "preferred_photo": "performance"

    }

    searches = build_requests(sample)

    print()

    print("SEARCH REQUESTS")

    print("--------------------------")

    for search in searches:

        print(f"{search.source:15} {search.query}")