"""
===========================================
ShowBiz HTML Builder
Version 1.0
===========================================

Purpose:
    Build consistent HTML for
    ShowBiz Guide pages.

This module does NOT:

    • Call OpenAI
    • Publish to WordPress
    • Find trailers
    • Find posters

Author:
    ShowBiz Automation
"""


def build_page(title, body, updated=None):
    """
    Build a complete ShowBiz Guide page.

    Args:
        title (str)
        body (str)
        updated (str | None)

    Returns:
        str
    """

    parts = []

    parts.append(
        '<section class="showbiz-guide">'
    )

    parts.append(
        f"<h1>{title}</h1>"
    )

    if updated:
        parts.append(
            (
                '<p class="showbiz-updated">'
                f"<strong>Updated:</strong> {updated}"
                "</p>"
            )
        )

    parts.append(body)

    parts.append("</section>")

    return "\n".join(parts)


def trailer_button(url):
    """
    Build a trailer button.
    """

    return (
        '<p>'
        '<a class="showbiz-trailer-button" '
        f'href="{url}" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        '▶ Watch Official Trailer'
        '</a>'
        '</p>'
    )


def editors_pick():
    """
    Return the Editor's Pick badge.
    """

    return (
        '<div class="showbiz-editors-pick">'
        '🏆 Editor\'s Pick'
        '</div>'
    )


if __name__ == "__main__":

    html = build_page(
        title="Test Guide",
        body="<p>Hello ShowBiz.</p>",
        updated="July 2026",
    )

    print(html)