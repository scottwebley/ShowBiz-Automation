"""
===========================================
ShowBiz Guide Writer
Version 1.0
===========================================

Purpose:
    Generate HTML for a ShowBiz Guide.

This module does NOT:

    • Publish to WordPress
    • Select images
    • Schedule guides

It simply sends a prompt to OpenAI and
returns HTML.

Public Functions:

    write_guide()

Author:
    ShowBiz Automation
"""

from engine.openai_helper import create_response


DEFAULT_MODEL = "gpt-5.5"


def write_guide(
    title: str,
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate guide HTML.

    Args:
        title: Guide title.
        prompt: Full guide prompt.
        model: OpenAI model.

    Returns:
        HTML string.

    Raises:
        RuntimeError if no HTML is returned.
    """

    response = create_response(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are the ShowBiz editorial team. "
                    "Return HTML only. "
                    "Do not wrap the response in markdown."
                ),
            },
            {
                "role": "user",
                "content": f"{title}\n\n{prompt}",
            },
        ],
    )

    html = getattr(response, "output_text", "")

    if html:
        return html.strip()

    # Fallback for SDKs that do not expose output_text
    try:
        html = (
            response.output[0]
            .content[0]
            .text
        )
    except Exception as exc:
        raise RuntimeError(
            "OpenAI returned no guide HTML."
        ) from exc

    html = html.strip()

    if not html:
        raise RuntimeError(
            "OpenAI returned an empty guide."
        )

    return html


if __name__ == "__main__":

    print("Guide Writer")
    print("Import write_guide() from a guide module.")