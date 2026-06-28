"""
===========================================
ShowBiz Image Engine
ai_editor.py
Version 2.0
===========================================

Uses GPT-5.5 to determine the best
editorial image for a story.

This module NEVER downloads images.

It simply thinks like a professional
entertainment photo editor.
"""

import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def analyze_story(headline, summary="", category=""):

    prompt = f"""
You are the Senior Photo Editor for ShowBiz.com.

Analyze the entertainment news story below.

Do NOT write an article.

Decide what IMAGE a professional entertainment
publication should use.

Return ONLY valid JSON.

Headline:
{headline}

Summary:
{summary}

Category:
{category}

Return EXACTLY this structure:

{{
    "subject": "",
    "subject_type": "",
    "story_type": "",
    "preferred_photo": "",
    "preferred_source": "",
    "reasoning": ""
}}

Rules

subject_type must be ONE of:

person
movie
television
music
company
broadway
event
place
general

preferred_photo must be ONE of:

portrait
performance
movie_still
tv_still
production_photo
red_carpet
logo
venue
general

preferred_source must be ONE of:

official_press
editorial_photo
licensed_stock
ai_illustration

Do NOT invent new values.

Keep story_type short.

Keep reasoning to one sentence.

Return ONLY JSON.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return json.loads(response.output_text)


if __name__ == "__main__":

    result = analyze_story(

        headline="Taylor Swift draws cheers and boos during surprise appearance at Alan Jackson's farewell concert",

        summary="Swift surprised fans during Alan Jackson's farewell concert.",

        category="Music"

    )

    print(json.dumps(result, indent=4))