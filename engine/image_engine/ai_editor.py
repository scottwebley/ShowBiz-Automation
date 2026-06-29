"""
===========================================
ShowBiz Image Engine
ai_editor.py
Version 2.2
===========================================

Uses GPT to make editorial image decisions.
"""

import json

from openai import OpenAI
from dotenv import load_dotenv

from story import Story
from editorial_decision import EditorialDecision

load_dotenv()

client = OpenAI()


def analyze_story(story: Story) -> EditorialDecision:

    prompt = f"""
You are the Senior Photo Editor for ShowBiz.com.

Analyze this entertainment story.

Headline:
{story.headline}

Summary:
{story.summary}

Category:
{story.category}

Return ONLY valid JSON.

{{
    "subject": "",
    "subject_type": "",
    "story_type": "",
    "preferred_photo": "",
    "preferred_source": "",
    "reasoning": ""
}}

Rules

subject_type must be one of:

person
movie
television
music
company
event
place
general

preferred_photo must be one of:

portrait
performance
movie_still
tv_still
logo
venue
general

preferred_source must be one of:

official_press
editorial_photo
licensed_stock
wikimedia

Return ONLY JSON.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    data = json.loads(response.output_text)

    return EditorialDecision(

        subject=data["subject"],

        subject_type=data["subject_type"],

        story_type=data["story_type"],

        preferred_photo=data["preferred_photo"],

        preferred_source=data["preferred_source"],

        reasoning=data["reasoning"]

    )


def main():

    story = Story(

        headline="Taylor Swift draws cheers and boos during surprise appearance at Alan Jackson's farewell concert",

        summary="Swift surprised fans during Alan Jackson's farewell concert.",

        category="Music"

    )

    decision = analyze_story(story)

    print()

    print("=" * 60)
    print("EDITORIAL DECISION")
    print("=" * 60)

    print(decision)


if __name__ == "__main__":
    main()