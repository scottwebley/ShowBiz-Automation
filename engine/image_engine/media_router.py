"""
===========================================
ShowBiz Media Engine
media_router.py
Version 1.0
===========================================

Routes stories to the best media source.

This file contains NO API code.

It simply decides which provider
should handle the story.
"""

from editorial_decision import EditorialDecision


class MediaRouter:

    def choose_provider(
        self,
        decision: EditorialDecision
    ):

        # Movies

        if decision.subject_type == "movie":
            return "official_press"

        # Television

        if decision.subject_type == "television":
            return "official_press"

        # Music

        if decision.subject_type == "music":
            return "editorial_photo"

        # Companies

        if decision.subject_type == "company":
            return "official_press"

        # Events

        if decision.subject_type == "event":
            return "editorial_photo"

        # Historical / General

        return "wikimedia"


def main():

    decision = EditorialDecision(

        subject="Taylor Swift",

        subject_type="music",

        story_type="concert appearance",

        preferred_photo="performance",

        preferred_source="editorial_photo",

        reasoning="Primary performer."

    )

    router = MediaRouter()

    provider = router.choose_provider(decision)

    print()

    print("=" * 60)
    print("MEDIA ROUTER")
    print("=" * 60)

    print()

    print("Chosen Provider:")

    print(provider)


if __name__ == "__main__":
    main()