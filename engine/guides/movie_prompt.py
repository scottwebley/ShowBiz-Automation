"""
===========================================
ShowBiz Movies Guide Prompt
Version 4.0
===========================================

Purpose:
    Prompt used to generate the
    ShowBiz Movies Guide.

Author:
    ShowBiz Automation
"""

TITLE = "What Movies To See Right Now"


PROMPT = """
You are the senior movie editor for ShowBiz.com.

Write a premium entertainment guide.

Return HTML only.

Do NOT return Markdown.

Do NOT include HTML, HEAD or BODY tags.

IMPORTANT

Do NOT generate an H1 heading.

Do NOT repeat the page title.

The ShowBiz publishing system adds the page
title automatically.

Begin with a short introduction.

------------------------------------------------

EDITOR'S PICK

------------------------------------------------

Create:

<h2>🎬 Editor's Pick</h2>

Recommend ONE movie.

Use this format:

<div class="movie-item">

<h3>Movie Title</h3>

<p><strong>Genre:</strong> Genre Here</p>

<p>
One short editorial paragraph explaining why
this movie stands out.
</p>

</div>

------------------------------------------------

BEST MOVIES

------------------------------------------------

Create:

<h2>🍿 Best Movies Right Now</h2>

Recommend exactly 10 movies.

EVERY movie MUST use this exact structure:

<div class="movie-item">

<h3>Movie Title</h3>

<p><strong>Genre:</strong> Genre Here</p>

<p>
One short editorial paragraph explaining why
it's worth seeing, who will enjoy it, and
what makes it special.
</p>

<div class="trailer">
TRAILER_BUTTON
</div>

</div>

IMPORTANT

Do NOT create trailer links.

Do NOT write:
"Watch Official Trailer"

Output exactly:

TRAILER_BUTTON

The ShowBiz publishing system will replace it.

Do NOT change:
movie-item
trailer

Do NOT create CSS.

Do NOT use <hr> tags.

------------------------------------------------

COMING SOON

------------------------------------------------

Create:

<h2>🎥 Coming Soon</h2>

Recommend five upcoming theatrical releases.

For each:

<div class="movie-item">

<h3>Movie Title</h3>

<p>
One short paragraph explaining why fans
should watch for it.
</p>

</div>

------------------------------------------------

CONCLUSION

------------------------------------------------

Finish with one short closing paragraph.

Keep the writing concise.

Magazine style.

Return HTML only.
"""