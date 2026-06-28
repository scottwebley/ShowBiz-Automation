"""
===========================================
ShowBiz Image Engine
editor.py
Version 1.0
===========================================

This module acts as the editorial brain for
ShowBiz's image selection system.

Its job is NOT to download images.

Its job is to determine WHAT image an
entertainment editor would choose.

Everything else happens later.
"""

from dataclasses import dataclass


# ============================================
# Story Object
# ============================================

@dataclass
class Story:

    headline: str
    category: str
    summary: str = ""


# ============================================
# Editorial Decision
# ============================================

@dataclass
class ImageDecision:

    story_type: str
    search_query: str
    preferred_source: str


# ============================================
# Editorial Brain
# ============================================

def analyze_story(story: Story) -> ImageDecision:

    headline = story.headline.lower()

    # ----------------------------------------
    # Movie Releases
    # ----------------------------------------

    if any(word in headline for word in [
        "movie",
        "film",
        "box office",
        "trailer"
    ]):

        return ImageDecision(
            story_type="Movie",
            search_query=f"{story.headline} official promotional image",
            preferred_source="official_press"
        )

    # ----------------------------------------
    # Television
    # ----------------------------------------

    if any(word in headline for word in [
        "series",
        "season",
        "television",
        "tv",
        "episode"
    ]):

        return ImageDecision(
            story_type="Television",
            search_query=f"{story.headline} publicity photo",
            preferred_source="official_press"
        )

    # ----------------------------------------
    # Music
    # ----------------------------------------

    if any(word in headline for word in [
        "album",
        "tour",
        "concert",
        "single",
        "music"
    ]):

        return ImageDecision(
            story_type="Music",
            search_query=f"{story.headline} publicity photo",
            preferred_source="official_press"
        )

    # ----------------------------------------
    # Broadway / Theatre
    # ----------------------------------------

    if any(word in headline for word in [
        "broadway",
        "theatre",
        "theater",
        "musical"
    ]):

        return ImageDecision(
            story_type="Broadway",
            search_query=f"{story.headline} production photo",
            preferred_source="official_press"
        )

    # ----------------------------------------
    # Streaming
    # ----------------------------------------

    if any(word in headline for word in [
        "netflix",
        "disney+",
        "hulu",
        "max",
        "prime video",
        "apple tv"
    ]):

        return ImageDecision(
            story_type="Streaming",
            search_query=f"{story.headline} promotional image",
            preferred_source="official_press"
        )

    # ----------------------------------------
    # Default
    # ----------------------------------------

    return ImageDecision(
        story_type="General Entertainment",
        search_query=story.headline,
        preferred_source="editorial_photo"
    )


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    story = Story(
        headline="Toy Story 5 dominates the weekend box office",
        category="Movies"
    )

    decision = analyze_story(story)

    print("\nEDITORIAL DECISION")
    print("----------------------------")
    print("Story Type      :", decision.story_type)
    print("Search Query    :", decision.search_query)
    print("Preferred Source:", decision.preferred_source)