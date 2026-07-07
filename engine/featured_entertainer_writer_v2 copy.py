"""
===========================================
ShowBiz Featured Entertainer Writer
Version 2.0
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


def _section(title: str, body: str) -> str:
    """
    Render a standard ShowBiz section.
    """

    if not body.strip():
        return ""

    return f"""
<h2>{title}</h2>

{body}
"""


def _paragraph(text: str) -> str:

    if not text:
        return ""

    return f"<p>{text}</p>"


def _bullet_list(items) -> str:

    if not items:
        return ""

    html = "<ul>\n"

    for item in items:

        html += f"<li>{item}</li>\n"

    html += "</ul>\n"

    return html
...


def render_hero(profile: dict) -> str:

    today = datetime.now().strftime("%B %d, %Y")

    headline = profile.get(
        "headline",
        ""
    )

    intro = profile.get(
        "opening_feature",
        ""
    )

    return f"""
<p><strong>{today}</strong></p>

<h1>{headline}</h1>

<p>
<strong>{profile.get("name","")}</strong>
</p>

<p>
{intro}
</p>
"""
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
        ("Nationality", "nationality"),
        ("Occupation", "occupation"),
        ("Years Active", "years_active"),
        ("Residence", "current_residence"),
        ("Spouse", "spouse"),
        ("Children", "children"),
    ]

    for label, key in rows:

        value = facts.get(key)

        if value:

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

        labels = [
            ("Parents", "parents"),
            ("Siblings", "siblings"),
            ("Spouse", "spouse"),
            ("Children", "children"),
            ("Residence", "current_residence"),
        ]

        for label, key in labels:

            value = family.get(key)

            if value:

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

    html = ""

    for show in shows:

        if isinstance(show, dict):

            title = show.get("title", "")
            years = show.get("years", "")
            role = show.get("role", "")

            line = title

            if years:
                line += f" ({years})"

            if role:
                line += f" — {role}"

            html += f"<li>{line}</li>\n"

        else:

            html += f"<li>{show}</li>\n"

    return _section(
        "Television",
        f"<ul>\n{html}</ul>"
    )


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

    html = ""

    for film in films:

        if isinstance(film, dict):

            title = film.get("title", "")
            year = film.get("year", "")
            role = film.get("role", "")

            line = title

            if year:
                line += f" ({year})"

            if role:
                line += f" — {role}"

            html += f"<li>{line}</li>\n"

        else:

            html += f"<li>{film}</li>\n"

    return _section(
        "Filmography",
        f"<ul>\n{html}</ul>"
    )
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

    html = ""

    for award in awards:

        if isinstance(award, dict):

            year = award.get("year", "")
            name = award.get("award", "")
            category = award.get("category", "")
            result = award.get("result", "")

            line = ""

            if year:
                line += f"{year} — "

            line += name

            if category:
                line += f" ({category})"

            if result:
                line += f" — {result}"

            html += f"<li>{line}</li>\n"

        else:

            html += f"<li>{award}</li>\n"

    return _section(
        "Awards & Honors",
        f"<ul>\n{html}</ul>"
    )


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


def render_watch_next(profile: dict) -> str:
    """
    Render watch next recommendations.
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


def render_why_featured(profile: dict) -> str:
    """
    Explain why ShowBiz selected
    this entertainer.
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


def write_featured_entertainer(profile: dict) -> dict:
    """
    Convert a profile dictionary into
    a complete ShowBiz article.
    """

    html = ""

    html += render_hero(profile)
    html += render_quick_facts(profile)
    html += render_biography(profile)
    html += render_television(profile)
    html += render_films(profile)
    html += render_awards(profile)
    html += render_business(profile)
    html += render_philanthropy(profile)
    html += render_current_projects(profile)
    html += render_interesting_facts(profile)
    html += render_why_featured(profile)
    html += render_watch_next(profile)

    title = (
        f"⭐ Featured Entertainer of the Week: "
        f"{profile.get('name', '')}"
    )

    excerpt = (
        profile.get(
            "headline",
            ""
        )
    )

    return {
        "title": title,
        "content": html,
        "excerpt": excerpt,
        "category": "Featured Entertainer",
        "category_id": 55,
    }