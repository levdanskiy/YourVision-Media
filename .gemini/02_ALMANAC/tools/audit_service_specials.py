#!/usr/bin/env python3
"""Audit optional SV service notes and SP special posts."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_almanac import ROOT, rel, service_metadata  # noqa: E402


CONTENT = ROOT / "02_CONTENT" / "2026"
ACTIVE_FROM = (2026, 7, 7)
VALID_STATUSES = {"READY", "ГОТОВ", "SCHEDULED", "PUBLISHED"}
VALID_SV_TYPES = {
    "POLL",
    "DIRECTION-PULSE",
    "RECAP",
    "SERIES-NAV",
    "SOURCE-NOTE",
    "AUDIO-NOTE",
    "ARCHIVE-NOTE",
    "COLLAB-NOTE",
    "VISUAL-ESSAY",
    "READER-NOTE",
    "ORACLE-NOTE",
    "CALENDAR-RADAR",
}
FORBIDDEN_BAIT = (
    "лайк",
    "поставь",
    "подпиш",
    "репост",
    "поделись",
    "коммент",
    "share",
    "like",
    "subscribe",
    "tag someone",
)
FORBIDDEN_ORACLE = (
    "точно случится",
    "обязательно случится",
    "гарантированно",
    "предначертано",
    "судьба решит",
    "карты требуют",
    "звёзды требуют",
    "звезды требуют",
    "вложите",
    "инвестируйте",
    "лечит",
    "диагноз",
)

SERVICE_NAME = re.compile(
    r"^(?P<prefix>SV|SP)-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rest>.+)\.md$"
)


@dataclass
class Finding:
    severity: str
    path: Path
    message: str


def file_date(match: re.Match[str]) -> tuple[int, int, int]:
    return (2026, int(match.group("month")), int(match.group("day")))


def body_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("//"):
            continue
        if line.startswith("---"):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def extract_type(prefix: str, rest: str) -> str:
    if prefix == "SV":
        for service_type in sorted(VALID_SV_TYPES, key=len, reverse=True):
            if rest == service_type or rest.startswith(f"{service_type}-"):
                return service_type
        return rest.split("-", 1)[0]

    return rest.split("-", 1)[0]


def iter_files(args: list[str]) -> list[Path]:
    if len(args) == 3:
        year, month, day = args
        return sorted((ROOT / "02_CONTENT" / year / month / day).glob("[SS][VP]-*.md"))
    if len(args) == 2:
        year, month = args
        return sorted((ROOT / "02_CONTENT" / year / month).rglob("[SS][VP]-*.md"))
    if len(args) == 0:
        return sorted(CONTENT.rglob("[SS][VP]-*.md"))
    raise SystemExit("Usage: audit_service_specials.py [YYYY MM [DD]]")


def audit_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    match = SERVICE_NAME.match(path.name)
    if not match:
        findings.append(Finding("ERROR", path, "service/special filename does not match SV/SP format"))
        return findings

    prefix = match.group("prefix")
    service_type = extract_type(prefix, match.group("rest"))
    hour = match.group("hour")
    minute = match.group("minute")
    date_tuple = file_date(match)
    text = path.read_text(encoding="utf-8")
    metadata = service_metadata(text)
    body = body_text(text)
    expected_id = path.stem

    if date_tuple < ACTIVE_FROM:
        findings.append(Finding("ERROR", path, "SV/SP layer is active only from 2026-07-07"))

    if metadata.get("id") != expected_id:
        findings.append(Finding("ERROR", path, f"id metadata must match filename ({expected_id})"))

    if metadata.get("status") not in VALID_STATUSES:
        findings.append(Finding("ERROR", path, "status must be READY/ГОТОВ/SCHEDULED/PUBLISHED"))

    protocols = metadata.get("протоколы", "") or metadata.get("protocols", "")
    if "SERVICE" not in protocols and "SPECIAL" not in protocols:
        findings.append(Finding("WARN", path, "protocol metadata should include SERVICE or SPECIAL"))

    length = len(body)
    if prefix == "SV":
        if service_type not in VALID_SV_TYPES:
            findings.append(Finding("ERROR", path, f"unknown SV type {service_type}"))
        if not 400 <= length <= 900:
            findings.append(Finding("WARN", path, f"SV body length {length} outside 400-900"))
    else:
        if hour != "21" or minute != "04":
            findings.append(Finding("ERROR", path, "SP special posts must use 21:04"))
        if not 900 <= length <= 1600:
            findings.append(Finding("WARN", path, f"SP body length {length} outside 900-1600"))

    lower_text = text.lower()
    for phrase in FORBIDDEN_BAIT:
        if phrase in lower_text:
            findings.append(Finding("ERROR", path, f"engagement bait phrase detected: {phrase}"))

    if prefix == "SV" and service_type == "ORACLE-NOTE":
        for phrase in FORBIDDEN_ORACLE:
            if phrase in lower_text:
                findings.append(Finding("ERROR", path, f"unsafe oracle phrase detected: {phrase}"))

    return findings


def audit_cadence(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    sv_by_week: dict[tuple[int, int], list[Path]] = defaultdict(list)
    sv_by_day: dict[tuple[int, int, int], list[Path]] = defaultdict(list)
    sp_by_month: dict[int, list[Path]] = defaultdict(list)
    direction_by_month: dict[int, list[Path]] = defaultdict(list)

    for path in files:
        match = SERVICE_NAME.match(path.name)
        if not match:
            continue
        year, month, day = file_date(match)
        prefix = match.group("prefix")
        service_type = extract_type(prefix, match.group("rest"))
        if prefix == "SV":
            week = __import__("datetime").date(year, month, day).isocalendar().week
            sv_by_week[(month, week)].append(path)
            sv_by_day[(year, month, day)].append(path)
            if service_type == "DIRECTION-PULSE":
                direction_by_month[month].append(path)
        elif prefix == "SP":
            sp_by_month[month].append(path)

    for paths in sv_by_week.values():
        if len(paths) > 2:
            for path in paths:
                findings.append(Finding("ERROR", path, "more than 2 SV service notes in this week"))

    for paths in sv_by_day.values():
        if len(paths) > 1:
            for path in paths:
                findings.append(Finding("WARN", path, "more than 1 SV service note on this day"))

    for paths in sp_by_month.values():
        if len(paths) > 4:
            for path in paths:
                findings.append(Finding("ERROR", path, "more than 4 SP special posts in this month"))

    for paths in direction_by_month.values():
        if len(paths) > 1:
            for path in paths:
                findings.append(Finding("ERROR", path, "more than 1 direction pulse in this month"))

    return findings


def main() -> int:
    files = iter_files(sys.argv[1:])
    findings: list[Finding] = []
    for path in files:
        findings.extend(audit_file(path))
    findings.extend(audit_cadence(files))

    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARN"]

    print("# Almanac Service/Special Audit")
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
