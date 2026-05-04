#!/usr/bin/env python3
"""HERMES — Cross-Platform Syndicator. Reads publish queue and logs distribution tasks."""
import os
import json
import datetime

PUBLISH_QUEUE = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/publish_queue.json"
SYNDICATION_LOG = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/syndication_log.json"

PLATFORMS = ["instagram", "telegram", "hub"]

def t10_safe(dt: datetime.datetime) -> bool:
    """Returns False if post falls within 10 min before the hour (:50–:00)."""
    return not (50 <= dt.minute <= 59)

def run_syndication():
    now = datetime.datetime.now()

    if not os.path.exists(PUBLISH_QUEUE):
        return "⚠️ HERMES: publish_queue.json not found — run HELIOS first."

    with open(PUBLISH_QUEUE, 'r', encoding='utf-8') as f:
        queue = json.load(f)

    due = queue.get("due", [])
    if not due:
        return "🪽 HERMES: Nothing in queue to syndicate."

    if not t10_safe(now):
        return f"🪽 HERMES: T-10 block active ({now.strftime('%H:%M')}) — syndication deferred."

    log_entries = []
    for post in due:
        entry = {
            "post_id": post.get("id", "unknown"),
            "project": post.get("project", "YV"),
            "syndicated_at": now.isoformat(),
            "platforms": PLATFORMS,
            "status": "logged"
        }
        log_entries.append(entry)

    if os.path.exists(SYNDICATION_LOG):
        with open(SYNDICATION_LOG, 'r', encoding='utf-8') as f:
            log = json.load(f)
    else:
        log = {"entries": []}

    log["entries"].extend(log_entries)
    log["entries"] = log["entries"][-50:]  # keep last 50

    with open(SYNDICATION_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=4, ensure_ascii=False)

    return f"🪽 HERMES: {len(log_entries)} post(s) logged for syndication → {PLATFORMS}"

if __name__ == "__main__":
    print(run_syndication())
