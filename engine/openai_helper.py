"""
===========================================
ShowBiz OpenAI Helper
Version 3.0
===========================================

Purpose:
    Provide a single shared OpenAI client for
    the entire ShowBiz project.

Features:
    • Shared OpenAI client
    • Response wrapper
    • Image wrapper
    • One-time quota detection
    • Disable AI after quota exhaustion
    • Centralized logging
"""

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

#
# Shared client
#

client = OpenAI()

#
# Global state
#

AI_DISABLED = False
_ALREADY_REPORTED = False


def ai_available():
    """
    Return True if AI is enabled.
    """

    return not AI_DISABLED


def disable_ai():
    """
    Disable AI for the remainder
    of the current process.
    """

    global AI_DISABLED
    global _ALREADY_REPORTED

    AI_DISABLED = True

    if not _ALREADY_REPORTED:

        print()
        print("========================================")
        print("OPENAI UNAVAILABLE")
        print("========================================")
        print("429 insufficient_quota")
        print()
        print("AI features disabled for this run.")
        print("========================================")
        print()

        _ALREADY_REPORTED = True


def _handle_rate_limit(error):
    """
    Detect insufficient quota.
    """

    try:
        code = error.body.get(
            "error",
            {},
        ).get(
            "code"
        )
    except Exception:
        code = None

    if code == "insufficient_quota":
        disable_ai()

    raise error


def create_response(**kwargs):
    """
    Wrapper around:

        client.responses.create()

    Future enhancements will be added here.
    """

    if AI_DISABLED:
        raise RuntimeError(
            "AI disabled for this run."
        )

    try:

        return client.responses.create(
            **kwargs
        )

    except RateLimitError as e:

        _handle_rate_limit(e)


def generate_image(**kwargs):
    """
    Wrapper around:

        client.images.generate()

    Future enhancements will be added here.
    """

    if AI_DISABLED:
        raise RuntimeError(
            "AI disabled for this run."
        )

    try:

        return client.images.generate(
            **kwargs
        )

    except RateLimitError as e:

        _handle_rate_limit(e)