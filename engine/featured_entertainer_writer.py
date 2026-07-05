from datetime import datetime


def write_featured_entertainer(report):
    """
    Converts the Featured Entertainer JSON into
    a complete HTML article for ShowBiz.com.
    """

    today = datetime.now().strftime("%B %d, %Y")

    highlights = report.get("career_highlights", [])
    projects = report.get("recent_projects", [])
    watch_next = report.get("watch_next", [])

    html = f"""
<p><strong>{today}</strong></p>

<p>
Every week, ShowBiz.com recognizes one performer whose work,
achievements and news coverage made the biggest impact across
the entertainment industry.
</p>

<h2>⭐ Featured Entertainer of the Week</h2>

<p>
<strong>{report["name"]}</strong> has been selected as this week's
Featured Entertainer.
</p>

<p>
{report["why_selected"]}
</p>

<h2>About {report["name"]}</h2>

<p>
{report["summary"]}
</p>

<h2>Profession</h2>

<p>
{report["profession"]}
</p>

<h2>Career Highlights</h2>

<ul>
"""

    for item in highlights:
        html += f"<li>{item}</li>\n"

    html += """
</ul>

<h2>Recent Projects</h2>

<ul>
"""

    for item in projects:
        html += f"<li>{item}</li>\n"

    html += """
</ul>
"""

    if report.get("fun_fact"):

        html += f"""
<h2>Fun Fact</h2>

<p>
{report["fun_fact"]}
</p>
"""

    if report.get("quote"):

        html += f"""
<h2>Quote</h2>

<blockquote>
{report["quote"]}
</blockquote>
"""

    html += """
<h2>Watch Next</h2>

<ul>
"""

    for item in watch_next:
        html += f"<li>{item}</li>\n"

    html += f"""
</ul>

<h2>Why They Were Chosen</h2>

<p>
{report["why_selected"]}
</p>

<p>
This selection is based on ShowBiz.com's editorial analysis of
the week's biggest entertainment stories.
</p>

<p>
Visit ShowBiz.com every week for a new
<strong>Featured Entertainer of the Week</strong>.
</p>
"""

    title = (
        f"⭐ Featured Entertainer of the Week: "
        f"{report['name']}"
    )

    excerpt = (
        f"{report['name']} is ShowBiz.com's "
        f"Featured Entertainer of the Week."
    )

    return {
        "title": title,
        "content": html,
        "excerpt": excerpt,
        "category": "Featured Entertainer",
        "category_id": 55,
    }


if __name__ == "__main__":

    sample = {
        "name": "Taylor Swift",
        "profession": "Singer-Songwriter",
        "headline": "Taylor Swift dominates entertainment headlines",
        "summary": (
            "Taylor Swift captured worldwide attention this week "
            "following major entertainment news."
        ),
        "why_selected": (
            "She dominated entertainment coverage throughout the week."
        ),
        "career_highlights": [
            "Multiple Grammy Award winner",
            "Record-breaking world tours",
            "One of the world's best-selling artists",
        ],
        "recent_projects": [
            "International concert tour",
            "New music releases",
            "High-profile public appearances",
        ],
        "fun_fact": (
            "She is the first artist to occupy the entire Top 10 "
            "of the Billboard Hot 100."
        ),
        "quote": "",
        "watch_next": [
            "Upcoming tour announcements",
            "Future music releases",
            "Award season appearances",
        ],
    }

    article = write_featured_entertainer(sample)

    print(article["title"])
    print()
    print(article["content"][:1200])