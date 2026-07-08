"""
===========================================
ShowBiz Homepage Prompt
Version 1.0
===========================================

Purpose:
    Build the GPT prompt used by the
    Homepage Ranker.

Author:
    ShowBiz Automation
"""

import json


def build_homepage_prompt(choices):
    """
    Build the homepage ranking prompt.

    Args:
        choices (list): Simplified story list.

    Returns:
        str: Prompt for GPT.
    """

    return f"""
You are the Editor-in-Chief of ShowBiz.com.

Below is today's approved entertainment news.

Your job is to rank EVERY story in the
order it should appear on the homepage.

Rank #1 should be the single most
important entertainment story.

Rank the remaining stories in descending
editorial importance.

Prioritize:

• Breaking entertainment news
• Major celebrities
• Movie announcements
• Television
• Streaming
• Box office
• Awards
• Music
• Broadway
• Gaming

Avoid promoting:

• Roundups
• SummaryBrief articles
• Tag pages
• Archive pages
• Evergreen articles
• Generic listicles
• Minor updates

Return ONLY valid JSON.

Example:

{{
    "homepage_ranking":
    [
        4,
        7,
        2,
        1,
        5,
        0,
        3,
        6
    ]
}}

Stories:

{json.dumps(choices, indent=2)}
"""