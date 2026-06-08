#!/usr/bin/env python3
"""Validate current Almanac AL posts without modifying files.

Default scope starts at 2026-05-16, when the current rubric rules took effect.
Use `--all` to include transitional March-April archive files.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "02_CONTENT" / "2026"

RUBRIC_LIMITS = {
    "FRAGMENT": 800,
    "CHRONOS": 2000,
    "OMENS": 2200,
    "DIVINATION": 2600,
    "PERSONAE": 2600,
    "BESTIARY": 2600,
    "OBJECTS": 2500,
    "LISTS": 2500,
    "WORKFLOW": 2500,
    "LORE": 2600,
    "SOURCE": 2600,
    "HERITAGE": 2600,
    "CALENDAR": 2600,
    "WHEEL": 2600,
    "CAKES": 2700,
    "BUNS": 2700,
    "PATISSERIE": 2700,
    "DESSERTS": 2700,
    "SWEETS": 2500,
    "BREAD": 2700,
    "FLATBREAD": 2600,
    "PIES": 2700,
    "FERMENT": 2700,
    "PRESERVE": 2600,
    "SOUP": 2600,
    "CONDIMENTS": 2500,
    "RECIPE": 2700,
    "FOODWAYS": 2600,
    "PANTRY": 2600,
    "DRINKS": 2600,
    "TOOLS": 2500,
    "ETYMON": 2400,
    "PROSE": 2600,
    "CYCLES": 2600,
    "MODERN": 2600,
    "RITES": 2500,
    "FEAST": 2600,
}

ACTIVE_FROM = (2026, 5, 16)
NEW_SLOT_RULES_FROM = (2026, 7, 7)
VALID_STATUSES = {
    "IDEA",
    "DRAFT",
    "ЧЕРНОВИК",
    "NEEDS_FACTCHECK",
    "NEEDS_REWRITE",
    "READY",
    "ГОТОВ",
    "SCHEDULED",
    "PUBLISHED",
    "ARCHIVE",
}
READY_STATUSES = {"READY", "ГОТОВ", "SCHEDULED", "PUBLISHED"}
VALID_IMAGE_STATUSES = {"needed", "generated", "approved", "used", "rejected"}
VALID_GRADES = {"S", "A", "B", "C", "F"}
VALID_CULTURAL_ZONES = {
    "Africa",
    "African Diaspora",
    "Indigenous Americas",
    "Latin America",
    "North America",
    "East Asia",
    "South Asia",
    "Southeast Asia",
    "Central Asia",
    "West Asia",
    "Oceania",
    "Europe",
    "Arctic North",
    "Island Cultures",
    "Global Modern",
    "Cross-Cultural",
}

LEGACY_SLOT_RUBRICS = {
    "10:04": {"LORE", "SOURCE", "OMENS", "DIVINATION", "FRAGMENT", "ETYMON", "PROSE"},
    "15:04": {
        "CAKES",
        "BUNS",
        "PATISSERIE",
        "DESSERTS",
        "SWEETS",
        "RECIPE",
        "BREAD",
        "FLATBREAD",
        "PIES",
        "LISTS",
        "WORKFLOW",
        "PROSE",
    },
    "18:02": {"CHRONOS", "CALENDAR", "HERITAGE", "WHEEL", "CYCLES", "MODERN", "RITES", "ETYMON"},
}

SLOT_RUBRICS = {
    "10:04": {
        "LORE",
        "SOURCE",
        "OMENS",
        "DIVINATION",
        "PERSONAE",
        "BESTIARY",
        "OBJECTS",
        "FRAGMENT",
        "ETYMON",
        "PROSE",
    },
    "15:04": {
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
        "LISTS",
        "WORKFLOW",
        "FOODWAYS",
        "PANTRY",
        "DRINKS",
        "TOOLS",
    },
    "18:02": {"CHRONOS", "CALENDAR", "HERITAGE", "WHEEL", "CYCLES", "MODERN", "RITES", "FEAST", "ETYMON"},
}

AL_NAME = re.compile(
    r"^AL-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rubric>[A-Z]+)-?.*\.md$"
)


@dataclass
class Issue:
    severity: str
    path: Path
    message: str


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"').strip("'")
    return metadata


def service_metadata(text: str) -> dict[str, str]:
    metadata = simple_frontmatter(text)
    for line in text.splitlines()[:40]:
        if not line.startswith("//"):
            continue
        body = line[2:].strip()
        if ":" not in body:
            continue
        key, value = body.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "ид-поста":
            metadata.setdefault("id", value)
        elif key == "дата публикации":
            metadata.setdefault("publication", value)
        elif key == "статус":
            metadata.setdefault("status", value)
        elif key == "factcheck":
            metadata.setdefault("factcheck", value)
        elif key == "alt":
            metadata.setdefault("alt", value)
        elif key in {
            "image_status",
            "grade",
            "rubric",
            "protocols",
            "протоколы",
            "timezone",
            "date",
            "time",
            "cultural_zone",
            "coverage_axis",
            "source_type",
            "secondary_zones",
        }:
            metadata.setdefault(key, value)
    return metadata


def body_text(text: str) -> str:
    lines = text.splitlines()
    start = None
    end = len(lines)
    for i, line in enumerate(lines):
        if start is None and re.match(r"^[^\w\s/`*-].*#", line):
            start = i
        if start is not None and line.startswith("---"):
            end = i
            break
    if start is None:
        return ""
    return "\n".join(lines[start:end]).strip()


def prompt_text(text: str) -> str:
    match = re.search(r"(?im)^\*\*(?:Visual\s+)?Prompt:\*\*\s*(.+)$", text)
    return match.group(1).strip() if match else ""


def file_date(match: re.Match[str]) -> tuple[int, int, int]:
    return (2026, int(match.group("month")), int(match.group("day")))


def slot_rubrics_for(date_tuple: tuple[int, int, int]) -> dict[str, set[str]]:
    return SLOT_RUBRICS if date_tuple >= NEW_SLOT_RULES_FROM else LEGACY_SLOT_RUBRICS


def validate_file(path: Path, include_archive: bool, strict_coverage: bool) -> list[Issue]:
    issues: list[Issue] = []
    name = path.name
    match = AL_NAME.match(name)
    if not match:
        return issues
    if not include_archive and file_date(match) < ACTIVE_FROM:
        return issues

    text = path.read_text(encoding="utf-8")
    metadata = service_metadata(text)
    rubric = match.group("rubric")
    slot = f"{match.group('hour')}:{match.group('minute')}"
    year, month, day = file_date(match)
    expected_id = path.stem
    expected_date = f"{year}-{month:02d}-{day:02d}"

    if metadata.get("id") is None:
        issues.append(Issue("ERROR", path, "missing post id metadata"))
    elif metadata["id"] != expected_id:
        issues.append(Issue("ERROR", path, f"id metadata does not match filename ({expected_id})"))

    if metadata.get("date") is None and metadata.get("publication") is None:
        issues.append(Issue("ERROR", path, "missing publication date metadata"))
    elif metadata.get("date") and metadata["date"] != expected_date:
        issues.append(Issue("ERROR", path, f"date metadata does not match filename ({expected_date})"))

    if metadata.get("status") is None:
        issues.append(Issue("WARN", path, "missing status metadata"))
    elif metadata["status"] not in VALID_STATUSES:
        issues.append(Issue("WARN", path, f"unknown status {metadata['status']}"))

    if metadata.get("time") and metadata["time"] != slot:
        issues.append(Issue("ERROR", path, f"time metadata does not match filename ({slot})"))
    if metadata.get("rubric") and metadata["rubric"].lstrip("#") != rubric:
        issues.append(Issue("ERROR", path, f"rubric metadata does not match filename ({rubric})"))

    try:
        month_dir = int(path.parent.parent.name)
        day_dir = int(path.parent.name)
        year_dir = int(path.parent.parent.parent.name)
        if (year_dir, month_dir, day_dir) != (year, month, day):
            issues.append(Issue("ERROR", path, "directory date does not match filename"))
    except ValueError:
        issues.append(Issue("WARN", path, "could not verify directory date"))

    if "—" in text or "–" in text:
        issues.append(Issue("ERROR", path, "contains forbidden dash character"))
    if re.search(r"--(ar|v|style|s)\b", text):
        issues.append(Issue("ERROR", path, "contains forbidden visual prompt flag"))

    allowed = slot_rubrics_for((year, month, day)).get(slot)
    if allowed and rubric not in allowed:
        issues.append(Issue("WARN", path, f"rubric {rubric} does not match slot {slot}"))

    image_status = metadata.get("image_status")
    if image_status and image_status not in VALID_IMAGE_STATUSES:
        issues.append(Issue("WARN", path, f"unknown image_status {image_status}"))
    if image_status in {"approved", "used"} and not metadata.get("alt"):
        issues.append(Issue("WARN", path, "approved/used image is missing ALT metadata"))

    grade = metadata.get("grade")
    if grade and grade not in VALID_GRADES:
        issues.append(Issue("WARN", path, f"unknown grade {grade}"))

    prompt = prompt_text(text)
    if not prompt:
        issues.append(Issue("WARN", path, "missing Prompt block"))
    elif not prompt.endswith("shot on 35mm film Kodak Portra 800"):
        issues.append(Issue("WARN", path, "Prompt does not end with required film phrase"))

    body = body_text(text)
    if not body:
        issues.append(Issue("WARN", path, "could not detect post body for length check"))
    else:
        limit = RUBRIC_LIMITS.get(rubric)
        if limit and len(body) > limit:
            issues.append(Issue("WARN", path, f"body length {len(body)} exceeds {rubric} limit {limit}"))

    if metadata.get("status") in READY_STATUSES and not prompt:
        issues.append(Issue("ERROR", path, "ready post has no visual prompt"))

    if strict_coverage and metadata.get("status") in READY_STATUSES:
        zone = metadata.get("cultural_zone")
        if not zone:
            issues.append(Issue("WARN", path, "ready post missing cultural_zone metadata"))
        elif zone not in VALID_CULTURAL_ZONES:
            issues.append(Issue("WARN", path, f"unknown cultural_zone {zone}"))
        if not metadata.get("coverage_axis"):
            issues.append(Issue("WARN", path, "ready post missing coverage_axis metadata"))
        if not metadata.get("source_type"):
            issues.append(Issue("WARN", path, "ready post missing source_type metadata"))

    return issues


def main() -> int:
    include_archive = "--all" in sys.argv[1:]
    strict_coverage = "--strict-coverage" in sys.argv[1:]
    issues: list[Issue] = []
    checked = 0
    for path in sorted(CONTENT.rglob("AL-*.md")):
        file_issues = validate_file(path, include_archive, strict_coverage)
        if include_archive or file_issues or (AL_NAME.match(path.name) and file_date(AL_NAME.match(path.name)) >= ACTIVE_FROM):
            checked += 1
        issues.extend(file_issues)

    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARN"]

    print(f"# Almanac validation")
    print()
    print(f"- Scope: {'all AL archive files' if include_archive else 'active AL files from 2026-05-16'}")
    print(f"- Strict coverage metadata: {'yes' if strict_coverage else 'no'}")
    print(f"- Files checked: {checked}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if issues:
        print()
        for issue in issues:
            print(f"{issue.severity}: {rel(issue.path)} - {issue.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
