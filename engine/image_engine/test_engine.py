"""
===========================================
ShowBiz Image Engine
test_engine.py
Version 1.0
===========================================

Tests the Image Engine without touching
production.

Pipeline:

Story
   ↓
AI Editor
   ↓
Finder
   ↓
Display search requests
"""

from ai_editor import analyze_story
from finder import build_requests


def main():

    headline = "Taylor Swift draws cheers and boos during surprise appearance at Alan Jackson's farewell concert"

    summary = (
        "Swift surprised fans with an unexpected appearance "
        "during Alan Jackson's farewell concert."
    )

    category = "Music"

    print()
    print("=" * 60)
    print("SHOWBIZ IMAGE ENGINE TEST")
    print("=" * 60)

    print("\nAnalyzing story...\n")

    decision = analyze_story(
        headline=headline,
        summary=summary,
        category=category
    )

    print("EDITORIAL DECISION")
    print("------------------------------")

    for key, value in decision.items():
        print(f"{key:20} {value}")

    print("\nBuilding search requests...\n")

    requests = build_requests(decision)

    print("SEARCH REQUESTS")
    print("------------------------------")

    for request in requests:
        print(f"{request.source:18} {request.query}")

    print("\n✓ Image Engine test completed.")


if __name__ == "__main__":
    main()