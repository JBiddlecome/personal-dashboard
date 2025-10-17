# app.py
# Main Flask application file for the personal dashboard
# This file initializes the Flask app and defines routes for the dashboard
import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Provider selection helpers ------------------------------------------------

def load_provider(kind: str):
    """Dynamically import a provider module based on env selection."""
    mapping = {
        "gmail_demo": "providers.demo",
        "outlook_demo": "providers.demo",
        "tasks_demo": "providers.demo",
        "calendar_demo": "providers.demo",
        # Future real integrations (same exported functions signatures):
        # "gmail_googleapi": "providers.gmail_googleapi",
        # "outlook_graph": "providers.outlook_graph",
    }
    module_name = mapping.get(kind, "providers.demo")
    mod = __import__(module_name, fromlist=["*"])
    return mod

email_provider = load_provider(os.getenv("PROVIDER_EMAIL", "gmail_demo"))
outlook_provider = load_provider(os.getenv("PROVIDER_OUTLOOK", "outlook_demo"))
tasks_provider = load_provider(os.getenv("PROVIDER_TASKS", "tasks_demo"))
calendar_provider = load_provider(os.getenv("PROVIDER_CALENDAR", "calendar_demo"))


# --- Routes --------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    # Each provider returns simple Python data (ints/lists/dicts)
    gmail_unread = email_provider.get_gmail_unread()
    outlook_unread = outlook_provider.get_outlook_unread()
    tasks_today = tasks_provider.get_tasks_due_today()
    events_today = calendar_provider.get_events_today()

    return jsonify({
        "gmail": {"unread": gmail_unread},
        "outlook": {"unread": outlook_unread},
        "tasks": {"today_due": tasks_today},
        "calendar": {"today": events_today},
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## providers/__init__.py
```python
# empty on purpose – allows relative imports
```

---

## providers/demo.py
```python
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
