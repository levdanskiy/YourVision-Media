#!/usr/bin/env python3
"""Audit ALMANAC rubric and theme rotation.

Usage:
    python3 tools/audit_rotation.py 2026 07        # one month
    python3 tools/audit_rotation.py                 # all July+ content
"""
from __future__ import annotations

import argparse
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

RECIPE_ONLY_FROM = date(2026, 7, 23)

SLOT_TIMES = {"09": "09:10 PREP", "15": "14:00 COOK", "21": "20:40 SWEET"}

ALLOWED_RECIPE_RUBRICS = {
    "CAKES", "BUNS", "PATISSERIE", "DESSERTS", "SWEETS",
    "BREAD", "FLATBREAD", "PIES",
    "FERMENT", "PRESERVE", "SOUP", "CONDIMENTS",
    "MAINS", "SALADS", "GRAINS", "LEGUMES", "VEGETABLES",
    "BREAKFAST", "RECIPE", "FOODWAYS", "PANTRY", "DRINKS",
    "TOOLS", "WORKFLOW", "LISTS", "FEAST_TABLE",
}

ALLOWED_PRE_PIVOT_RUBRICS = ALLOWED_RECIPE_RUBRICS | {
    "LORE", "PERSONAE", "BESTIARY", "OBJECTS", "SOURCE",
    "OMENS", "DIVINATION", "FRAGMENT", "ETYMON",
    "PROSE", "SYMBOL", "LOCUS", "ARTIFACT",
    "MYTHOS", "MORPHOLOGY", "CALENDAR", "CHRONOS",
    "HERITAGE", "FEAST", "MODERN", "CYCLES",
}

SWEET = {"CAKES", "BUNS", "PATISSERIE", "DESSERTS", "SWEETS"}
SAVORY_BAKE = {"BREAD", "FLATBREAD", "PIES"}
BROAD_FOOD = ALLOWED_RECIPE_RUBRICS - SWEET - SAVORY_BAKE

WEEKLY_MINIMUMS = {
    "sweet": (4, 6),
    "savory_bake": (4, 6),
    "broad_food": (6, 9),
    "ferment": (1, None),
    "preserve": (1, None),
    "soup": (1, None),
    "condiments": (1, None),
    "everyday": (2, None),
}


def iter_posts(year: int, month: int) -> list[dict]:
    month_dir = CONTENT / f"{year}" / f"{month:02d}"
    if not month_dir.exists():
        return []
    posts = []
    for path in sorted(month_dir.rglob("AL-*.md")):
        m = AL_NAME.match(path.name)
        if not m:
            continue
        slot = f"{m.group('hour')}:{m.group('minute')}"
        posts.append({
            "path": path,
            "day": int(m.group("day")),
            "month": month,
            "year": year,
            "slot": slot,
            "hour": m.group("hour"),
            "rubric": m.group("rubric"),
            "date": date(year, month, int(m.group("day"))),
        })
    return posts


