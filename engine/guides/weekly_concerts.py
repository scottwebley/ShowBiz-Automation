"""
===========================================
ShowBiz Weekly Concert Guide
Version 2.0
===========================================

Generate and publish the
"New Concerts & Tours" guide.

Author:
    ShowBiz Automation
"""

from engine.guides.guide_writer import (
    write_guide,
)
from engine.guides.concert_guide_enricher import (
    enrich_guide,
)
from engine.guides.concert_prompt import (
    TITLE,
    PROMPT,
)
from engine.guides.concert_data import (
    get_concert_guide,
)
from engine.publisher import (
    publish_html,
)


PAGE_ID = 23748


def get_concerts():

    from engine.guides.concert_filters import (
        filter_concerts,
    )

    from engine.guides.concert_ranker import (
        rank_concerts,
    )

    concerts = get_concert_guide(
        limit=1000,
    )

    concerts = filter_concerts(
        concerts,
    )

    # Rank a larger pool first.
    concerts = rank_concerts(
        concerts,
        limit=1000,
    )

    # Final deduplication after scoring.
    unique = []
    seen = set()

    for concert in concerts:

        key = (
            concert.get("artist", "").strip().lower(),
            concert.get("event_date", "").strip(),
            concert.get("city", "").strip().lower(),
            concert.get("state", "").strip().lower(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(concert)

        if len(unique) >= 30:
            break

    concerts = unique

    print()
    print("========================================")
    print("FINAL TOP 30")
    print("========================================")

    for i, concert in enumerate(concerts, 1):

        print(
            f"{i:2}. "
            f"{concert.get('editorial_score', 0):4}  "
            f"{concert.get('title', '')}"
        )

    print()

    return concerts


def build_concert_context(
    concerts,
):

    if not concerts:

        return ""

    context = """

CURRENT CONCERT DATA:

Use ONLY the concerts below.

"""

    for concert in concerts:

        context += f"""

Title: {concert.get('title')}
Artist: {concert.get('artist')}
Date: {concert.get('event_date')}
Venue: {concert.get('venue')}
City: {concert.get('city')}
State: {concert.get('state')}

Overview: {concert.get('overview')}
Poster: {concert.get('poster')}
Event URL: {concert.get('url')}

"""

    return context


def build_guide():

    concerts = get_concerts()

    concert_context = build_concert_context(
        concerts
    )

    prompt = (
        PROMPT
        + concert_context
    )

    html = write_guide(
        title=TITLE,
        prompt=prompt,
    )

    with open(
        "concert_ai_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            html
        )

    enriched_html = enrich_guide(
        title=TITLE,
        html=html,
        concerts=concerts,
    )

    with open(
        "concert_enriched_output.html",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            enriched_html
        )

    return enriched_html


def publish_guide():

    html = build_guide()

    return publish_html(
        page_id=PAGE_ID,
        html=html,
    )


def main():

    print()
    print("========================================")
    print("UPDATING CONCERT GUIDE")
    print("========================================")

    success = publish_guide()

    print()

    if success:

        print(
            "✓ Concert Guide updated."
        )

        print(
            "✓ Saved concert_ai_output.html"
        )

        print(
            "✓ Saved concert_enriched_output.html"
        )

    else:

        print(
            "✗ Concert Guide failed."
        )


if __name__ == "__main__":

    main()