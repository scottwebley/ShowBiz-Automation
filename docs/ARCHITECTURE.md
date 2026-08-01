# ShowBiz Automation Architecture

Version: 1.0

---

# Overview

ShowBiz Automation is a fully automated AI-powered entertainment newsroom.

The system continuously collects entertainment news, evaluates editorial importance, creates original content, selects images, publishes to WordPress, updates guide pages, and maintains the homepage automatically.

The architecture is modular so individual components can be improved without affecting the production pipeline.

---

# System Overview

                    showbiz_daily.py
                            │
                            ▼
                 News Collection Engine
                            │
                            ▼
                  Editorial Processing
                            │
                            ▼
                    Story Selection
                            │
                            ▼
                       AI Writer
                            │
                            ▼
                   Image Selection
                            │
                            ▼
                 WordPress Publisher
                            │
                            ▼
                  Homepage Updates

---

# Primary Components

## News Collection

Purpose

Download entertainment news from multiple sources.

Responsibilities

- Fetch RSS feeds
- Normalize stories
- Remove invalid content
- Prepare stories for editorial scoring

---

## Editorial Engine

Purpose

Determine which stories deserve publication.

Responsibilities

- Editorial filtering
- Duplicate detection
- Story scoring
- Homepage ranking

---

## AI Writer

Purpose

Generate original ShowBiz articles.

Responsibilities

- Create headlines
- Write original articles
- Maintain ShowBiz writing style
- Generate related content

---

## Image System

Purpose

Find the best available image.

Priority

1. WordPress Media Library
2. Approved external sources
3. AI-generated image

Responsibilities

- Image search
- Image scoring
- Image verification
- Image generation fallback

---

## WordPress Publisher

Purpose

Publish content automatically.

Responsibilities

- Publish posts
- Upload images
- Update metadata
- Assign featured images

---

## Homepage System

Purpose

Maintain the ShowBiz homepage.

Responsibilities

- Rank stories
- Replace homepage content
- Maintain featured sections

---

## Guide System

Purpose

Maintain evergreen guide pages.

Current Guides

Movies

TV

Streaming

Concerts

Each guide operates independently.

---

# Guide Architecture

Movies

TMDb

↓

AI enrichment

↓

Trailer links

↓

HTML builder

↓

WordPress page

---

TV

TMDb

↓

AI enrichment

↓

Trailer links

↓

WordPress page

---

Concerts

Ticketmaster

↓

AI enrichment

↓

Ticket links

↓

WordPress page

---

# Scheduler

Purpose

Run automation automatically.

Responsibilities

Daily publishing

Homepage updates

Guide updates

Future scheduled jobs

---

# Folder Structure

engine/

editorial/

guides/

homepage/

media_library/

publisher/

scheduler/

tests/

docs/

---

# Design Philosophy

Every subsystem should be independent.

Production systems should remain stable.

One change at a time.

One file at a time.

Test after every modification.

Keep changes reversible.

Never redesign working systems unnecessarily.

---

# Current Focus

Movies Guide mobile layout.

No changes to production systems until Movies is complete.

After Movies:

TV

Streaming

Concerts

---

End of Document