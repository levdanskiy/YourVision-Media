#!/usr/bin/env python3
"""Print a month-level Almanac content audit."""

from __future__ import annotations

import calendar
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "02_CONTENT"
AL_NAME = re.compile(
    r"^AL-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rubric>[A-Z]+)-?.*\.md$"
)
LEGACY_EXPECTED_SLOTS = {"10:04", "15:04", "18:02"}
TIME_SHIFTED_EXPECTED_SLOTS = {"09:04", "15:04", "21:04"}
SUNDAY = 6
NEW_SLOT_RULES_FROM = (2026, 7, 7)
TIME_CHANGE_FROM = (2026, 7, 17)
RECIPE_ONLY_FROM = (2026, 7, 23)
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
    "MAINS",
    "SALADS",
    "GRAINS",
    "LEGUMES",
    "VEGETABLES",
    "BREAKFAST",
    "FOODWAYS",
    "PANTRY",
    "DRINKS",
    "TOOLS",
    "LISTS",
    "WORKFLOW",
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
    "10:04": {"LORE", "SOURCE", "OMENS", "DIVINATION", "PERSONAE", "BESTIARY", "OBJECTS", "FRAGMENT", "ETYMON", "PROSE"},
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
        "MAINS",
        "SALADS",
        "GRAINS",
        "LEGUMES",
        "VEGETABLES",
        "BREAKFAST",
        "FOODWAYS",
        "PANTRY",
        "DRINKS",
        "TOOLS",
        "LISTS",
        "WORKFLOW",
    },
    "18:02": {"CHRONOS", "CALENDAR", "HERITAGE", "WHEEL", "CYCLES", "MODERN", "RITES", "FEAST", "ETYMON"},
}

TIME_SHIFTED_SLOT_RUBRICS = {
    "09:04": SLOT_RUBRICS["10:04"],
    "15:04": SLOT_RUBRICS["15:04"],
    "21:04": SLOT_RUBRICS["18:02"],
}

RECIPE_ONLY_SLOT_RUBRICS = {
    "09:04": FOOD_RUBRICS,
    "15:04": FOOD_RUBRICS,
    "21:04": FOOD_RUBRICS,
}


def expected_slots_for(date_tuple: tuple[int, int, int]) -> set[str]:
    if date_tuple >= TIME_CHANGE_FROM:
        return TIME_SHIFTED_EXPECTED_SLOTS
    return LEGACY_EXPECTED_SLOTS


