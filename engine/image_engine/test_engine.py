"""
===========================================
ShowBiz Media Engine
test_engine.py
Version 3.0
===========================================

Complete Media Engine test.

Story
   ↓
AI Editor
   ↓
Media Router
   ↓
Finder
"""

from story import Story
from ai_editor import analyze_story
from media_router import MediaRouter
from finder import build_requests


def main():

    story = Story(

        headline="Taylor Swift draws cheers and boos during surprise appearance at Alan Jackson's farewell concert",

        summary="Swift surprised fans during Alan Jackson's farewell concert.",

        category="Music"

    )

    print()

    print("=" * 60)
    print("SHOWBIZ MEDIA ENGINE")
    print("=" * 60)

    print()

    print("Story")

    print("----------------------------------------")

    print(story)

    #
    # AI Editor
    #

    decision = analyze_story(story)

    print()

    print("Editorial Decision")

    print("----------------------------------------")

    print(decision)

    #
    # Media Router
    #

    router = MediaRouter()

    provider = router.choose_provider(decision)

    print()

    print("Chosen Provider")

    print("----------------------------------------")

    print(provider)

    #
    # Finder
    #

    requests = build_requests(decision)

    print()

    print("Search Requests")

    print("----------------------------------------")

    for request in requests:

        print(f"{request.source:18} {request.query}")

    print()

    print("=" * 60)

    print("MEDIA ENGINE TEST COMPLETE")

    print("=" * 60)


if __name__ == "__main__":
    main()