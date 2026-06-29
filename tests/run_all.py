"""
===========================================
ShowBiz Automated Test Suite
Version 2.0
===========================================

Runs regression tests for the ShowBiz newsroom.

Usage

    python3 -m tests.run_all
"""

from engine.editorial_filter import keep_story
from engine.scorer import score_story
from engine.categorizer import categorize_story


passed = 0
failed = 0


def run_test(name, result):

    global passed
    global failed

    if result:

        print(f"✓ {name}")
        passed += 1

    else:

        print(f"✗ {name}")
        failed += 1


def test_editorial_filter():

    story = {
        "headline": "Supreme Court Issues New Decision",
        "summary": ""
    }

    return keep_story(story) is False


def test_story_scorer():

    story = {
        "headline": "Netflix Renews Hit Series For Season 3",
        "summary": ""
    }

    return score_story(story) == 65


def test_categorizer_movies():

    story = {
        "headline": "Marvel Releases Fantastic Four Trailer",
        "summary": ""
    }

    return categorize_story(story) == "Movies"


def test_categorizer_music():

    story = {
        "headline": "Taylor Swift Announces World Tour",
        "summary": ""
    }

    return categorize_story(story) == "Music"


def test_categorizer_tv():

    story = {
        "headline": "Netflix Renews Hit Series For Season 3",
        "summary": ""
    }

    return categorize_story(story) == "Television"


def main():

    print()
    print("=" * 60)
    print("SHOWBIZ AUTOMATED TEST SUITE")
    print("=" * 60)
    print()

    run_test(
        "Editorial Filter rejects Supreme Court",
        test_editorial_filter()
    )

    run_test(
        "Story Scorer scores Netflix correctly",
        test_story_scorer()
    )

    run_test(
        "Categorizer identifies Movies",
        test_categorizer_movies()
    )

    run_test(
        "Categorizer identifies Music",
        test_categorizer_music()
    )

    run_test(
        "Categorizer identifies Television",
        test_categorizer_tv()
    )

    print()
    print("=" * 60)
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print("=" * 60)

    if failed == 0:

        print()
        print("✓ ALL TESTS PASSED")

    else:

        print()
        print("✗ SOME TESTS FAILED")


if __name__ == "__main__":
    main()