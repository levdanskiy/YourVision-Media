#!/usr/bin/env python3
"""HEPHAESTUS — System Builder. Validates Hub integrity and checks asset/data consistency."""
import os
import json
import datetime

HUB_HTML = "/home/levdanskiy/YV_Editor_Hub.html"
DATA_JS = "/home/levdanskiy/data.js"
BUILD_REPORT = "/home/levdanskiy/.gemini/01_YOURVISION/_SHARED/build_report.json"

def run_integrity_check():
    now = datetime.datetime.now()
    issues = []
    checks = {}

    # 1. Hub HTML exists and is non-empty
    if os.path.exists(HUB_HTML):
        size = os.path.getsize(HUB_HTML)
        checks["hub_html"] = f"OK ({size} bytes)"
        if size < 1000:
            issues.append("YV_Editor_Hub.html is suspiciously small")
    else:
        checks["hub_html"] = "MISSING"
        issues.append("YV_Editor_Hub.html not found")

    # 2. data.js exists and is non-empty
    if os.path.exists(DATA_JS):
        size = os.path.getsize(DATA_JS)
        checks["data_js"] = f"OK ({size} bytes)"
        if size < 100:
            issues.append("data.js is suspiciously small")
    else:
        checks["data_js"] = "MISSING"
        issues.append("data.js not found")

    # 3. Content folders exist
    for folder in [
        "/home/levdanskiy/.gemini/01_YOURVISION",
        "/home/levdanskiy/.gemini/02_ALMANAC",
        "/home/levdanskiy/.gemini/03_NOVELLS",
    ]:
        label = os.path.basename(folder)
        checks[label] = "OK" if os.path.isdir(folder) else "MISSING"
        if not os.path.isdir(folder):
            issues.append(f"{label} folder missing")

    report = {
        "built_at": now.isoformat(),
        "status": "FAIL" if issues else "OK",
        "checks": checks,
        "issues": issues
    }

    with open(BUILD_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    if issues:
        return f"🔧 HEPHAESTUS: {len(issues)} issue(s) found — {issues}"
    return "🔧 HEPHAESTUS: All systems nominal. Hub integrity confirmed."

if __name__ == "__main__":
    print(run_integrity_check())
