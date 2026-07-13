"""
===========================================
ShowBiz Concert Guide Prompt
Version 1.0
===========================================

Prompt used by the AI writer to
generate the Weekly Concert Guide.

Author:
    ShowBiz Automation
"""

TITLE = "🎤 New Concerts & Tours"

PROMPT = """
Write a professional entertainment article for ShowBiz.com.

TITLE

🎤 New Concerts & Tours

GOAL

Create a weekly guide highlighting the
most interesting upcoming concerts,
tours and live music events in the
United States.

STYLE

• Professional entertainment journalism.

• Write for readers first.

• Avoid hype, clickbait and filler.

• Use natural language.

• Keep paragraphs short.

• Mention artists, venues and cities
  when relevant.

• Focus on why each concert is worth
  seeing.

USE THE PROVIDED DATA

The supplied concert data is your
primary source.

Prefer major artists, notable tours,
festival appearances and unique live
events.

Ignore obvious ticket packages,
VIP offers, season passes,
parking passes and promotional items.

If several entries are very similar,
choose only the strongest one.

FORMAT

Begin with a short introduction.

Then create one section for each
featured concert.

Each concert must use exactly:

<div class="movie-item">
<h3>Concert Name</h3>

<p>
Two or three informative paragraphs
about the artist, tour or event.
Include venue, city and concert date
when available.
</p>

</div>

Include between 10 and 15 concerts.

Finish with a short closing paragraph
encouraging readers to check local
availability and tour schedules.

Return HTML only.

Do not wrap the response in Markdown.

Do not include CSS.

Do not include JavaScript.

Do not invent concerts that are not
present in the supplied data.
"""