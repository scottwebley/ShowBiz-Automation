"""
===========================================
ShowBiz AI Writer Core
Version 2.0
===========================================

Core implementation for article generation.

Public API:
    write_article_core(story)

Called by:
    engine.ai_writer
"""

from engine.openai_helper import create_response


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
# ==========================================================

CATEGORY_ALIASES = {

    "Television": "TV & Streaming",
    "TV": "TV & Streaming",
    "Streaming": "TV & Streaming",

    "Celebrity": "Celebrity News",
    "Celebrities": "Celebrity News",
    "Stars": "Celebrity News",

    "Movie": "Movies",
    "Film": "Movies",

    "Awards": "Entertainment Industry",
    "Award": "Entertainment Industry",
    "Award Show": "Entertainment Industry",

    "Concert": "Music",
    "Tours": "Music",

    "Broadway": "Entertainment Industry",
    "Festival": "Entertainment Industry",
}


# ==========================================================
# WordPress Top Story Category
# ==========================================================

TOP_STORY_CATEGORY_ID = 64


def normalize_category(category):
    """
    Normalize AI category names into
    WordPress category names.
    """

    category = CATEGORY_ALIASES.get(
        category,
        category,
    )

    if category not in CATEGORY_IDS:

        print(
            f"Unknown category '{category}' "
            "-> Entertainment Industry"
        )

        category = "Entertainment Industry"

    return category


def build_prompt(story, category):
    """
    Build article generation prompt.
    """

    return f"""
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


def write_article_core(story):
    """
    Generate a ShowBiz article.

    Returns:
        dict on success
        None on failure
    """

    from engine.guides.trailer_finder import trailer_button

    TRAILER_KEYWORDS = (
        "trailer",
        "teaser",
        "official trailer",
        "teaser trailer",
        "first look",
    )

    category = normalize_category(
        story.get(
            "category",
            "Entertainment Industry",
        )
    )

    prompt = build_prompt(
        story,
        category,
    )

    try:

        response = create_response(
            model="gpt-5.5",
            input=prompt,
        )

    except Exception as e:

        print("\n========================================")
        print("AI WRITER")
        print("========================================")
        print(f"Unable to generate article:\n{e}")
        print("Skipping publication.\n")

        return None

    html = response.output_text.strip()

    if not html:

        print(
            "\nAI Writer returned an empty article.\n"
        )

        return None

    # ---------------------------------------------------------
    # Add Watch Trailer button for trailer stories
    # ---------------------------------------------------------

    headline = story.get("headline", "")

    if any(
        keyword in headline.lower()
        for keyword in TRAILER_KEYWORDS
    ):

        try:

            button = trailer_button(title=headline)

            if button:

                first_paragraph = html.find("</p>")

                if first_paragraph != -1:

                    trailer_html = (
                        "\n"
                        "<h3>🎬 Watch the Trailer</h3>\n"
                        f"{button}\n"
                    )

                    html = (
                        html[:first_paragraph + 4]
                        + trailer_html
                        + html[first_paragraph + 4:]
                    )

                    print("✓ Trailer button added.")

        except Exception as exc:

            print(f"Trailer lookup failed: {exc}")

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