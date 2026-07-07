"""
===========================================
ShowBiz Featured Entertainer Writer
Version 3.0
===========================================

Converts a Featured Entertainer profile into
a complete HTML article.

This module only renders HTML.

It does not call AI.
It does not publish.
It does not access WordPress.

Author:
    ShowBiz Automation
"""

from __future__ import annotations

from datetime import datetime


# --------------------------------------------------
# HTML HELPERS
# --------------------------------------------------


def _section(title: str, body: str) -> str:
    """
    Render a standard ShowBiz section.
    """

    if not body:
        return ""

    body = body.strip()

    if not body:
        return ""

    return f"""

<h2>{title}</h2>

{body}

"""


def _paragraph(text: str) -> str:
    """
    Render a paragraph.
    """

    if not text:
        return ""

    return f"<p>{text.strip()}</p>"


def _bullet_list(items) -> str:
    """
    Render a bullet list.
    """

    if not items:
        return ""

    html = "<ul>\n"

    for item in items:

        if item:

            html += (
                f"<li>{str(item).strip()}</li>\n"
            )

    html += "</ul>\n"

    return html


def _field(label: str, value) -> str:
    """
    Render a labeled field.

    Lists become bullet lists.
    """

    if not value:
        return ""

    if isinstance(value, list):

        html = (
            f"<p><strong>{label}</strong></p>\n"
        )

        html += _bullet_list(value)

        return html

    return (
        f"<p><strong>{label}:</strong> "
        f"{value}</p>\n"
    )


# --------------------------------------------------
# HERO
# --------------------------------------------------


def render_hero(profile: dict) -> str:
    """
    Render the page hero.
    """

    today = datetime.now().strftime(
        "%B %d, %Y"
    )

    headline = profile.get(
        "headline",
        ""
    )

    intro = profile.get(
        "opening_feature",
        ""
    )

    name = profile.get(
        "name",
        ""
    )

    return f"""
<p><strong>{today}</strong></p>

<h1>{headline}</h1>

<p>
<strong>{name}</strong>
</p>

{_paragraph(intro)}
"""
# --------------------------------------------------
# QUICK FACTS
# --------------------------------------------------


def render_quick_facts(profile: dict) -> str:
    """
    Render the Quick Facts table.
    """

    facts = profile.get(
        "quick_facts",
        {}
    )

    if not facts:
        return ""

    html = """
<div class="showbiz-quick-facts">

<h2>Quick Facts</h2>

<table class="showbiz-facts">
"""

    rows = [
        ("Born", "born"),
        ("Birth Name", "birth_name"),
        ("Age", "age"),
        ("Birthplace", "birthplace"),
        ("Nationality", "nationality"),
        ("Occupation", "occupation"),
        ("Years Active", "years_active"),
        ("Residence", "current_residence"),
        ("Spouse", "spouse"),
        ("Children", "children"),
    ]

    for label, key in rows:

        value = facts.get(key)

        if not value:
            continue

        if isinstance(value, list):

            value = ", ".join(
                str(v) for v in value
            )

        html += f"""
<tr>
    <td><strong>{label}</strong></td>
    <td>{value}</td>
</tr>
"""

    html += """
</table>

</div>
"""

    return html
# --------------------------------------------------
# BIOGRAPHY
# --------------------------------------------------


def render_biography(profile: dict) -> str:
    """
    Render the biography section.
    """

    html = ""

    early_life = profile.get(
        "early_life",
        ""
    )

    family = profile.get(
        "family",
        {}
    )

    career_story = profile.get(
        "career_story",
        ""
    )

    if early_life:

        html += _section(
            "Early Life",
            _paragraph(early_life),
        )

    if family:

        body = ""

        rows = [
            ("Parents", "parents"),
            ("Siblings", "siblings"),
            ("Spouse", "spouse"),
            ("Children", "children"),
            ("Residence", "current_residence"),
        ]

        for label, key in rows:

            value = family.get(key)

            body += _field(
                label,
                value,
            )

        if body:

            html += _section(
                "Family",
                body,
            )

    if career_story:

        html += _section(
            "Career",
            _paragraph(career_story),
        )

    return html
# --------------------------------------------------
# TELEVISION
# --------------------------------------------------


def render_television(profile: dict) -> str:
    """
    Render notable television credits.
    """

    shows = profile.get(
        "television",
        []
    )

    if not shows:
        return ""

    html = "<ul>\n"

    for show in shows:

        #
        # Future-proof:
        #
        # Accept either:
        #
        # "Friends"
        #
        # or
        #
        # {
        #     "title": "...",
        #     "years": "...",
        #     "role": "..."
        # }
        #

        if isinstance(show, dict):

            line = show.get(
                "title",
                ""
            )

            years = show.get(
                "years",
                ""
            )

            role = show.get(
                "role",
                ""
            )

            if years:
                line += f" ({years})"

            if role:
                line += f" — {role}"

        else:

            line = str(show)

        html += f"<li>{line}</li>\n"

    html += "</ul>"

    return _section(
        "Television",
        html,
    )


