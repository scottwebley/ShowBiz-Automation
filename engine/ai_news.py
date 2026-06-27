from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


def get_top_stories():

    prompt = """
Generate today's five biggest entertainment stories.

Return ONLY valid JSON.

Format:

[
  {
    "headline":"",
    "summary":"",
    "category":"",
    "image_search":""
  }
]

Rules:

- Categories must be one of:
Movies
Television
Music
Streaming
Awards
Celebrity
Theatre

- summary should be 25-40 words.

- image_search should describe the ideal news image.

- Do not use markdown.

- Do not explain anything.

Return JSON only.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input="""
Return ONLY valid JSON.

Return an array of exactly 5 objects.

Each object must contain:

headline
summary
category
image_search

Do not explain anything.
Do not use markdown.
Do not wrap the JSON in code fences.
"""

)

    print(response.output_text)

    return json.loads(response.output_text)