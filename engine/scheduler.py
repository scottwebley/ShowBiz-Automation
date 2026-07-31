# ============================================
# SHOWBIZ AUTOMATION SCHEDULER
# ============================================

import json
from pathlib import Path
from datetime import datetime, date

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
    today = date.today().isoformat()
    return state.get("last_daily") != today


def mark_daily_complete():
    state = _load_state()
    state["last_daily"] = date.today().isoformat()
    _save_state(state)


def should_run_weekly():
    state = _load_state()
    this_week = datetime.now().strftime("%Y-%U")
    return state.get("last_weekly") != this_week


def mark_weekly_complete():
    state = _load_state()
    state["last_weekly"] = datetime.now().strftime("%Y-%U")
    _save_state(state)