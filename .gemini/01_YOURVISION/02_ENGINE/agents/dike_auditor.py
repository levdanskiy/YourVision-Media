#!/usr/bin/env python3
"""DIKE — Quality Auditor. Checks recent posts for brand compliance and fact-check status."""
import os
import json
import datetime
import glob

POSTS_ROOT = "/home/levdanskiy/.gemini/01_YOURVISION/04_CONTENT"
AUDIT_LOG = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/audit_log.json"

REQUIRED_SECTIONS = ["#VERDICT", "📍", "🎙"]
FORBIDDEN_PATTERNS = ["наверное", "скорее всего", "возможно", "кажется"]

def audit_recent_posts(days_back: int = 2) -> str:
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days_back)
    violations = []
    audited = 0

    pattern = os.path.join(POSTS_ROOT, "**", "*.md")
    for filepath in glob.glob(pattern, recursive=True):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        if mtime < cutoff:
            continue

        audited += 1
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        missing = [s for s in REQUIRED_SECTIONS if s not in content]
        found_forbidden = [w for w in FORBIDDEN_PATTERNS if w.lower() in content.lower()]

        if missing or found_forbidden:
            violations.append({
                "file": os.path.relpath(filepath, "/home/levdanskiy/.gemini"),
                "missing_sections": missing,
                "weak_language": found_forbidden
            })

    audit = {
        "audited_at": now.isoformat(),
        "posts_checked": audited,
        "violations": violations,
        "status": "FAIL" if violations else "CLEAN"
    }

    with open(AUDIT_LOG, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=4, ensure_ascii=False)

    if violations:
        return f"⚖️ DIKE: {len(violations)}/{audited} post(s) have violations — see audit_log.json"
    return f"⚖️ DIKE: All {audited} recent post(s) passed quality audit."

if __name__ == "__main__":
    print(audit_recent_posts())
