#!/usr/bin/env python3
"""Build CONTENT_INDEX.csv for 02_ALMANAC from 02_CONTENT tree."""

from __future__ import annotations

import csv
from pathlib import Path

CONTENT_DIR = Path("/home/levdanskiy/.gemini/02_Almanac/Table/02_CONTENT")
OUT = Path("/home/levdanskiy/.gemini/02_Almanac/Table/CONTENT_INDEX.csv")

RE_HEADER = {
    "topic": ("// ТЕМА:", 9),
    "status": ("// СТАТУС:", 10),
    "rubric_line": ("// ПРОТОКОЛЫ:", 13),
    "publish_dt": ("// ДАТА ПУБЛИКАЦИИ:", 19),
}


def parse_filename(path: Path) -> dict:
    """Parse ID-DD.MM-HH-MM-SLUG-PARTS.md into components."""
    stem = path.stem
    try:
        file_id, dd_mm, hh, mm, rubric_slug = stem.split("-", 4)
    except ValueError:
        return {}
    try:
        dd, mm = dd_mm.split(".")
    except ValueError:
        return {}
    return {
        "file_id": file_id,
        "date": f"2026-{mm}-{dd}",
        "time": f"{hh}:{mm}",
        "rubric": rubric_slug.split("-")[0] if rubric_slug else "",
    }


def parse_header(path: Path) -> dict:
    data = {"topic": "", "status": "", "rubric": ""}
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return data

    for line in text.splitlines()[:80]:
        for key, (prefix, pos) in RE_HEADER.items():
            if line.startswith(prefix):
                val = line[pos:].strip().lstrip("/").strip()
                if key == "rubric_line":
                    data["rubric"] = val.split(",", 1)[1].strip() if "," in val else val.replace("Almanac", "").replace(",", "").strip()
                else:
                    data[key] = val
                break

    return data


def walk() -> list[dict]:
    rows: list[dict] = []
    files = sorted(CONTENT_DIR.rglob("*.md"))

    for path in files:
        rel = path.relative_to(CONTENT_DIR)
        parts = list(rel.parts)
        if len(parts) < 4:
            continue

        date_from_dir = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        fn = parse_filename(path)
        hdr = parse_header(path)

        row = {
            "post_id": path.stem,
            "path": str(rel),
            "date": hdr.get("date") or fn.get("date") or date_from_dir,
            "time": hdr.get("time") or fn.get("time", ""),
            "rubric": hdr.get("rubric") or fn.get("rubric", ""),
            "status": hdr.get("status", ""),
            "topic": hdr.get("topic", ""),
            "title": "",
            "tier": "",
            "timezone": "Europe/Riga",
            "cultural_zone": "",
            "factcheck_confidence": "",
            "visual_status": "",
        }
        rows.append(row)
    return rows


def main() -> None:
    rows = walk()
    fields = [
        "post_id",
        "path",
        "date",
        "time",
        "rubric",
        "status",
        "topic",
        "title",
        "tier",
        "timezone",
        "cultural_zone",
        "factcheck_confidence",
        "visual_status",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"Wrote {len(rows)} posts to {OUT}")


if __name__ == "__main__":
    main()
