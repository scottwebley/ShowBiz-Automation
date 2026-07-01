from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# ==========================================================
# WordPress Category IDs
# ==========================================================

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

# ==========================================================
# AI Category Aliases
#
# GPT occasionally invents category names.
# Convert them to valid ShowBiz categories.
# ==========================================================

CATEGORY_ALIASES = {

    # TV

    "Television": "TV & Streaming",
    "TV": "TV & Streaming",
    "Streaming": "TV & Streaming",

    # Celebrity

    "Celebrity": "Celebrity News",
    "Celebrities": "Celebrity News",
    "Stars": "Celebrity News",

    # Movies

    "Movie": "Movies",
    "Film": "Movies",

    # Awards

    "Awards": "Entertainment Industry",
    "Award": "Entertainment Industry",
    "Award Show": "Entertainment Industry",

    # Music

    "Concert": "Music",
    "Tours": "Music",

    # Default entertainment bucket

    "Broadway": "Entertainment Industry",
    "Festival": "Entertainment Industry",
}

# ==========================================================
# WordPress Top Story category
# ==========================================================

TOP_STORY_CATEGORY_ID = 64


def write_article(story):
    """
    Write a ShowBiz article and return everything
    needed for WordPress publishing.
    """

    category = story.get(
        "category",
        "Entertainment Industry",
    )

    #
    # Normalize category names
    #

    category = CATEGORY_ALIASES.get(
        category,
        category,
    )

    #
    # Final safety net.
    # Never allow an unknown category
    # to crash production.
    #

    if category not in CATEGORY_IDS:

        print(
            f"Unknown category '{category}' "
            "-> Entertainment Industry"
        )

        category = "Entertainment Industry"

    prompt = f"""
You are a senior entertainment journalist writing for ShowBiz.com.

Write a completely original entertainment news article.

Do NOT copy wording from any publication.

Write in a professional entertainment news style similar in quality to
Variety, Deadline or The Hollywood Reporter while maintaining a unique voice.

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
{category}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    html = response.output_text.strip()

    #
    # Every Top Story belongs to:
    #
    #   Top Story
    #   Editorial Category
    #

    category_ids = [
        TOP_STORY_CATEGORY_ID,
        CATEGORY_IDS[category],
    ]

    return {
        "title": story["headline"],
        "content": html,
        "excerpt": story["summary"],
        "category": category,
        "category_ids": category_ids,
    }


if __name__ == "__main__":

    test_story = {
        "headline": "Danny Glover Reveals Alzheimer's Diagnosis",
        "summary": "Test summary.",
        "category": "Celebrity",
    }

    article = write_article(test_story)

    print(article["title"])
    print(article["category"])
    print(article["category_ids"])