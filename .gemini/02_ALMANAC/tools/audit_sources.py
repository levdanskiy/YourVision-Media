#!/usr/bin/env python3
"""Audit ready Almanac posts for source-note and claim discipline."""

from __future__ import annotations

import re
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


SOURCE_RUBRICS = {"SOURCE"}
DIVINATION_RUBRICS = {"DIVINATION"}
FOOD_RUBRICS = {
    "CAKES",
    "BUNS",
    "PATISSERIE",
    "DESSERTS",
    "SWEETS",
    "RECIPE",
    "BREAD",
    "FLATBREAD",
    "PIES",
    "FERMENT",
    "PRESERVE",
    "SOUP",
    "CONDIMENTS",
    "FOODWAYS",
    "PANTRY",
    "DRINKS",
    "TOOLS",
    "LISTS",
    "WORKFLOW",
}
CALENDAR_RUBRICS = {"CHRONOS", "CALENDAR", "WHEEL", "CYCLES", "FEAST"}
HERITAGE_RUBRICS = {"HERITAGE", "RITES", "OMENS", "LORE", "PERSONAE", "BESTIARY", "OBJECTS"}

PLACEHOLDER_RE = re.compile(r"(?i)\b(todo|tbd|source needed|источник нужен|уточнить|\[source\])\b")
YEAR_RE = re.compile(r"\b(?:1[0-9]{3}|20[0-9]{2}|~\d{3,4})\b")


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
    raise SystemExit("Usage: audit_sources.py [YYYY MM [DD]]")


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


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
    body = body_text(text)
    factcheck = metadata.get("factcheck", "")
    source_type = metadata.get("source_type", "")
    source_blob = f"{factcheck}\n{source_type}\n{body}"

    if not factcheck:
        findings.append(Finding("ERROR", path, "ready post missing FACTCHECK metadata"))
    elif PLACEHOLDER_RE.search(factcheck):
        findings.append(Finding("ERROR", path, "FACTCHECK contains placeholder language"))

    if rubric in SOURCE_RUBRICS:
        excerpt = "\n".join(body.splitlines()[:10])
        if "«" not in excerpt and '"' not in excerpt:
            findings.append(Finding("WARN", path, "SOURCE post may lack a visible source quotation"))
        if not YEAR_RE.search(source_blob):
            findings.append(Finding("WARN", path, "SOURCE post has no visible source date/year"))

    if rubric in DIVINATION_RUBRICS:
        if not has_any(source_blob, ("deck", "колод", "museum", "catalog", "oracle", "tarot", "zodiac", "i ching")):
            findings.append(Finding("WARN", path, "DIVINATION needs deck/oracle/catalog source context"))
        if has_any(body, ("личный прогноз", "персональный прогноз", "диагноз", "лечит", "исцеляет")):
            findings.append(Finding("ERROR", path, "DIVINATION includes personal prediction or medical language"))

    if rubric in FOOD_RUBRICS:
        if not has_any(source_type, ("food_history", "technique", "primary_source", "institutional_reference")):
            findings.append(Finding("WARN", path, "food post source_type should include food_history or technique"))
        if not has_any(source_blob, ("recipe", "cookbook", "food", "bread", "pastry", "culinary", "baking", "drink", "pantry", "preservation", "ethnography", "museum", "encyclopedia")):
            findings.append(Finding("WARN", path, "food post may lack culinary source context"))

    if rubric in CALENDAR_RUBRICS:
        if not has_any(source_type, ("astronomy", "calendar_data", "science_reference", "primary_source")):
            findings.append(Finding("WARN", path, "calendar post source_type should include astronomy/calendar/science source"))

    if rubric in HERITAGE_RUBRICS:
        if not has_any(source_type, ("field_record", "ethnography", "ethnobotany", "institutional_reference", "primary_source")):
            findings.append(Finding("WARN", path, "heritage/myth post source_type should name field/institutional/source basis"))

    if has_any(body, ("всегда", "никогда", "доказано, что", "единственный источник", "во всех культурах")):
        findings.append(Finding("WARN", path, "absolute claim needs source tightening"))

    return findings


def main() -> int:
    paths = iter_scope(sys.argv[1:])
    findings: list[Finding] = []
    for path in paths:
        findings.extend(audit_file(path))

    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARN"]

    print("# Almanac source audit")
    print()
    print(f"- Files checked: {len(paths)}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if findings:
        print()
        for item in findings:
            print(f"{item.severity}: {rel(item.path)} - {item.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
