"""
===========================================================
ShowBiz Event Registry Diagnostic Tool
Version 1.0

Downloads the raw Event Registry feed exactly as the
production newsroom sees it.

This tool DOES NOT filter, score, rank, or publish stories.

Usage:

    python3 tools/diagnose_event_registry.py

===========================================================
"""

from collections import Counter
from datetime import datetime
from pathlib import Path
import os

from dotenv import load_dotenv
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems

load_dotenv()

API_KEY = os.getenv("NEWSAPI_AI_KEY")

if not API_KEY:
    raise RuntimeError("NEWSAPI_AI_KEY not found in environment.")

er = EventRegistry(apiKey=API_KEY)

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

KEYWORDS = [
    "Taylor",
    "Swift",
    "Kelce",
    "Disney",
    "Netflix",
    "Warner",
    "Universal",
    "Paramount",
    "Marvel",
    "Apple",
]


def build_query():
    """
    Uses the EXACT same query as production.
    """

    return QueryArticlesIter(
        keywords=QueryItems.OR([
            "movies",
            "television",
            "streaming",
            "Netflix",
            "music",
            "celebrity",
            "Hollywood",
            "gaming",
            "Broadway",
            "awards",
        ]),
        lang="eng",
    )


def main():

    print("=" * 70)
    print(" SHOWBIZ EVENT REGISTRY DIAGNOSTIC")
    print("=" * 70)
    print()

    query = build_query()

    articles = []

    print("Downloading raw Event Registry feed...\n")

    for article in query.execQuery(
        er,
        sortBy="date",
        maxItems=200,
    ):

        articles.append(article)

    print(f"Downloaded {len(articles)} articles.\n")

    source_counter = Counter()

    keyword_hits = {k: 0 for k in KEYWORDS}

    report_lines = []

    for i, article in enumerate(articles, start=1):

        headline = article.get("title", "").strip()
        source = article.get("source", {}).get("title", "Unknown")
        published = article.get("dateTime", "")
        url = article.get("url", "")

        source_counter[source] += 1

        for keyword in KEYWORDS:
            if keyword.lower() in headline.lower():
                keyword_hits[keyword] += 1

        print(f"{i:03d}. {headline}")
        print(f"     Source    : {source}")
        print(f"     Published : {published}")
        print(f"     URL       : {url}")
        print()

        report_lines.append(f"{i:03d}. {headline}")
        report_lines.append(f"Source    : {source}")
        report_lines.append(f"Published : {published}")
        report_lines.append(f"URL       : {url}")
        report_lines.append("")

    print("=" * 70)
    print("SOURCE SUMMARY")
    print("=" * 70)

    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("SOURCE SUMMARY")
    report_lines.append("=" * 70)

    for source, count in source_counter.most_common():

        print(f"{source:<35} {count:>4}")

        report_lines.append(f"{source:<35} {count:>4}")

    print()
    print("=" * 70)
    print("KEYWORD MATCHES")
    print("=" * 70)

    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("KEYWORD MATCHES")
    report_lines.append("=" * 70)

    for keyword, count in keyword_hits.items():

        print(f"{keyword:<15} {count}")

        report_lines.append(f"{keyword:<15} {count}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = REPORT_DIR / f"event_registry_{timestamp}.txt"

    report_file.write_text("\n".join(report_lines), encoding="utf-8")

    print()
    print("=" * 70)
    print(f"Report saved to: {report_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()