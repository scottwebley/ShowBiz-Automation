# ShowBiz Image System

Version 1.0

---

# Purpose

The Image System selects the best possible image for every piece of published content.

The goal is to maximize relevance while using legal, high-quality sources.

The system always prefers existing licensed images before generating new ones.

---

# Image Philosophy

Correct images are more important than beautiful images.

Never use unrelated images simply because they score well.

Prefer official artwork whenever available.

Avoid duplicate images whenever practical.

---

# Image Priority

The image system searches in this order:

1. WordPress Media Library
2. Approved External Sources
3. AI Generated Image

The search stops when an acceptable image is found.

---

# Media Library

Purpose

Reuse previously licensed or uploaded images.

Workflow

Search

↓

Score

↓

Verify

↓

Select

↓

Return

Primary Components

- media_library/search.py
- media_library/scorer.py
- media_library/cache.py

---

# External Images

Purpose

Retrieve official artwork when appropriate.

Examples

TMDb

Ticketmaster

Other approved providers

Rules

Only approved sources.

No random internet image searches.

---

# AI Generated Images

Purpose

Fallback only.

Used when no acceptable real image exists.

Examples

Entertainment concepts

Generic editorial artwork

Historical topics without artwork

Never replace official movie posters or concert artwork with AI images.

---

# Movie Posters

Source

TMDb

Characteristics

Portrait orientation

Official poster artwork

Guide Usage

Movies

TV

Streaming

Preferred Layout

Vertical card

---

# Concert Images

Source

Ticketmaster

Characteristics

Landscape orientation

Promotional artwork

Guide Usage

Concert Guide only

Preferred Layout

Wide banner

Do not reuse the movie poster layout.

---

# Story Images

Purpose

Support daily news articles.

Priority

Media Library

↓

Official provider

↓

AI fallback

---

# Image Verification

Purpose

Reject poor image selections.

Checks

- Resolution
- Relevance
- Quality
- Aspect ratio
- Subject accuracy

---

# Entity Extraction

Purpose

Determine what image should be searched.

Examples

Movie titles

Artists

Television shows

Celebrities

Studios

Streaming services

Important Rule

Search for the primary entity.

Never search generic headline words.

Example

Wrong

"ALERT"

"NEW"

"MUSIC"

Correct

"Destiny's Child"

This greatly improves image quality.

---

# Duplicate Prevention

Goals

Avoid using identical images repeatedly.

Prefer variety when several acceptable images exist.

---

# Media Library Cache

Purpose

Speed up searches.

When to rebuild

After adding large numbers of images.

After cache corruption.

After search algorithm changes.

---

# Debugging Order

1. Entity extraction
2. Search query
3. Media Library search
4. Image scoring
5. Image verification
6. External providers
7. AI fallback

Never skip directly to AI image generation.

---

# Development Rules

Never lower image quality standards.

Never bypass verification.

Never replace official artwork with AI.

Improve search before adding new providers.

Always preserve legal image usage.

---

# Future Improvements

Better duplicate detection.

Improved entity recognition.

Additional approved image providers.

Smarter relevance scoring.

Automatic quality ranking.

---

End of Document