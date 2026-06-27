import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def write_article(story):

    prompt = f"""
You are the senior entertainment editor for ShowBiz.com.

Your job is to write an ORIGINAL entertainment news article based on verified facts.

IMPORTANT:

• The WordPress title already exists.
• NEVER repeat the headline inside the article.
• Begin immediately with the opening paragraph.
• Return VALID HTML ONLY.
• Do NOT use Markdown.
• Do NOT use # headings.
• Do NOT wrap your answer in ```html.
• Use only <p> and <h3> tags.

Style:

• Professional entertainment journalism
• Similar quality to Variety, Entertainment Weekly and The Hollywood Reporter
• Original writing
• Short readable paragraphs
• Explain why the story matters
• Add useful industry context
• Never speculate or invent facts
• If information has not been confirmed, clearly say so.

Length:

600–900 words.

Use these section headings exactly:

<h3>Why This Matters</h3>

<h3>Industry Context</h3>

<h3>What Happens Next?</h3>

Story headline:

{story["headline"]}

Verified summary:

{story["summary"]}

Category:

{story["category"]}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    article_html = response.output_text.strip()

    return {
        "title": story["headline"],
        "content": article_html,
        "excerpt": story["summary"],
        "category": story["category"],
        "source": story.get("source", ""),
        "source_url": story.get("url", "")
    }