#!/usr/bin/env python3
"""Audit Almanac post body lengths against rubric target bands."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_almanac import (  # noqa: E402
    AL_NAME,
    CONTENT,
    READY_STATUSES,
    ROOT,
    body_text,
    file_date,
    rel,
    service_metadata,
)


TARGETS = {
    "FRAGMENT": (400, 600, 800),
    "CHRONOS": (1000, 1500, 2000),
    "OMENS": (1300, 1800, 2200),
    "DIVINATION": (1800, 2400, 2600),
    "PERSONAE": (1800, 2300, 2600),
    "BESTIARY": (1800, 2300, 2600),
    "OBJECTS": (1700, 2200, 2500),
    "LISTS": (1500, 2000, 2500),
    "WORKFLOW": (1500, 2100, 2500),
    "LORE": (1800, 2300, 2600),
    "SOURCE": (1800, 2300, 2600),
    "HERITAGE": (1800, 2300, 2600),
    "CALENDAR": (1800, 2300, 2600),
    "WHEEL": (1800, 2300, 2600),
    "CAKES": (2000, 2500, 2700),
    "BUNS": (2000, 2500, 2700),
    "PATISSERIE": (2000, 2500, 2700),
    "DESSERTS": (2000, 2500, 2700),
    "SWEETS": (1800, 2300, 2500),
    "BREAD": (2000, 2500, 2700),
    "FLATBREAD": (1800, 2300, 2600),
    "PIES": (2000, 2500, 2700),
    "FERMENT": (2000, 2500, 2700),
    "PRESERVE": (1800, 2300, 2600),
    "SOUP": (1800, 2300, 2600),
    "CONDIMENTS": (1500, 2100, 2500),
    "RECIPE": (2000, 2500, 2700),
    "FOODWAYS": (1800, 2300, 2600),
    "PANTRY": (1800, 2300, 2600),
    "DRINKS": (1800, 2300, 2600),
    "TOOLS": (1500, 2100, 2500),
    "ETYMON": (1500, 2000, 2400),
    "PROSE": (1800, 2300, 2600),
    "CYCLES": (1800, 2300, 2600),
    "MODERN": (1800, 2300, 2600),
    "RITES": (1500, 2000, 2500),
    "FEAST": (1800, 2300, 2600),
}


@dataclass
class Finding:
    severity: str
    path: Path
    message: str


def iter_scope(args: list[str]) -> list[Path]:
    if len(args) == 3:
        year, month, day = args
        return sorted((ROOT / "02_CONTENT" / year / month / day).glob("AL-*.md"))
    if len(args) == 2:
        year, month = args
        return sorted((ROOT / "02_CONTENT" / year / month).rglob("AL-*.md"))
    if len(args) == 0:
        return [
            path
            for path in sorted(CONTENT.rglob("AL-*.md"))
            if AL_NAME.match(path.name) and file_date(AL_NAME.match(path.name)) >= (2026, 5, 16)
        ]
    raise SystemExit("Usage: audit_lengths.py [YYYY MM [DD]]")


def audit_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    match = AL_NAME.match(path.name)
    if not match:
        return findings

    text = path.read_text(encoding="utf-8")
    metadata = service_metadata(text)
    status = metadata.get("status", "")
    if status not in READY_STATUSES:
        return findings

    rubric = match.group("rubric")
    target = TARGETS.get(rubric)
    body = body_text(text)
    if not target or not body:
        return findings

    low, high, hard = target
    length = len(body)
    if length > hard:
        findings.append(Finding("ERROR", path, f"body length {length} exceeds {rubric} hard limit {hard}"))
    elif length > high:
        findings.append(Finding("WARN", path, f"body length {length} is above {rubric} target {low}-{high}"))
    elif length < low:
        findings.append(Finding("WARN", path, f"body length {length} is below {rubric} target {low}-{high}"))

    return findings


def main() -> int:
    findings: list[Finding] = []
    files = iter_scope(sys.argv[1:])
    for path in files:
        findings.extend(audit_file(path))

    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARN"]

    print("# Almanac Length Audit")
    print()
    print(f"- Files checked: {len(files)}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if findings:
        print()
        for item in findings:
            print(f"{item.severity}: {rel(item.path)} - {item.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
