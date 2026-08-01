# Architectural Decisions

Version 1.0

---

# Purpose

This document records important engineering decisions made during development.

Future developers should understand why a decision was made before changing it.

Never remove a design decision simply because it appears unusual.

---

# Decision 001

One File At A Time

Reason

Large changes made debugging extremely difficult.

Decision

Production modifications should be isolated to one file whenever practical.

Status

Permanent.

---

# Decision 002

Complete File Replacements

Reason

Partial snippets frequently caused merge mistakes and indentation errors.

Decision

Provide complete replacement files or complete function replacements whenever possible.

Status

Permanent.

---

# Decision 003

Movies, TV and Streaming Share Architecture

Reason

These guides all use portrait artwork from TMDb.

Sharing layout and enrichment code reduces maintenance.

Status

Permanent.

---

# Decision 004

Concert Guide Uses Independent Layout

Reason

Ticketmaster provides landscape promotional artwork.

Trying to force landscape artwork into portrait layouts reduced quality.

Decision

Concert Guide may diverge from the other guides when necessary.

Status

Permanent.

---

# Decision 005

Publishing Pipeline Is Protected

Reason

Publishing affects every subsystem.

Small experiments previously created unintended production failures.

Decision

Publishing code should only change when the current task specifically requires it.

Status

Permanent.

---

# Decision 006

Media Library First

Reason

Previously uploaded licensed images should always be preferred over AI generation.

Decision

Search order

Media Library

↓

Approved Providers

↓

AI Image

Status

Permanent.

---

# Decision 007

Trailer Links

Reason

Readers benefit from immediate access to official trailers.

Decision

Movies and TV automatically include trailer buttons.

Status

Permanent.

---

# Decision 008

Generated HTML Must Be Verified

Reason

Generated HTML and browser-rendered HTML are not always identical.

Decision

Always inspect generated HTML before changing CSS.

Status

Permanent.

---

# Decision 009

Regression Policy

Reason

Features occasionally stop working while improving unrelated systems.

Decision

Restore previous behavior before redesigning.

Status

Permanent.

---

# Decision 010

Production Stability

Reason

Reliable automation is more valuable than rapid feature growth.

Decision

Protect working systems.

Improve them carefully.

Status

Permanent.

---

# Future Decisions

Every significant architectural choice should be recorded here.

The goal is to preserve the reasoning behind the code.

---

End of Document