def print_header(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def audit_month(year: int, month: int) -> int:
    posts = iter_posts(year, month)
    errors = 0
    warnings = 0

    print_header(f"ALMANAC ROTATION AUDIT — {year}-{month:02d}")
    print(f"Posts found: {len(posts)}")
    if not posts:
        print("No posts to audit.")
        return 0

    days_in_month = calendar.monthrange(year, month)[1]

    # --- Slot distribution ---
    slot_counts = Counter(p["slot"] for p in posts)
    print_header("1. SLOT DISTRIBUTION")
    for slot_key, slot_label in SLOT_TIMES.items():
        count = sum(c for s, c in slot_counts.items() if s.startswith(slot_key))
        expected = days_in_month
        flag = " ⚠️" if count < expected * 0.9 else ""
        print(f"  {slot_label:20s}: {count:3d}/{expected} posts{flag}")
    print()

    # --- Rubric distribution ---
    rubric_counts = Counter(p["rubric"] for p in posts)
    print_header("2. RUBRIC DISTRIBUTION (post-pivot = recipe only)")
    for r, c in sorted(rubric_counts.items(), key=lambda x: -x[1]):
        allowed = "✅" if r in ALLOWED_RECIPE_RUBRICS else "❌ ILLEGAL"
        print(f"  {r:20s}: {c:3d}  {allowed}")
    print()

    # --- Illegal rubrics post-pivot ---
    print_header("3. ILLEGAL RUBRICS AFTER 2026-07-23")
    illegal = [p for p in posts if p["date"] >= RECIPE_ONLY_FROM and p["rubric"] not in ALLOWED_RECIPE_RUBRICS]
    if illegal:
        for p in illegal:
            print(f"  ❌ {p['path'].name} — rubric {p['rubric']} not allowed post-pivot")
            errors += 1
    else:
        print("  All rubrics valid.")
    print()

    # --- Weekly rotation balance ---
    print_header("4. WEEKLY ROTATION BALANCE")
    by_week: dict[int, list[dict]] = defaultdict(list)
    for p in posts:
        by_week[p["date"].isocalendar()[1]].append(p)

    for week_num in sorted(by_week.keys()):
        week_posts = by_week[week_num]
        week_rubrics = Counter(p["rubric"] for p in week_posts)
        sweet = sum(week_rubrics.get(r, 0) for r in SWEET)
        savory = sum(week_rubrics.get(r, 0) for r in SAVORY_BAKE)
        broad = sum(week_rubrics.get(r, 0) for r in BROAD_FOOD)
        ferment = week_rubrics.get("FERMENT", 0)
        preserve = week_rubrics.get("PRESERVE", 0)

        issues = []
        if sweet < 4:
            issues.append(f"sweet={sweet}<4")
        if sweet > 6:
            issues.append(f"sweet={sweet}>6")
        if savory < 4:
            issues.append(f"savory_bake={savory}<4")
        if ferment < 1:
            issues.append("no FERMENT")
        if preserve < 1:
            issues.append("no PRESERVE")

        status = "OK" if not issues else "⚠️ " + ", ".join(issues)
        print(f"  W{week_num:02d}: sweet={sweet} savory={savory} broad={broad} ferment={ferment} preserve={preserve}  {status}")
    print()

    # --- Three-sweet-day check ---
    print_header("5. SWEET CLUSTER CHECK (max 2 sweet/day)")
    by_day: dict[date, list[dict]] = defaultdict(list)
    for p in posts:
        by_day[p["date"]].append(p)
    sweet_cluster_days = 0
    for d in sorted(by_day.keys()):
        day_sweet = sum(1 for p in by_day[d] if p["rubric"] in SWEET)
        if day_sweet >= 3:
            print(f"  {d.isoformat()}: {day_sweet} sweet posts")
            sweet_cluster_days += 1
            warnings += 1
    if sweet_cluster_days == 0:
        print("  No days with 3+ sweet posts.")
    print()

    # --- Consecutive same-rubric check ---
    print_header("6. CONSECUTIVE SAME-RUBRIC CHECK")
    by_slot_date: dict[str, list[dict]] = defaultdict(list)
    for p in posts:
        by_slot_date[p["slot"]].append(p)
    consec_issues = 0
    for slot in sorted(by_slot_date.keys()):
        slot_posts = sorted(by_slot_date[slot], key=lambda x: x["date"])
        for i in range(1, len(slot_posts)):
            if slot_posts[i]["rubric"] == slot_posts[i - 1]["rubric"]:
                gap = (slot_posts[i]["date"] - slot_posts[i - 1]["date"]).days
                if gap <= 2:
                    print(f"  {slot}: {slot_posts[i-1]['rubric']} on {slot_posts[i-1]['date'].isoformat()} -> same on {slot_posts[i]['date'].isoformat()}")
                    consec_issues += 1
                    warnings += 1
    if consec_issues == 0:
        print("  No consecutive same-rubric issues.")
    print()

    # --- Cultural zone coverage ---
    print_header("7. CULTURAL ZONE COVERAGE")
    zone_counts: Counter[str] = Counter()
    no_zone = 0
    for p in posts:
        text = p["path"].read_text(encoding="utf-8")
        zones_found = []
        for zone in ["Africa", "Asia", "America", "Oceania", "Europe",
                      "Африка", "Азия", "Америка", "Океания", "Европа",
                      "Latin", "Indigenous", "Caribbean", "Middle East",
                      "South Asia", "East Asia", "Southeast Asia"]:
            if zone.lower() in text.lower():
                zones_found.append(zone)
        if zones_found:
            for z in zones_found:
                zone_counts[z] += 1
        else:
            no_zone += 1
    for zone, count in zone_counts.most_common(10):
        print(f"  {zone:20s}: {count}")
    if no_zone:
        print(f"  No zone detected: {no_zone} posts")
    print()

    # --- Rubric repetition (same rubric within 5 days) ---
    print_header("8. RUBRIC REPETITION (same rubric within 5 days)")
    by_rubric_dates: dict[str, list[date]] = defaultdict(list)
    for p in posts:
        by_rubric_dates[p["rubric"]].append(p["date"])
    rep_issues = 0
    for rubric, dates in sorted(by_rubric_dates.items()):
        unique = sorted(set(dates))
        for i in range(1, len(unique)):
            gap = (unique[i] - unique[i - 1]).days
            if gap <= 5:
                print(f"  {rubric}: {unique[i-1].isoformat()} -> {unique[i].isoformat()} ({gap}d)")
                rep_issues += 1
                warnings += 1
    if rep_issues == 0:
        print("  No rubric repetition within 5 days.")
    print()

    # --- Summary ---
    print_header("SUMMARY")
    print(f"  Total posts: {len(posts)}")
    print(f"  Days covered: {len(by_day)}/{days_in_month}")
    print(f"  Unique rubrics: {len(rubric_counts)}")
    print(f"  Illegal rubrics post-pivot: {len(illegal)}")
    print(f"  Errors: {errors}")
    print(f"  Warnings: {warnings}")
    print()

    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit ALMANAC rubric and theme rotation")
    parser.add_argument("year", nargs="?", type=int, default=2026)
    parser.add_argument("month", nargs="?", type=int, default=7)
    args = parser.parse_args()
    return audit_month(args.year, args.month)


if __name__ == "__main__":
    sys.exit(main())
