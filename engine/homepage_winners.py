def generate_homepage_winners(report):
    """
    Generates the homepage HTML block for the
    Entertainment Winners & Losers section.
    """

    winner = report["winner"]["name"]
    reason = report["winner"]["reason"]

    html = f"""
<h2>🏆 ENTERTAINMENT WINNERS & LOSERS OF THE DAY</h2>

<p>
Every day ShowBiz.com highlights the biggest winners,
losers and trends shaping today's entertainment industry.
</p>

<p>
<strong>🏆 Winner: {winner}</strong>
</p>

<p>
{reason}
</p>

<p>
<a href="/entertainment-winners-losers/">
<strong>Read Full Report →</strong>
</a>
</p>
"""

    return html


if __name__ == "__main__":

    sample = {
        "winner": {
            "name": "Christopher Nolan",
            "reason": (
                "The announcement of his next film became today's "
                "biggest entertainment story."
            )
        }
    }

    print(generate_homepage_winners(sample))