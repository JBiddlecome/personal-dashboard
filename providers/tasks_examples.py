# providers/tasks_examples.py
# Examples for task sources integration (Google Tasks, Microsoft To Do, CSV files)
# This file provides sample implementations and examples for different task management systems
Three simple ways to source “tasks due today” while learning:
1) CSV file in your repo (beginner friendly)
2) Google Tasks via Google API
3) Microsoft To Do via Graph API


Each function should return a list[str] of task names due today.
"""
from datetime import date
from typing import List


# 1) CSV example – keep a tasks.csv in the repo and parse it
# Format: task, due_date (YYYY-MM-DD), done (true/false)
import csv


def tasks_from_csv(path: str = "tasks.csv") -> List[str]:
try:
out = []
today = date.today().isoformat()
with open(path, newline="", encoding="utf-8") as f:
reader = csv.DictReader(f)
for row in reader:
if (row.get("due_date") == today) and (row.get("done", "false").lower() != "true"):
out.append(row.get("task", "").strip())
return out
except FileNotFoundError:
return []


# 2) Google Tasks – outline only
# def tasks_from_google() -> List[str]:
# # Use tasks.tasks.list(tasklist='@default', due <= today, not completed)
# return []


# 3) Microsoft To Do – outline only
# def tasks_from_ms_todo() -> List[str]:
# # Use Graph endpoint /me/todo/lists and /tasks filtered by dueDateTime
# return []
