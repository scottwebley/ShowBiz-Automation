# ShowBiz Automation Troubleshooting

Version 1.0

---

# Purpose

This document lists common problems, their causes, and the recommended troubleshooting steps.

Always diagnose the problem before modifying code.

---

# General Troubleshooting Process

1. Read the complete error message.
2. Verify which file is responsible.
3. Compile the modified file.
4. Test only that subsystem.
5. Verify generated output.
6. Verify WordPress output.
7. Commit working changes.

Never change multiple systems while debugging.

---

# Python Compile Errors

Command

python3 -m py_compile filename.py

If compilation fails:

- Read the exact line number.
- Fix only that error.
- Compile again.

---

# WordPress Publishing Problems

Symptoms

Posts do not publish.

Checklist

- Verify WordPress credentials.
- Verify REST API.
- Verify Application Password.
- Verify publisher.py.
- Verify internet connection.

---

# Homepage Not Updating

Checklist

- Verify homepage updater.
- Verify homepage ranker.
- Verify page IDs.
- Verify REST API.

---

# Scheduler Problems

Symptoms

Automation never starts.

Checklist

- Verify LaunchAgent.
- Verify plist.
- Verify Python path.
- Verify permissions.
- Check scheduler logs.

Useful Commands

launchctl list

launchctl print gui/$(id -u)

tail -100 showbiz_scheduler.log

---

# AI Writer Problems

Symptoms

Articles not generated.

Checklist

- Verify API key.
- Verify OpenAI quota.
- Verify prompts.
- Check logs.

---

# Guide Problems

Always test guides individually.

Movies

python3 -m engine.guides.weekly_movies

TV

python3 -m engine.guides.weekly_tv

Concerts

python3 -m engine.guides.weekly_concerts

Streaming

(run appropriate module)

---

# Guide Layout Problems

Debug order

1. Generated HTML
2. Generated CSS
3. Browser HTML
4. Browser CSS
5. WordPress rendering

Never assume CSS is reaching the browser.

---

# Image Problems

Movie, TV, Streaming

TMDb posters

Concerts

Ticketmaster images

WordPress

Media Library

Fallback

AI generated images

---

# Media Library Problems

Checklist

- Verify cache.
- Verify search index.
- Verify scorer.
- Verify image verifier.

---

# REST API Problems

Test

test_rest_api.py

Common Causes

- Incorrect password
- Incorrect URL
- Security plugin
- Cloudflare
- Server permissions

---

# Git Problems

Before changing production code

git status

Commit often.

Commit before major changes.

Never continue debugging with uncommitted production changes.

---

# Debugging Rules

Never guess.

Always inspect output.

One change at a time.

One subsystem at a time.

One file at a time.

Test immediately.

Commit stable checkpoints.

---

# Emergency Recovery

If something breaks

1. Stop making changes.
2. Restore last working commit.
3. Verify production.
4. Restart debugging from the last known good state.

Never continue adding fixes to a broken system.

---

End of Document