"""
===========================================
ShowBiz Image Engine
story.py
Version 1.0
===========================================

Represents a news story that will be
processed by the Image Engine.
"""

from dataclasses import dataclass


@dataclass
class Story:

    headline: str

    summary: str = ""

    category: str = ""

    article_url: str = ""

    author: str = "ShowBiz AI"

    published_date: str = ""

    featured: bool = False


if __name__ == "__main__":

    story = Story(

        headline="Taylor Swift draws cheers and boos during surprise appearance at Alan Jackson's farewell concert",

        summary="Swift surprised fans with an unexpected appearance during Alan Jackson's farewell concert.",

        category="Music"

    )

    print(story)