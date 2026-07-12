#!/usr/bin/env python3
"""Run strict pre-publication checks for one Almanac day."""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_almanac import (  # noqa: E402
    AL_NAME,
    READY_STATUSES,
    ROOT,
    Issue,
    rel,
    service_metadata,
    validate_file,
)


TIME_CHANGE_FROM = (2026, 7, 17)
LEGACY_REQUIRED_SLOTS = {"10:04", "15:04", "18:02"}
TIME_SHIFTED_REQUIRED_SLOTS = {"09:10", "14:00", "20:40"}


@dataclass
class CheckResult:
    name: str
    errors: int
    warnings: int


def slot_for(path: Path) -> str | None:
    match = AL_NAME.match(path.name)
    if not match:
        return None
    return f"{match.group('hour')}:{match.group('minute')}"


def date_dir(year: str, month: str, day: str) -> Path:
    return ROOT / "02_CONTENT" / year / month / day


def required_slots_for(year: str, month: str, day: str) -> set[str]:
    date_tuple = (int(year), int(month), int(day))
    if date_tuple >= TIME_CHANGE_FROM:
        return TIME_SHIFTED_REQUIRED_SLOTS
    return LEGACY_REQUIRED_SLOTS


def run_python_audit(module_name: str, args: list[str]) -> list[Issue]:
    module = importlib.import_module(module_name)
    findings = []
    for path in module.iter_scope(args):
        findings.extend(module.audit_file(path))
    return [Issue(item.severity, item.path, item.message) for item in findings]


def print_issues(issues: list[Issue]) -> None:
    for issue in issues:
        print(f"{issue.severity}: {rel(issue.path)} - {issue.message}")


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: preflight_day.py YYYY MM DD")
        return 2

    year, month, day = sys.argv[1:]
    target = date_dir(year, month, day)
    all_issues: list[Issue] = []
    results: list[CheckResult] = []

    print(f"# Almanac Day Preflight - {year}-{month}-{day}")
    print()

    if not target.exists():
        print(f"ERROR: missing day directory {target}")
        return 1

    files = sorted(target.glob("AL-*.md"))
    if len(files) != 3:
        all_issues.append(Issue("ERROR", target, f"expected 3 AL files, found {len(files)}"))

    slots = [slot_for(path) for path in files]
    required_slots = required_slots_for(year, month, day)
    missing_slots = sorted(required_slots - {slot for slot in slots if slot})
    duplicate_slots = sorted({slot for slot in slots if slot and slots.count(slot) > 1})
    for slot in missing_slots:
        all_issues.append(Issue("ERROR", target, f"missing slot {slot}"))
    for slot in duplicate_slots:
        all_issues.append(Issue("ERROR", target, f"duplicate slot {slot}"))

    for path in files:
        text = path.read_text(encoding="utf-8")
        metadata = service_metadata(text)
        status = metadata.get("status", "")
        if status not in READY_STATUSES:
            all_issues.append(Issue("ERROR", path, f"post is not ready: {status or 'missing status'}"))
        if metadata.get("date") and metadata["date"] != f"{year}-{month}-{day}":
            all_issues.append(Issue("ERROR", path, "date metadata does not match requested day"))
        all_issues.extend(validate_file(path, include_archive=False, strict_coverage=True))

    validation_errors = sum(1 for issue in all_issues if issue.severity == "ERROR")
    validation_warnings = sum(1 for issue in all_issues if issue.severity == "WARN")
    results.append(CheckResult("structure + validator", validation_errors, validation_warnings))

    style_issues = run_python_audit("audit_style", [year, month, day])
    all_issues.extend(style_issues)
    results.append(
        CheckResult(
            "style",
            sum(1 for issue in style_issues if issue.severity == "ERROR"),
            sum(1 for issue in style_issues if issue.severity == "WARN"),
        )
    )

    source_issues = run_python_audit("audit_sources", [year, month, day])
    all_issues.extend(source_issues)
    results.append(
        CheckResult(
            "sources",
            sum(1 for issue in source_issues if issue.severity == "ERROR"),
            sum(1 for issue in source_issues if issue.severity == "WARN"),
        )
    )

    length_issues = run_python_audit("audit_lengths", [year, month, day])
    all_issues.extend(length_issues)
    results.append(
        CheckResult(
            "lengths",
            sum(1 for issue in length_issues if issue.severity == "ERROR"),
            sum(1 for issue in length_issues if issue.severity == "WARN"),
        )
    )

    total_errors = sum(1 for issue in all_issues if issue.severity == "ERROR")
    total_warnings = sum(1 for issue in all_issues if issue.severity == "WARN")

    print(f"- Files checked: {len(files)}")
    for result in results:
        print(f"- {result.name}: {result.errors} errors, {result.warnings} warnings")
    print(f"- Total: {total_errors} errors, {total_warnings} warnings")

    if all_issues:
        print()
        print_issues(all_issues)

    return 1 if total_errors or total_warnings else 0


if __name__ == "__main__":
    sys.exit(main())
