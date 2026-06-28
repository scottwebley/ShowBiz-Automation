from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# WordPress Category IDs
CATEGORY_IDS = {
    "Movies": 3,
    "TV & Streaming": 4,
    "Music": 6,
    "Gaming": 7,
    "Celebrity News": 55,
    "Entertainment Industry": 56,
    "Style": 59,
    "ShowBiz Originals": 60,
}


def write_article(story):

    prompt = f"""
You are a senior entertainment journalist writing for ShowBiz.com.

Write a completely original entertainment news article.

Do NOT copy wording from any publication.

Write in a professional entertainment news style similar in quality to
Variety, Deadline or The Hollywood Reporter, while maintaining a unique voice.

Return HTML ONLY.

Do NOT use Markdown.

Structure exactly like this:

<h3>Why This Matters</h3>

<p>...</p>

<h3>Industry Context</h3>

<p>...</p>

<h3>What Happens Next?</h3>

<p>...</p>

Requirements:

- 600-900 words
- Short readable paragraphs
- Explain why the story matters
- Add industry context
- End with What Happens Next
- Do NOT include a title in the article
- Do NOT repeat the headline
- Do NOT use # headings
- Do NOT wrap the HTML in code fences

Headline:
{story["headline"]}

Summary:
{story["summary"]}

Category:
{story["category"]}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    html = response.output_text.strip()

    return {
        "title": story["headline"],
        "content": html,
        "excerpt": story["summary"],
        "category": story["category"],
        "category_id": CATEGORY_IDS[story["category"]],
    }


if __name__ == "__main__":

    test_story = {
        "headline": "Test Headline",
        "summary": "Test summary.",
        "category": "Movies"
    }

    article = write_article(test_story)

    print(article["title"])
    print(article["category"])
    print(article["category_id"])