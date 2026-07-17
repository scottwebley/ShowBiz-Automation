# ============================================
# SHOWBIZ AUTOMATION SCHEDULER
# ============================================

import json
from pathlib import Path
from datetime import datetime

STATE_FILE = Path("data/automation_state.json")


def _load_state():
    STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not STATE_FILE.exists():
        return {}

    try:
        with open(
            STATE_FILE,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state):
    STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            state,
            f,
            indent=4,
        )


def should_run_daily():
    state = _load_state()

    today = datetime.now().strftime("%Y-%m-%d")

    if state.get("last_daily") == today:
        return False

    state["last_daily"] = today
    _save_state(state)

    return True


def should_run_weekly():
    state = _load_state()

    week = datetime.now().strftime("%Y-W%U")

    if state.get("last_weekly") == week:
        return False

    state["last_weekly"] = week
    _save_state(state)

    return True