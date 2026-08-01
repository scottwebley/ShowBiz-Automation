# File Reference

Version 1.0

---

# Purpose

This document explains every important file in the ShowBiz Automation project.

When modifying code, identify the correct file before making changes.

Only modify files that are responsible for the current task.

---

# Root Directory

## showbiz_daily.py

Purpose

Main automation entry point.

Responsibilities

- Collect news
- Select stories
- Publish Top Story
- Update homepage
- Execute daily automation

Status

Production

---

## config.py

Purpose

Global configuration.

Contains

- WordPress settings
- API keys
- Site configuration
- Publishing options

Status

Production

---

# Engine Folder

---

## engine/ai_writer.py

Purpose

Generate original ShowBiz articles.

Status

Production

---

## engine/publisher.py

Purpose

Publish posts and pages to WordPress.

Status

Production

Do Not Modify

Unless specifically working on publishing.

---

## engine/entity_extractor.py

Purpose

Determine the primary subject of stories.

Examples

Movies

Artists

Actors

TV Shows

Companies

Status

Production

---

## engine/image_search.py

Purpose

Locate candidate images.

Status

Production

---

## engine/image_verifier.py

Purpose

Reject poor image choices.

Status

Production

---

# Guides

---

## engine/guides/weekly_movies.py

Purpose

Generate Movies Guide.

Status

Production

---

## engine/guides/movie_data.py

Purpose

Retrieve TMDb movie data.

Status

Production

---

## engine/guides/weekly_tv.py

Purpose

Generate TV Guide.

Status

Production

---

## engine/guides/tv_data.py

Purpose

Retrieve television data.

Status

Production

---

## engine/guides/weekly_concerts.py

Purpose

Generate Concert Guide.

Status

Production

---

## engine/guides/concert_data.py

Purpose

Retrieve Ticketmaster events.

Status

Production

---

## engine/guides/guide_enricher.py

Purpose

Add

- Posters
- Buttons
- Trailer links
- Ticket links
- Card HTML

Current Status

Active Development

---

## engine/guides/guide_css.py

Purpose

Shared CSS for guides.

Current Status

Active Development

Known Issue

Movies mobile layout.

---

## engine/guides/html_builder.py

Purpose

Generate final HTML.

Status

Production

---

## engine/guides/trailer_finder.py

Purpose

Movie trailer lookup.

Status

Production

---

## engine/guides/tv_trailer_finder.py

Purpose

TV trailer lookup.

Status

Production

---

# Homepage

---

## engine/homepage_ranker.py

Purpose

Rank homepage stories.

Status

Production

---

## update_homepage.py

Purpose

Publish homepage.

Status

Production

---

# Media Library

---

## engine/media_library/cache.py

Purpose

Build searchable cache.

---

## engine/media_library/search.py

Purpose

Find candidate images.

---

## engine/media_library/scorer.py

Purpose

Score image relevance.

---

## engine/media_library/verifier.py

Purpose

Verify selected images.

---

# Scheduler

LaunchAgent

Purpose

Run showbiz_daily.py automatically.

Status

Production

---

# Testing

Always compile before testing.

Example

python3 -m py_compile filename.py

Test only the modified subsystem.

---

# Development Rules

Locate the responsible file first.

Modify one file only.

Test immediately.

Commit stable versions.

---

End of Document