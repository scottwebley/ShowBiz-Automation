"""
===========================================
ShowBiz Movies Guide Prompt
Version 4.1
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

IMPORTANT EDITORIAL RULES

Use the supplied movie data only.

A movie may appear ONLY ONCE on the page.

If a movie is selected for Editor's Pick,
do NOT repeat it anywhere else.

Movies in "Best Movies Right Now" must NOT
appear in "Coming Soon".

Movies in "Coming Soon" must NOT appear in
Editor's Pick.

Movies in "Coming Soon" must NOT appear in
"Best Movies Right Now".

For "Best Movies Right Now", choose ONLY
movies that have already been released.

For "Coming Soon", choose ONLY movies whose
release date is in the future.

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

Recommend exactly 10 different movies.

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

Recommend exactly five different upcoming
theatrical releases.

For each:

<div class="movie-item">

<h3>Movie Title</h3>

<p>
<strong>In theaters:</strong> Release Date
</p>

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