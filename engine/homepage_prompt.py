"""
===========================================
ShowBiz Homepage Prompt
Version 1.1
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

The homepage should prioritize stories
that matter most to readers RIGHT NOW.

Top Story Editorial Rules:

• Favor fresh developments over routine recurring events.
• Do not automatically rank awards nominations above major entertainment industry news.
• Major company announcements, studio moves, streaming platform changes, franchise developments, and historic entertainment events can outrank awards coverage.
• Consider cultural impact, reader interest, and industry significance.
• A major business or creative announcement may be more important than a standard annual event.
• Breaking news should generally outrank older or expected announcements.

Prioritize:

• Breaking entertainment news
• Major celebrity developments
• Major movie announcements
• Significant television and streaming developments
• Industry-changing announcements
• Box office stories
• Awards (especially winners, controversies, historic moments, and major announcements)
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