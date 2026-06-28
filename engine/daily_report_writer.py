from datetime import datetime


def write_daily_report(report):
    """
    Converts the Daily Report JSON into
    a complete HTML article for ShowBiz.com.
    """

    today = datetime.now().strftime("%B %d, %Y")

    html = f"""
<p><strong>{today}</strong></p>

<p>
Every day, ShowBiz.com highlights the biggest winners, losers,
and trends shaping the entertainment industry.
</p>

<h2>🏆 Winner of the Day: {report["winner"]["name"]}</h2>

<p>{report["winner"]["reason"]}</p>

<h2>📉 Loser of the Day: {report["loser"]["name"]}</h2>

<p>{report["loser"]["reason"]}</p>

<h2>🎬 Trending Movie: {report["trending_movie"]["title"]}</h2>

<p>{report["trending_movie"]["reason"]}</p>

<h2>🎤 Trending Artist: {report["trending_artist"]["name"]}</h2>

<p>{report["trending_artist"]["reason"]}</p>

<h2>🔥 Trend to Watch: {report["trend_to_watch"]["title"]}</h2>

<p>{report["trend_to_watch"]["description"]}</p>

<h2>⭐ ShowBiz Take</h2>

<p>{report["showbiz_take"]}</p>

<h2>👀 Tomorrow's Watch List</h2>

<ul>
"""

    for item in report["watch_list"]:
        html += f"<li>{item}</li>\n"

    html += """
</ul>

<p>
Check back tomorrow for another edition of
<strong>Entertainment Winners & Losers of the Day.</strong>
</p>
"""

    return {
        "title": f"🏆 Entertainment Winners & Losers of the Day - {today}",
        "content": html,
        "excerpt": "The biggest winners, losers and trends shaping today's entertainment industry.",
        "category": "Entertainment Industry",
        "category_id": 56,
    }


if __name__ == "__main__":

    sample = {
        "winner": {
            "name": "Christopher Nolan",
            "reason": "Major film announcement."
        },
        "loser": {
            "name": "No Clear Loser",
            "reason": "Today's news cycle was largely positive."
        },
        "trending_movie": {
            "title": "Christopher Nolan's Next Film",
            "reason": "Dominating today's movie news."
        },
        "trending_artist": {
            "name": "Olivia Rodrigo",
            "reason": "Strong streaming and festival buzz."
        },
        "trend_to_watch": {
            "title": "Global Streaming",
            "description": "International audiences continue driving entertainment."
        },
        "showbiz_take":
            "Today's biggest stories show audiences continue rewarding premium entertainment.",

        "watch_list": [
            "Weekend Box Office",
            "Netflix Announcements",
            "Marvel News",
            "Music Charts",
            "Casting Updates"
        ]
    }

    article = write_daily_report(sample)

    print(article["title"])
    print()
    print(article["content"][:800])