"""
===========================================
ShowBiz Image Engine
finder.py
Version 2.2
===========================================

Builds search requests from an
EditorialDecision.
"""

from dataclasses import dataclass

from editorial_decision import EditorialDecision


@dataclass
class SearchRequest:

    source: str
    query: str


def build_requests(decision: EditorialDecision):

    subject = decision.subject
    photo = decision.preferred_photo

    requests = []

    # ----------------------------------------
    # Official Press
    # ----------------------------------------

    official_queries = {

        "performance":
            f"{subject} performance publicity photo",

        "portrait":
            f"{subject} publicity portrait",

        "movie_still":
            f"{subject} official movie still",

        "tv_still":
            f"{subject} official television still",

        "logo":
            f"{subject} official logo",

        "venue":
            f"{subject} venue publicity photo",

        "general":
            subject

    }

    requests.append(

        SearchRequest(

            source="official_press",

            query=official_queries.get(photo, subject)

        )

    )

    # ----------------------------------------
    # Wikimedia
    # ----------------------------------------

    requests.append(

        SearchRequest(

            source="wikimedia",

            query=subject

        )

    )

    return requests


def main():

    decision = EditorialDecision(

        subject="Taylor Swift",

        subject_type="person",

        story_type="concert appearance",

        preferred_photo="performance",

        preferred_source="editorial_photo",

        reasoning="Taylor Swift is the primary visual subject."

    )

    print()

    print("=" * 60)
    print("SEARCH REQUEST TEST")
    print("=" * 60)

    searches = build_requests(decision)

    for search in searches:

        print(f"{search.source:18} {search.query}")


if __name__ == "__main__":
    main()