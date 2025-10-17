# providers/demo.py
# Demo provider implementation that works from environment variables only (no external APIs)
# This provider simulates email, calendar, and task data for demonstration purposes
## providers/demo.py
import os

def get_gmail_unread() -> int:
    return int(os.getenv("DEMO_GMAIL_UNREAD", "0"))


def get_outlook_unread() -> int:
    return int(os.getenv("DEMO_OUTLOOK_UNREAD", "0"))


def get_tasks_due_today() -> list:
    raw = os.getenv("DEMO_TASKS_TODAY", "").strip()
    return [t.strip() for t in raw.split(",") if t.strip()] if raw else []


def get_events_today() -> list:
    """
    Returns a list of dicts like {"time": "09:00", "title": "Standup", "location": "Zoom"}
    Read from DEMO_EVENTS_TODAY env var as:
    "HH:MM - Title @ Location|HH:MM - Title2 @ Location2"
    """
    raw = os.getenv("DEMO_EVENTS_TODAY", "").strip()
    if not raw:
        return []
    events = []
    for chunk in raw.split("|"):
        piece = chunk.strip()
        if not piece:
            continue
        # Parse simple pattern HH:MM - Title @ Location
        time_part, rest = piece.split(" - ", 1) if " - " in piece else ("", piece)
        title_part, location_part = rest.split(" @ ", 1) if " @ " in rest else (rest, "")
        events.append({
            "time": time_part.strip(),
            "title": title_part.strip(),
            "location": location_part.strip(),
        })
    return events
