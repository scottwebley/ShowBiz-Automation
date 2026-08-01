# ShowBiz AI Development Protocol

Version 1.0

This document defines how AI assistants must work on the ShowBiz Automation project.

These rules override convenience.

They exist to protect production stability.

---

# Primary Objective

Preserve a stable production newsroom while continuously improving it.

Never sacrifice reliability for new features.

---

# Before Writing Code

Always determine:

1. What problem is being solved?
2. Which file owns that responsibility?
3. Is the production system currently stable?
4. Can the change be isolated?

Never begin coding before answering these questions.

---

# Development Workflow

1. Identify the responsible file.
2. Explain why that file is the correct one.
3. Replace one complete file or one complete function.
4. Wait for testing.
5. Analyze the results.
6. Continue only after verification.

---

# Never

Never modify multiple unrelated systems.

Never redesign working production code.

Never guess.

Never continue making random changes after two failed attempts.

Never create unnecessary complexity.

Never sacrifice readability.

Never leave partial implementations.

---

# Required Behavior

Prefer investigation over speculation.

Inspect generated output before changing code.

Use evidence.

Explain the reasoning behind recommendations.

Preserve existing functionality whenever possible.

---

# Project Priorities

Production Stability

↓

Correctness

↓

Maintainability

↓

Performance

↓

New Features

---

# Shared Components

Changes to shared components require extra caution.

Examples

Publisher

Guide CSS

Homepage Ranker

Scheduler

Media Library

Shared Trailer Finder

Changing these files may affect multiple systems.

---

# Guide Development

Movies

TV

Streaming

Concerts

Treat each guide as an independent product.

Do not redesign multiple guides simultaneously.

Finish one guide before moving to the next.

---

# Regression Policy

If something previously worked:

Do not redesign it.

Determine why it stopped working.

Restore the previous behavior first.

Improve it later.

---

# Debugging Rules

Observe.

Measure.

Verify.

Then modify.

Do not modify code based only on assumptions.

---

# Communication

Keep explanations concise.

Identify the file first.

Provide complete replacements whenever practical.

Wait for test results.

Avoid unnecessary discussion during debugging.

---

# Documentation

Update PROJECT_STATUS.md after major milestones.

Update CHANGELOG.md after significant changes.

Record important discoveries in LESSONS_LEARNED.md.

---

# Long-Term Goal

Create a fully autonomous entertainment newsroom that remains understandable, maintainable, and stable.

Every code change should move the project toward that goal.

---

End of Document