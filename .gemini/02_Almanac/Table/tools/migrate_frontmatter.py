#!/usr/bin/env python3
"""Migrate 02_ALMANAC posts to YAML front matter.
Idempotent: skips files that already have front matter.

Now tests clean on one file before scale.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

CONTENT_DIR = Path("/home/levdanskiy/.gemini/02_Almanac/Table/02_CONTENT")

RE_HEADERS = {
    "post_id": re.compile(r"^//\s*ИД-ПОСТА:\s*(.+)$", re.IGNORECASE),
    "title": re.compile(r"^//\s*ТЕМА:\s*(.+)$", re.IGNORECASE),
    "status": re.compile(r"^//\s*СТАТУС:\s*(.+)$", re.IGNORECASE),
    "publish_dt": re.compile(r"^//\s*ДАТА ПУБЛИКАЦИИ:\s*(.+)$", re.IGNORECASE),
    "rubric_line": re.compile(r"^//\s*ПРОТОКОЛЫ:\s*(.+)$", re.IGNORECASE),
    "cultural_zone": re.compile(r"^//\s*cultural_zone:\s*(.+)$", re.IGNORECASE),
    "secondary_zones": re.compile(r"^//\s*secondary_zones:\s*(.+)$", re.IGNORECASE),
    "coverage_axis": re.compile(r"^//\s*coverage_axis:\s*(.+)$", re.IGNORECASE),
    "source_type": re.compile(r"^//\s*source_type:\s*(.+)$", re.IGNORECASE),
    "factcheck": re.compile(r"^//\s*FACTCHECK:\s*(.+)$", re.IGNORECASE),
    "v4": re.compile(r"^//\s*V4-приёмы:\s*(.+)$", re.IGNORECASE),
}

RE_FN = re.compile(
    r"^(?P<file_id>[A-Z]{2,3})-(?P<dd>\d{2})\.(?P<mm>\d{2})-(?P<hh>\d{2})-(?P<min>\d{2})-(?P<rubric>[A-Z_]+)-(?P<slug>.+)$"
)


def parse_headers(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return data

    for line in text.splitlines()[:50]:
        for key, pat in RE_HEADERS.items():
            m = pat.match(line)
            if m:
                data[key] = m.group(1).strip()
                break

    return data


def parse_filename(path: Path) -> dict[str, str]:
    stem = path.stem
    m = RE_FN.match(stem)
    if not m:
        return {}
    g = m.group
    return {
        "date": f"2026-{g('mm')}-{g('dd')}",
        "time": f"{g('hh')}:{g('min')}",
        "rubric": g("rubric"),
        "slug": g("slug"),
    }


def derive_front_matter(path: Path, hdr: dict[str, str], fn: dict[str, str]) -> dict[str, Any]:
    protocol_rubric = hdr.get("rubric_line", "").split(",", 1)[1].strip() if "," in hdr.get("rubric_line", "") else ""
    protocol_rubric = re.sub(r"\s*\(.+?\)\s*$", "", protocol_rubric).strip()
    fm: dict[str, Any] = {
        "post_id": hdr.get("post_id") or path.stem,
        "title": hdr.get("title", ""),
        "slug": fn.get("slug", ""),
        "date": hdr.get("publish_dt", "").split(",")[0].strip() if hdr.get("publish_dt") else fn.get("date", ""),
        "time": "",
        "timezone": "Europe/Riga",
        "status": hdr.get("status", "DRAFT"),
        "rubric": fn.get("rubric", "") or protocol_rubric,
        "tier": "",
        "cultural_zone": hdr.get("cultural_zone", ""),
        "secondary_zones": [z.strip() for z in hdr.get("secondary_zones", "").split(",") if z.strip()],
        "coverage_axes": [a.strip() for a in hdr.get("coverage_axis", "").split(",") if a.strip()],
        "source_types": [s.strip() for s in hdr.get("source_type", "").split(",") if s.strip()],
        "factcheck_notes": hdr.get("factcheck", ""),
        "factcheck_confidence": "",
        "v4_techniques": hdr.get("v4", ""),
        "visual_status": "indexed_legacy",
        "sources_used": "indexed_legacy",
        "author": "",
        "notes": "",
    }

    # Parse time
    if hdr.get("publish_dt"):
        dt = hdr["publish_dt"]
        parts = dt.split(",")
        if len(parts) >= 2:
            time_part = parts[1].strip()
            tz_match = re.search(r"\(([^)]+)\)", time_part)
            if tz_match:
                fm["timezone"] = tz_match.group(1)
                fm["time"] = time_part[:tz_match.start()].strip()
            else:
                fm["time"] = time_part
    if not fm["time"] and fn.get("time"):
        fm["time"] = fn["time"]

    # Normalize date to YYYY-MM-DD if needed
    if fm["date"] and not re.match(r"\d{4}-\d{2}-\d{2}", fm["date"]):
        m = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", fm["date"])
        if m:
            fm["date"] = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    if not fm["date"]:
        fm["date"] = fn.get("date", "")

    # Title cleanup
    if fm["title"].startswith("// "):
        fm["title"] = fm["title"][3:].strip()

    return fm


def format_front_matter(fm: dict[str, Any]) -> str:
    lines = ["---"]
    for key in [
        "post_id",
        "title",
        "slug",
        "date",
        "time",
        "timezone",
        "status",
        "rubric",
        "tier",
        "cultural_zone",
        "secondary_zones",
        "coverage_axes",
        "source_types",
        "factcheck_confidence",
        "factcheck_notes",
        "visual_status",
        "sources_used",
        "author",
        "notes",
    ]:
        val = fm.get(key, "")
        if val == "" or val is None:
            continue
        if isinstance(val, list):
            val_str = ", ".join(str(v) for v in val)
        else:
            val_str = str(val)
        lines.append(f'{key}: "{val_str}"')
    if fm.get("v4_techniques"):
        lines.append(f'v4_techniques: "{fm["v4_techniques"]}"')
    lines.append("---")
    return "\n".join(lines) + "\n"


def has_front_matter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def migrate(path: Path, dry_run: bool = False) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if has_front_matter(text):
        return False

    hdr = parse_headers(path)
    fn = parse_filename(path)
    fm = derive_front_matter(path, hdr, fn)
    fm_block = format_front_matter(fm)

    new_text = fm_block + "\n" + text
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
    files = sorted(CONTENT_DIR.rglob("*.md"))
    print(f"Found {len(files)} posts")

    migrated = 0
    skipped = 0
    errors = 0

    for path in files:
        try:
            changed = migrate(path, dry_run=dry_run)
            if changed:
                migrated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"ERROR: {path}: {e}")
            errors += 1

    mode = "DRY-RUN" if dry_run else "MIGRATED"
    print(f"{mode}: {migrated} | SKIPPED (already frontmatter): {skipped} | ERRORS: {errors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
