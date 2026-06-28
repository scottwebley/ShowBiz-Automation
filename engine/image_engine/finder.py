"""
ShowBiz Image Engine
finder.py

Version 1.0

This module determines the best search phrase
for finding an editorial-quality image.
"""

from dataclasses import dataclass


@dataclass
class Story:

    headline: str
    category: str
    summary: str = ""


def build_search_query(story: Story) -> str:
    """
    Build the best search query for an image.
    """

    headline = story.headline.strip()

    if story.category.lower() == "movies":
        return f"{headline} official promotional image"

    if story.category.lower() == "television":
        return f"{headline} publicity photo"

    if story.category.lower() == "streaming":
        return f"{headline} promotional image"

    if story.category.lower() == "music":
        return f"{headline} publicity photo"

    return headline


if __name__ == "__main__":

    story = Story(
        headline="Toy Story 5",
        category="Movies"
    )

    print(build_search_query(story))