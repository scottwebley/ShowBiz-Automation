from datetime import datetime


def write_featured_entertainer(report):
    """
    Converts the Featured Entertainer JSON into
    a complete HTML article for ShowBiz.com.
    """

    week = report.get("week", "")
    generated_date = report.get(
        "generated_date",
        datetime.now().strftime("%B %d, %Y")
    )

    html = f"""
<p><strong>{week}</strong></p>

<p>
Each week, the ShowBiz.com editorial team recognizes one performer
whose work, accomplishments, or headline-making news had the biggest
impact across the entertainment industry.
</p>

<h2>⭐ Featured Entertainer: {report["name"]}</h2>

<p><strong>{report["profession"]}</strong></p>

<h2>📰 This Week's Headline</h2>

<p>{report["headline"]}</p>

<h2>🎭 Why They Were Selected</h2>

<p>{report["why_selected"]}</p>

<h2>📖 Weekly Summary</h2>

<p>{report["summary"]}</p>

<h2>🏆 Career Highlights</h2>

<ul>
"""

    for item in report["career_highlights"]:
        html += f"<li>{item}</li>\n"

    html += """
</ul>

<h2>🎬 Recent Projects</h2>

<ul>
"""

    for item in report["recent_projects"]:
        html += f"<li>{item}</li>\n"

    html += """
</ul>
"""

    if report.get("fun_fact", "").strip():
        html += f"""
<h2>🎉 Fun Fact</h2>

<p>{report["fun_fact"]}</p>
"""

    if report.get("quote", "").strip():
        html += f"""
<h2>💬 Quote</h2>

<blockquote>
{report["quote"]}
</blockquote>
"""

    html += """
<h2>👀 Watch Next</h2>

<ul>
"""

    for item in report["watch_next"]:
        html += f"<li>{item}</li>\n"

    html += f"""
</ul>

<p>
Published: {generated_date}
</p>

<p>
Check back next week for another edition of
<strong>Featured Entertainer of the Week.</strong>
</p>
"""

    return {
        "title": f"⭐ Featured Entertainer of the Week - {week}",
        "content": html,
        "excerpt": (
            f"This week's Featured Entertainer is "
            f'{report["name"]}, recognized for making the biggest impact '
            "across entertainment."
        ),
        "category": "Entertainment Industry",
        "category_id": 56,
    }


if __name__ == "__main__":

    sample = {
        "name": "Taylor Swift",
        "profession": "Singer-songwriter",
        "headline": "Taylor Swift announces surprise stadium tour dates",
        "summary": (
            "Taylor Swift generated major entertainment headlines after "
            "announcing surprise stadium tour dates."
        ),
        "why_selected": (
            "Her announcement dominated entertainment conversation and "
            "generated widespread fan excitement."
        ),
        "career_highlights": [
            "Multiple Grammy Award winner",
            "Record-breaking global touring artist",
            "One of the world's best-selling recording artists"
        ],
        "recent_projects": [
            "Surprise stadium tour announcement",
            "The Eras Tour",
            "Taylor Swift: The Eras Tour"
        ],
        "fun_fact": (
            "Taylor Swift has repeatedly broken concert attendance "
            "and touring revenue records."
        ),
        "quote": "",
        "watch_next": [
            "Upcoming stadium tour dates",
            "New music announcements",
            "Future live performances"
        ],
        "week": "Week of July 4, 2026",
        "generated_date": "July 4, 2026"
    }

    article = write_featured_entertainer(sample)

    print(article["title"])
    print()
    print(article["content"][:800])