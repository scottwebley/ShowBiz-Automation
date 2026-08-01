# ShowBiz Guide System

Version 1.0

---

# Purpose

The Guide System automatically builds and publishes evergreen entertainment guides.

Each guide runs independently but shares common infrastructure where appropriate.

Current Guides

- Movies
- TV
- Streaming
- Concerts

---

# Design Philosophy

Each guide should be capable of running independently.

A failure in one guide must never prevent another guide from updating.

Shared components should be reused whenever practical.

Guide-specific behavior should remain inside the guide itself.

---

# Guide Workflow

Guide Runner

↓

Data Collection

↓

AI Content Generation

↓

Guide Enrichment

↓

HTML Builder

↓

WordPress Publisher

↓

Live Guide

---

# Movies Guide

Purpose

Display upcoming theatrical releases.

Primary Data Source

TMDb

Workflow

weekly_movies.py

↓

movie_data.py

↓

AI Writer

↓

guide_enricher.py

↓

html_builder.py

↓

publisher.py

↓

WordPress

Current Status

- Working
- TMDb integration complete
- Trailer links complete

Known Issue

Mobile poster sizing.

---

# TV Guide

Purpose

Display upcoming television and streaming premieres.

Primary Data Source

TMDb

Workflow

weekly_tv.py

↓

tv_data.py

↓

AI Writer

↓

guide_enricher.py

↓

html_builder.py

↓

publisher.py

↓

WordPress

Status

Working

Future

Use the final Movies layout.

---

# Streaming Guide

Purpose

Display upcoming streaming releases.

Primary Data Source

TMDb

Workflow

weekly_streaming.py

↓

streaming_data.py

↓

AI Writer

↓

guide_enricher.py

↓

html_builder.py

↓

publisher.py

↓

WordPress

Status

Working

Future

Use the final Movies layout.

---

# Concert Guide

Purpose

Display upcoming concert tours.

Primary Data Source

Ticketmaster

Workflow

weekly_concerts.py

↓

concert_data.py

↓

AI Writer

↓

guide_enricher.py

↓

html_builder.py

↓

publisher.py

↓

WordPress

Status

Working

Known Issue

Landscape Ticketmaster images currently display much smaller than intended.

Future

Restore previous image sizing.

---

# Shared Components

guide_enricher.py

Responsible for

- Trailer buttons
- Ticket buttons
- Posters
- Card layout
- Metadata

---

html_builder.py

Responsible for

- Final HTML
- CSS injection
- Layout assembly

---

guide_css.py

Responsible for

- Shared guide styling
- Responsive layouts
- Buttons
- Cards
- Typography

---

trailer_finder.py

Shared movie trailer logic.

---

tv_trailer_finder.py

TV-specific trailer lookup.

---

# Guide Rules

Movies, TV and Streaming use portrait posters.

Concerts use landscape images.

Do not force all guides into the same layout.

Each guide may have guide-specific CSS when necessary.

---

# Publishing

Each guide publishes independently.

Failure of one guide must not stop the remaining guides.

---

# Debugging Order

1. Data collection
2. AI output
3. guide_enricher.py
4. HTML Builder
5. Generated HTML
6. Generated CSS
7. WordPress page
8. Browser rendering

Always determine where the problem first appears before modifying code.

---

# Development Rules

Modify one guide at a time.

Never redesign multiple guides simultaneously.

Finish Movies before applying layout changes elsewhere.

Keep shared components stable whenever possible.

---

End of Document