# --------------------------------------------------
# FILMOGRAPHY
# --------------------------------------------------


def render_films(profile: dict) -> str:
    """
    Render notable film credits.
    """

    films = profile.get(
        "films",
        []
    )

    if not films:
        return ""

    html = "<ul>\n"

    for film in films:

        if isinstance(film, dict):

            line = film.get(
                "title",
                ""
            )

            year = film.get(
                "year",
                ""
            )

            role = film.get(
                "role",
                ""
            )

            if year:
                line += f" ({year})"

            if role:
                line += f" — {role}"

        else:

            line = str(film)

        html += f"<li>{line}</li>\n"

    html += "</ul>"

    return _section(
        "Filmography",
        html,
    )
# --------------------------------------------------
# AWARDS
# --------------------------------------------------


def render_awards(profile: dict) -> str:
    """
    Render awards and honors.
    """

    awards = profile.get(
        "awards",
        []
    )

    if not awards:
        return ""

    #
    # Future enhancement:
    #
    # This section will eventually render
    # as a sortable HTML table.
    #

    html = "<ul>\n"

    for award in awards:

        if isinstance(award, dict):

            line = ""

            year = award.get(
                "year",
                ""
            )

            if year:
                line += f"{year} — "

            line += award.get(
                "award",
                ""
            )

            category = award.get(
                "category",
                ""
            )

            if category:
                line += (
                    f" ({category})"
                )

            result = award.get(
                "result",
                ""
            )

            if result:
                line += (
                    f" — {result}"
                )

        else:

            line = str(award)

        html += f"<li>{line}</li>\n"

    html += "</ul>"

    return _section(
        "Awards & Honors",
        html,
    )


# --------------------------------------------------
# BUSINESS
# --------------------------------------------------


def render_business(profile: dict) -> str:
    """
    Render business ventures.
    """

    ventures = profile.get(
        "business_ventures",
        []
    )

    if not ventures:
        return ""

    return _section(
        "Business Ventures",
        _bullet_list(ventures),
    )


# --------------------------------------------------
# PHILANTHROPY
# --------------------------------------------------


def render_philanthropy(profile: dict) -> str:
    """
    Render charitable work.
    """

    philanthropy = profile.get(
        "philanthropy",
        []
    )

    if not philanthropy:
        return ""

    return _section(
        "Philanthropy",
        _bullet_list(philanthropy),
    )


# --------------------------------------------------
# CURRENT PROJECTS
# --------------------------------------------------


def render_current_projects(profile: dict) -> str:
    """
    Render current projects.
    """

    projects = profile.get(
        "current_projects",
        []
    )

    if not projects:
        return ""

    return _section(
        "Current Projects",
        _bullet_list(projects),
    )
# --------------------------------------------------
# INTERESTING FACTS
# --------------------------------------------------


def render_interesting_facts(profile: dict) -> str:
    """
    Render interesting facts.
    """

    facts = profile.get(
        "interesting_facts",
        []
    )

    if not facts:
        return ""

    return _section(
        "Interesting Facts",
        _bullet_list(facts),
    )


# --------------------------------------------------
# WHY FEATURED
# --------------------------------------------------


def render_why_featured(profile: dict) -> str:
    """
    Explain why ShowBiz selected this entertainer.
    """

    text = profile.get(
        "why_featured",
        ""
    )

    if not text:
        return ""

    return _section(
        "Why ShowBiz Selected This Entertainer",
        _paragraph(text),
    )


# --------------------------------------------------
# WATCH NEXT
# --------------------------------------------------


def render_watch_next(profile: dict) -> str:
    """
    Render watch-next recommendations.
    """

    items = profile.get(
        "watch_next",
        []
    )

    if not items:
        return ""

    return _section(
        "Watch Next",
        _bullet_list(items),
    )


# --------------------------------------------------
# ARTICLE WRITER
# --------------------------------------------------


def write_featured_entertainer(
    profile: dict,
) -> dict:
    """
    Convert a Featured Entertainer profile into
    a complete ShowBiz article.
    """

    sections = [
        render_hero(profile),
        render_quick_facts(profile),
        render_biography(profile),
        render_television(profile),
        render_films(profile),
        render_awards(profile),
        render_business(profile),
        render_philanthropy(profile),
        render_current_projects(profile),
        render_interesting_facts(profile),
        render_why_featured(profile),
        render_watch_next(profile),
    ]

    html = "".join(sections)

    title = (
        "Featured Entertainer of the Week: "
        f"{profile.get('name', '')}"
    )

    excerpt = profile.get(
        "headline",
        ""
    )

    return {
        "title": title,
        "content": html,
        "excerpt": excerpt,
        "category": "Featured Entertainer",
        "category_id": 55,
    }