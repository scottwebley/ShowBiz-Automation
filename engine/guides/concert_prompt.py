"""
===========================================
ShowBiz Concert Guide Prompt
Version 2.1
===========================================

Prompt used by the AI writer to
generate the Weekly Concert Guide.
"""

TITLE = "🎤 New Concerts & Tours"

PROMPT = """
Write a professional entertainment article for ShowBiz.com.

TITLE

🎤 New Concerts & Tours

GOAL

Create a weekly guide covering the
best upcoming concerts and live music
events in the United States.

STYLE

• Professional entertainment journalism.

• Write for readers first.

• Avoid hype, clickbait and filler.

• Use natural language.

• Keep paragraphs short.

• Mention artists, venues, cities and
  concert dates when relevant.

• Focus on why each performance is
  worth seeing.

USE THE PROVIDED DATA

The supplied concert data is your
only source.

Use ONLY the supplied concerts.

Do NOT invent concerts.

Do NOT invent tour dates.

Do NOT invent additional tour stops.

Do NOT invent tour history.

Do NOT invent future appearances.

Do NOT invent venue information.

CONCERT SELECTION

The supplied concerts have already
been editorially selected and ranked.

Create one section for EVERY supplied
concert.

Do NOT omit concerts.

Do NOT replace concerts with others.

Do NOT reorder the concerts.

Write about the concerts in the exact
order they are provided.

Ignore obvious ticket packages,
VIP offers, season passes,
parking passes and promotional items
only if they appear in the supplied data.

FORMAT

Begin with a short introduction.

Then create one section for EACH
concert provided.

Each concert must use exactly:

<div class="movie-item">
<h3>Concert Name</h3>

<p>
Write two or three informative
paragraphs about the artist and the
upcoming performance.

Include the venue, city and concert
date when available.

Explain why fans may be interested in
this performance using ONLY the
supplied information.
</p>

</div>

Create one section for every supplied
concert.

Do NOT skip any concert.

Finish with a short closing paragraph
encouraging readers to check official
ticket availability and event details.

Return HTML only.

Do not wrap the response in Markdown.

Do not include CSS.

Do not include JavaScript.
"""