def slot_rubrics_for(date_tuple: tuple[int, int, int]) -> dict[str, set[str]]:
    if date_tuple >= RECIPE_ONLY_FROM:
        return RECIPE_ONLY_SLOT_RUBRICS
    if date_tuple >= TIME_CHANGE_FROM:
        return TIME_SHIFTED_SLOT_RUBRICS
    return SLOT_RUBRICS if date_tuple >= NEW_SLOT_RULES_FROM else LEGACY_SLOT_RUBRICS


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


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 tools/audit_month.py YEAR MM", file=sys.stderr)
        return 2

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    month_dir = CONTENT / f"{year}" / f"{month:02d}"

    if not month_dir.exists():
        print(f"Month directory not found: {month_dir}", file=sys.stderr)
        return 1

    days_in_month = calendar.monthrange(year, month)[1]
    by_day: dict[int, list[Path]] = defaultdict(list)
    by_slot: Counter[str] = Counter()
    by_rubric: Counter[str] = Counter()
    by_week: dict[int, Counter[str]] = defaultdict(Counter)
    days_by_week: dict[int, set[int]] = defaultdict(set)
    long_posts: list[tuple[int, Path]] = []
    rotation_issues: list[str] = []

    for path in sorted(month_dir.rglob("AL-*.md")):
        match = AL_NAME.match(path.name)
        if not match:
            continue
        day = int(match.group("day"))
        slot = f"{match.group('hour')}:{match.group('minute')}"
        rubric = match.group("rubric")
        by_day[day].append(path)
        by_slot[slot] += 1
        by_rubric[rubric] += 1
        week = date(year, month, day).isocalendar().week
        by_week[week][rubric] += 1
        days_by_week[week].add(day)

        allowed = slot_rubrics_for((year, month, day)).get(slot)
        if allowed and rubric not in allowed:
            rotation_issues.append(
                f"{year}-{month:02d}-{day:02d} `{path.name}` uses `{rubric}` in slot `{slot}`"
            )

        body_len = len(body_text(path.read_text(encoding="utf-8")))
        if body_len > 2700:
            long_posts.append((body_len, path))

    print(f"# Almanac Audit - {year}-{month:02d}")
    print()
    print(f"- AL posts: {sum(len(paths) for paths in by_day.values())}")
    print(f"- Days with content: {len(by_day)} / {days_in_month}")
    print()

    print("## Slot Counts")
    print()
    display_slots = set(LEGACY_EXPECTED_SLOTS) | set(TIME_SHIFTED_EXPECTED_SLOTS) | set(by_slot)
    for slot in sorted(display_slots):
        print(f"- `{slot}`: {by_slot[slot]}")
    print()

    print("## Rubric Counts")
    print()
    for rubric, count in by_rubric.most_common():
        print(f"- `{rubric}`: {count}")
    print()

    print("## Missing Or Extra Slots")
    print()
    any_gap = False
    for day in range(1, days_in_month + 1):
        slots = []
        for path in by_day.get(day, []):
            match = AL_NAME.match(path.name)
            if match:
                slots.append(f"{match.group('hour')}:{match.group('minute')}")
        expected_slots = expected_slots_for((year, month, day))
        missing = sorted(expected_slots - set(slots))
        extras = sorted(slot for slot in slots if slots.count(slot) > 1)
        if missing or extras or len(slots) != 3:
            any_gap = True
            print(f"- {year}-{month:02d}-{day:02d}: {len(slots)} posts, missing {missing or 'none'}, duplicate {sorted(set(extras)) or 'none'}")
    if not any_gap:
        print("- No slot gaps detected.")
    print()

    print("## Rotation Rules")
    print()
    for day in range(1, days_in_month + 1):
        day_date = date(year, month, day)
        if (year, month, day) < RECIPE_ONLY_FROM and day_date.weekday() == SUNDAY and day in by_day:
            sunday_fragment = False
            for path in by_day.get(day, []):
                match = AL_NAME.match(path.name)
                expected_fragment_slot = "09:04" if (year, month, day) >= TIME_CHANGE_FROM else "10:04"
                slot = f"{match.group('hour')}:{match.group('minute')}"
                if match and slot == expected_fragment_slot:
                    if (year, month, day) >= NEW_SLOT_RULES_FROM:
                        sunday_fragment = match.group("rubric") in {"FRAGMENT", "PROSE", "ETYMON"}
                    else:
                        sunday_fragment = match.group("rubric") == "FRAGMENT"
            if not sunday_fragment:
                if (year, month, day) >= NEW_SLOT_RULES_FROM:
                    slot_label = "09:04" if (year, month, day) >= TIME_CHANGE_FROM else "10:04"
                    rotation_issues.append(f"{year}-{month:02d}-{day:02d} Sunday {slot_label} is not `FRAGMENT`, `PROSE`, or `ETYMON`")
                else:
                    rotation_issues.append(f"{year}-{month:02d}-{day:02d} Sunday 10:04 is not `FRAGMENT`")

    for week, counts in sorted(by_week.items()):
        if counts["LISTS"] > 1:
            rotation_issues.append(f"ISO week {week}: `LISTS` appears {counts['LISTS']} times")
        week_dates = [date(year, month, day_number) for day_number in days_by_week[week]]
        if len(days_by_week[week]) >= 7 and max(week_dates) < date(*RECIPE_ONLY_FROM) and counts["HERITAGE"] == 0:
            rotation_issues.append(f"ISO week {week}: no `HERITAGE` post")
        if counts["HERITAGE"] > 2:
            rotation_issues.append(f"ISO week {week}: `HERITAGE` appears {counts['HERITAGE']} times")

    if rotation_issues:
        for issue in rotation_issues:
            print(f"- {issue}")
    else:
        print("- No rotation issues detected.")
    print()

    print("## Long Posts")
    print()
    if not long_posts:
        print("- No posts over 2700 detected by body counter.")
    else:
        for body_len, path in sorted(long_posts, reverse=True)[:30]:
            print(f"- {body_len}: `{path.relative_to(ROOT)}`")

    return 0


if __name__ == "__main__":
    sys.exit(main())
