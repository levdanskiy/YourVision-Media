#!/usr/bin/env python3
"""Validate a single day's Almanac content."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence, Tuple

CONTENT_DIR = Path("/home/levdanskiy/.gemini/02_Almanac/Table/02_CONTENT")
REQUIRED_PREFIXES = ("AC-", "NB-", "SW-", "AL-", "SV-")

# Rubrics that legitimately have no factcheck
NO_FACTCHECK_RUBRICS = {"SERVICE", "DIRECTION-PULSE", "WORKFLOW", "LISTS"}


def list_posts(day: str) -> list[Path]:
    try:
        y, m, d = day.split("-")
    except ValueError:
        raise ValueError("day must be YYYY-MM-DD")
    p = CONTENT_DIR / y / m.zfill(2) / d.zfill(2)
    if not p.exists():
        return []
    return sorted(p.glob("*.md"))


def parse_front_matter(path: Path) -> dict[str, list[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm = m.group(1)
    issues: list[str] = []
    has_status = bool(re.search(r"^status:\s*", fm, re.M))
    has_rubric = bool(re.search(r"^rubric:\s*", fm, re.M))
    has_publish = bool(re.search(r"^(date|time):\s*", fm, re.M))
    # visual_status is optional
    if not has_status:
        issues.append("missing frontmatter status")
    if not has_rubric:
        issues.append("missing frontmatter rubric")
    if not has_publish:
        issues.append("missing frontmatter date/time")
    return {"issues": issues, "ok": not issues}


def get_fm_field(text: str, field: str) -> str:
    """Extract field value from front matter."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return ""
    fm = m.group(1)
    pat = re.compile(rf"^{re.escape(field)}:\s*\"?([^\n\"]+)\"?\s*$", re.M)
    mm = pat.search(fm)
    return mm.group(1).strip() if mm else ""


def check_post(path: Path) -> Tuple[str, list[str]]:
    name = path.name
    stem = path.stem
    issues: list[str] = []

    if not any(name.startswith(p) for p in REQUIRED_PREFIXES):
        issues.append(f"wrong prefix: {name}")

    # Front matter checks
    fm = parse_front_matter(path)
    if fm:
        issues.extend(fm.get("issues", []))
        if issues:
            return stem, issues
    else:
        return stem, ["missing front matter"]

    # Content checks
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return stem, ["cannot read file"]

    rubric = get_fm_field(text, "rubric")
    rubrics = {r.strip() for r in rubric.split(",")}
    needs_factcheck = not rubrics & NO_FACTCHECK_RUBRICS

    if needs_factcheck:
        has_factcheck = bool(get_fm_field(text, "factcheck_notes"))
        if not has_factcheck:
            issues.append("missing factcheck_notes")

    return stem, issues


def coverage(day: str) -> Tuple[dict, list[dict]]:
    posts = list_posts(day)
    stats: dict = {"total": len(posts), "ok": 0, "blockers": 0, "by_prefix": {}}
    results: list[dict] = []

    for path in posts:
        post_id, issues = check_post(path)
        is_ok = not issues
        results.append({"path": str(path.relative_to(CONTENT_DIR)), "post_id": post_id, "ok": is_ok, "issues": issues})
        if is_ok:
            stats["ok"] += 1
        else:
            stats["blockers"] += 1
        for pfx in REQUIRED_PREFIXES:
            if path.name.startswith(pfx):
                stats["by_prefix"][pfx] = stats["by_prefix"].get(pfx, 0) + 1
                break

    return stats, results


def print_report(day: str, stats: dict, results: list[dict]) -> int:
    print(f"\n=== {day} | TOTAL {stats['total']} | OK {stats['ok']} | BLOCKERS {stats['blockers']} ===")
    print("-" * 64)

    if stats["blockers"] == 0:
        print("ALL POSTS OK")
        return 0

    print("BLOCKERS:")
    for r in results:
        if not r["ok"]:
            print(f"- {r['post_id']}: {', '.join(r['issues'])}")
    print("FIX THE ABOVE.")
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv or len(argv) != 1:
        print("usage: validate_day.py YYYY-MM-DD")
        return 1

    day = argv[0]
    stats, results = coverage(day)
    return print_report(day, stats, results)


if __name__ == "__main__":
    sys.exit(main())
