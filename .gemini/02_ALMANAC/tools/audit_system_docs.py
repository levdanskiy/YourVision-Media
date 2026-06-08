#!/usr/bin/env python3
"""Audit Almanac system docs for stale rubric and regional-anchor language."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORE_DOCS = [
    ROOT / "README.md",
    ROOT / "01_BIBLES" / "ALMANAC_BIBLE.md",
    ROOT / "01_BIBLES" / "RUBRIC_TAXONOMY.md",
    ROOT / "01_BIBLES" / "WORLD_COVERAGE_MATRIX.md",
    ROOT / "01_BIBLES" / "MONTHLY_PLANNING_TEMPLATE.md",
    ROOT / "01_BIBLES" / "RUBRIC_RULES.md",
    ROOT / "01_BIBLES" / "ARCHIVE_TEMPLATE.md",
    ROOT / "01_BIBLES" / "VOICE_LEXICON.md",
    ROOT / "01_BIBLES" / "CONTEMPORARY_STYLE_GUIDE.md",
    ROOT / "01_BIBLES" / "INTERACTIVITY_SYSTEM.md",
    ROOT / "01_BIBLES" / "SLOT_STRATEGY.md",
    ROOT / "01_BIBLES" / "SERVICE_AND_SPECIALS.md",
    ROOT / "01_BIBLES" / "FORMAT_EXTENSIONS.md",
    ROOT / "01_BIBLES" / "FOOD_TECHNOLOGY_MATRIX.md",
    ROOT / "01_BIBLES" / "CALENDAR_SYSTEMS_BANK.md",
    ROOT / "01_BIBLES" / "ANALYTICS_REVIEW.md",
    ROOT / "01_BIBLES" / "DISTRIBUTION_RULES.md",
    ROOT / "01_BIBLES" / "VISUAL_SYSTEM.md",
    ROOT / "01_BIBLES" / "PRE_PUBLISH_CHECKLIST.md",
    ROOT / "01_BIBLES" / "ROTATION_GUIDE.md",
    ROOT / "01_BIBLES" / "SOURCES.md",
    ROOT / "01_BIBLES" / "SOURCE_DATABASES.md",
    ROOT / "01_BIBLES" / "BAKERY_BIBLE.md",
    ROOT / "01_BIBLES" / "HOLIDAYS_BIBLE.md",
    ROOT / "01_BIBLES" / "STATUS_MODEL.md",
    ROOT / "01_BIBLES" / "VISUAL_PIPELINE.md",
    ROOT / "01_BIBLES" / "FACTCHECK_RULES.md",
]

HISTORICAL_DOCS = [
    ROOT / "01_BIBLES" / "CONTENT_CALENDAR.md",
    ROOT / "01_BIBLES" / "MAY_STRATEGY.md",
    ROOT / "01_BIBLES" / "JUNE_STRATEGY.md",
    ROOT / "01_BIBLES" / "JULY_AUGUST_STRATEGY.md",
    ROOT / "01_BIBLES" / "PLAN_16-31_MAY.md",
    ROOT / "01_BIBLES" / "PLAN_JUNE.md",
    ROOT / "01_BIBLES" / "PLAN_JULY.md",
    ROOT / "01_BIBLES" / "IDEAS_BANK.md",
    ROOT / "01_BIBLES" / "MYTHO_ATLAS.md",
    ROOT / "01_BIBLES" / "SENSORY_ATLAS.md",
]

STALE_CORE_PATTERNS = [
    re.compile(r"ТЕМА I:\s*ВЫПЕЧКА"),
    re.compile(r"(?<!НЕ)СЛАДКАЯ ВЫПЕЧКА"),
    re.compile(r"Региональный\s*/\s*умирающий"),
    re.compile(r"Правило 2\+1"),
    re.compile(r"домашн(ий|его|ем|ая)\s+(город|регион|оптик|точк)"),
]

REGIONAL_ANCHOR_PATTERNS = [
    re.compile(r"\b(у нас|у меня|здесь)\b.*\b(в стране|в регионе|в городе|в риге|в латвии)\b", re.IGNORECASE),
    re.compile(r"\b(наш|наша|наше|нашего|нашем)\b.*\b(город|страна|регион|широта|климат|традиция)\b", re.IGNORECASE),
    re.compile(r"\b(publication_timezone|timezone)\b.*\b(editorial|оптик|центр|голос|якор)\b", re.IGNORECASE),
    re.compile(r"\b(riga|latvia|baltic|baltics)\b.*\b(default|home|anchor|lens|voice)\b", re.IGNORECASE),
    re.compile(r"\b(рига|латвия|балтийск)\w*\b.*\b(по умолчанию|домашн|оптик|центр|голос|якор)\b", re.IGNORECASE),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def scan_file(path: Path, patterns: list[re.Pattern[str]]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    if not path.exists():
        return hits
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        lowered = line.lower()
        if any(
            marker in lowered
            for marker in [
                "нет домашнего",
                "без домашнего",
                "не от домашнего",
                "не является редакционным якорем",
                "не превращая город",
                "do not turn",
                "remove only default-center",
                "not the channel",
                "the rule is not",
                "the rule is \"no geography",
            ]
        ):
            continue
        for pattern in patterns:
            if pattern.search(line):
                hits.append((lineno, line.strip()))
                break
    return hits


def main() -> int:
    core_hits: list[tuple[Path, int, str]] = []
    historical_hits: list[tuple[Path, int, str]] = []

    for path in CORE_DOCS:
        for lineno, line in scan_file(path, STALE_CORE_PATTERNS + REGIONAL_ANCHOR_PATTERNS):
            core_hits.append((path, lineno, line))

    for path in HISTORICAL_DOCS:
        for lineno, line in scan_file(path, REGIONAL_ANCHOR_PATTERNS):
            historical_hits.append((path, lineno, line))

    print("# Almanac System Docs Audit")
    print()
    print("## Core Source-Of-Truth Hits")
    print()
    if core_hits:
        for path, lineno, line in core_hits:
            print(f"- `{rel(path)}:{lineno}` {line}")
    else:
        print("- No stale core rubric or regional-anchor language detected.")
    print()

    print("## Historical / Planning Hits")
    print()
    print("These are not automatically errors, but they must be rebuilt through current global rules before reuse.")
    print()
    if historical_hits:
        for path, lineno, line in historical_hits[:120]:
            print(f"- `{rel(path)}:{lineno}` {line}")
        if len(historical_hits) > 120:
            print(f"- ... {len(historical_hits) - 120} more")
    else:
        print("- No historical regional-anchor hits detected.")

    return 1 if core_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
