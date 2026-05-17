#!/usr/bin/env python3
"""HELIOS — Publication Scheduler. Scans content plan and flags posts due for release."""
import os
import json
import datetime

CONTENT_PLAN = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/content_plan.json"
PUBLISH_QUEUE = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/publish_queue.json"

def scan_and_flag():
    now = datetime.datetime.now()

    if not os.path.exists(CONTENT_PLAN):
        return "⚠️ HELIOS: content_plan.json not found — nothing to scan."

    with open(CONTENT_PLAN, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    due = []
    for post in plan.get("posts", []):
        scheduled_str = post.get("scheduled_at")
        status = post.get("status", "draft")
        if not scheduled_str or status != "ready":
            continue
        try:
            scheduled = datetime.datetime.fromisoformat(scheduled_str)
        except ValueError:
            continue
        if scheduled <= now:
            due.append(post)

    queue = {"updated_at": now.isoformat(), "due": due}
    with open(PUBLISH_QUEUE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=4, ensure_ascii=False)

    if due:
        ids = [p.get("id", "?") for p in due]
        return f"☀️ HELIOS: {len(due)} post(s) due — {ids}"
    return "☀️ HELIOS: No posts due. Queue clear."

if __name__ == "__main__":
    print(scan_and_flag())
