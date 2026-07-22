"""
===========================================
ShowBiz AI Writer
Version 2.0
===========================================

Public API for article generation.

The implementation lives in
engine.ai_writer_core.

This file intentionally stays small and
stable so production callers never change.
"""

from engine.ai_writer_core import write_article_core


def write_article(story):
    """
    Generate a publishable article.

    Args:
        story (dict): Selected Top Story.

    Returns:
        dict | None
    """
    return write_article_core(story)


#
# Test
#

if __name__ == "__main__":

    test_story = {
        "headline": "Danny Glover Reveals Alzheimer's Diagnosis",
        "summary": "Test summary.",
        "category": "Celebrity",
    }

    article = write_article(test_story)

    if article is None:

        print("\nArticle generation failed.")

    else:

        print(article["title"])
        print(article["category"])
        print(article["category_ids"])