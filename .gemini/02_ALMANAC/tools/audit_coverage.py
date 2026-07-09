#!/usr/bin/env python3
"""Audit Almanac cultural coverage metadata for one month."""

from __future__ import annotations

import calendar
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "02_CONTENT"
AL_NAME = re.compile(
    r"^AL-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rubric>[A-Z]+)-?.*\.md$"
)

VALID_ZONES = {
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
NON_EUROPEAN = VALID_ZONES - {"Europe"}
THEME_BY_SLOT = {
    "10:04": "morning myths/tales/omens/divination/personae",
    "09:10": "morning myths/tales/omens/divination/personae",
    "14:00": "14:00 food/desserts/baking/bread/foodways",
    "18:02": "evening calendar/ritual/time/feast",
    "20:40": "evening calendar/ritual/time/feast",
}
RECIPE_ONLY_FROM = date(2026, 7, 23)
REQUIRED_UNDERREPRESENTED = [
    {"Africa", "African Diaspora"},
    {"Indigenous Americas"},
    {"Oceania", "Island Cultures"},
    {"South Asia", "Southeast Asia"},
    {"Global Modern"},
]


def theme_for(year: int, month: int, day: int, slot: str) -> str:
    if date(year, month, day) >= RECIPE_ONLY_FROM:
        if slot == "09:10":
            return "09:10 prep/base recipe"
        if slot == "14:00":
            return "14:00 cook/table recipe"
        if slot == "20:40":
            return "20:40 slow/sweet recipe"
    return THEME_BY_SLOT.get(slot, slot)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    metadata: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line == "---":
            break
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"').strip("'")
    return metadata


def service_metadata(text: str) -> dict[str, str]:
    metadata = simple_frontmatter(text)
    for line in text.splitlines()[:50]:
        if not line.startswith("//"):
            continue
        body = line[2:].strip()
        if ":" not in body:
            continue
        key, value = body.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key in {"cultural_zone", "coverage_axis", "source_type", "secondary_zones"}:
            metadata.setdefault(key, value)
    return metadata


def month_posts(year: int, month: int) -> list[Path]:
    month_dir = CONTENT / f"{year}" / f"{month:02d}"
    if not month_dir.exists():
        raise FileNotFoundError(f"Month directory not found: {month_dir}")
    return sorted(path for path in month_dir.rglob("AL-*.md") if AL_NAME.match(path.name))


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 tools/audit_coverage.py YEAR MM", file=sys.stderr)
        return 2

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    try:
        posts = month_posts(year, month)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    by_zone: Counter[str] = Counter()
    by_theme_zone: dict[str, Counter[str]] = defaultdict(Counter)
    by_axis: Counter[str] = Counter()
    missing_metadata: list[Path] = []
    invalid_zone: list[tuple[Path, str]] = []
    unknown_source_type: list[Path] = []

    for path in posts:
        match = AL_NAME.match(path.name)
        if not match:
            continue
        slot = f"{match.group('hour')}:{match.group('minute')}"
        theme = theme_for(year, month, int(match.group("day")), slot)
        metadata = service_metadata(path.read_text(encoding="utf-8"))
        zone = metadata.get("cultural_zone")
        axis = metadata.get("coverage_axis")
        source_type = metadata.get("source_type")

        if not zone or not axis or not source_type:
            missing_metadata.append(path)
            continue
        if zone not in VALID_ZONES:
            invalid_zone.append((path, zone))
            continue

        by_zone[zone] += 1
        by_theme_zone[theme][zone] += 1
        by_axis[axis] += 1
        if len(source_type) < 3:
            unknown_source_type.append(path)

    known = sum(by_zone.values())
    non_european = sum(count for zone, count in by_zone.items() if zone in NON_EUROPEAN)
    days_in_month = calendar.monthrange(year, month)[1]

    print(f"# Almanac Coverage Audit - {year}-{month:02d}")
    print()
    print(f"- AL posts: {len(posts)}")
    print(f"- Days in month: {days_in_month}")
    print(f"- Posts with coverage metadata: {known}")
    print(f"- Missing coverage metadata: {len(missing_metadata)}")
    print(f"- Cultural zones represented: {len(by_zone)}")
    if known:
        print(f"- Non-European / cross-global coverage: {non_european}/{known} ({non_european / known:.0%})")
    print()

    print("## Zone Counts")
    print()
    if by_zone:
        for zone, count in by_zone.most_common():
            print(f"- `{zone}`: {count}")
    else:
        print("- No coverage metadata found.")
    print()

    print("## Theme Coverage")
    print()
    theme_order = list(dict.fromkeys(THEME_BY_SLOT.values())) + [
        "09:10 prep/base recipe",
        "14:00 cook/table recipe",
        "20:40 slow/sweet recipe",
    ]
    for theme in theme_order:
        zones = by_theme_zone.get(theme, Counter())
        print(f"### {theme}")
        if zones:
            for zone, count in zones.most_common():
                print(f"- `{zone}`: {count}")
        else:
            print("- No coverage metadata found.")
        print()

    print("## Coverage Axes")
    print()
    if by_axis:
        for axis, count in by_axis.most_common():
            print(f"- `{axis}`: {count}")
    else:
        print("- No coverage axes found.")
    print()

    print("## Coverage Debt")
    print()
    debt = False
    if len(by_zone) < 6:
        debt = True
        print(f"- Need at least 6 cultural zones; found {len(by_zone)}.")
    for theme, zones in by_theme_zone.items():
        if len(zones) < 3:
            debt = True
            print(f"- `{theme}` needs at least 3 zones; found {len(zones)}.")
    for required_group in REQUIRED_UNDERREPRESENTED:
        if not (set(by_zone) & required_group):
            debt = True
            print(f"- Missing required monthly group: {', '.join(sorted(required_group))}.")
    if known and non_european / known < 0.5:
        debt = True
        print("- Non-European/cross-global coverage below 50%.")
    if invalid_zone:
        debt = True
        print(f"- Invalid cultural_zone values: {len(invalid_zone)}.")
    if unknown_source_type:
        debt = True
        print(f"- Suspicious source_type values: {len(unknown_source_type)}.")
    if missing_metadata:
        debt = True
        print("- Add `cultural_zone`, `coverage_axis`, and `source_type` metadata to posts.")
    if not debt:
        print("- No coverage debt detected.")
    print()

    if invalid_zone:
        print("## Invalid Zones")
        print()
        for path, zone in invalid_zone[:30]:
            print(f"- `{rel(path)}`: `{zone}`")
        print()

    if missing_metadata:
        print("## Missing Metadata")
        print()
        for path in missing_metadata[:60]:
            print(f"- `{rel(path)}`")

    return 0


if __name__ == "__main__":
    sys.exit(main())
