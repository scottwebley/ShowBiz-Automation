# ShowBiz Image Engine 2.1

## Purpose

The Image Engine is responsible for selecting high-quality editorial images for ShowBiz articles.

It is completely independent from the production newsroom.

Nothing inside this folder should publish to WordPress until it has been fully tested.

---

# Architecture

```
Story
    │
    ▼
AI Editor
    │
    ▼
Finder
    │
    ▼
Provider Manager
    │
    ▼
Providers
    │
    ▼
Scorer
    │
    ▼
Downloader
    │
    ▼
Optimizer
    │
    ▼
Newsroom
```

---

# Modules

## ai_editor.py

Uses GPT to determine:

- subject
- subject type
- story type
- preferred photo
- preferred source

It never downloads images.

---

## finder.py

Converts the AI Editor's decision into search requests.

Example:

Subject:

Taylor Swift

↓

Official Press

↓

Taylor Swift performance publicity photo

---

## provider_manager.py

Coordinates every image provider.

Providers return ImageResult objects.

The manager combines them into one list.

---

## providers/

Each provider implements:

search(query)

Examples:

- Wikimedia
- Official Press
- Pexels
- Getty (future)
- ShowBiz Library (future)

---

## scorer.py

Ranks candidate images.

Future scoring factors:

- Resolution
- Editorial relevance
- Orientation
- License
- Face detection
- AI quality score

---

## downloader.py

Downloads only the highest-ranked image.

It never chooses images.

---

## optimizer.py (future)

Will resize images for:

- Homepage
- Story page
- Social media
- Mobile

---

# Development Rules

Production code is never edited here.

Every module must be testable by itself.

Every provider returns ImageResult objects.

Every module has exactly one responsibility.

---

# Current Status

✅ AI Editor

✅ Finder

✅ Provider Manager

✅ Provider Interface

✅ Scorer

✅ Downloader

🚧 Real Image Provider

🚧 Optimizer

🚧 WordPress Integration

---

# Long-Term Goal

Automatically choose a professional editorial-quality image for every published ShowBiz story using AI-assisted editorial decisions and trusted image providers.

The Image Engine should be completely modular so new providers can be added without changing the rest of the system.