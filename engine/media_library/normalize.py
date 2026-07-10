"""
===========================================
ShowBiz Media Normalization
Version 1.0
===========================================

Purpose:
    Shared text normalization helpers for
    Media Library searching.

Author:
    ShowBiz Automation
"""

import re


def safe(value):
    """
    Safely convert WordPress values to text.
    """

    if value is None:
        return ""

    if isinstance(value, dict):
        return str(value.get("rendered", ""))

    return str(value)


def normalize(text):
    """
    Normalize text for searching.
    """

    text = safe(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())