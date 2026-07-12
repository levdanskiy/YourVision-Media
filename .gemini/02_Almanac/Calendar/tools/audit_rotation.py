#!/usr/bin/env python3
"""Audit rubric and theme rotation for LEXICON.

Usage:
    python3 tools/audit_rotation.py 2026 07        # one month
    python3 tools/audit_rotation.py 2026 07 --week 28  # one ISO week
    python3 tools/audit_rotation.py                 # all content so far
"""
from __future__ import annotations

import argparse
import calendar
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta

from lexicon_common import (
    CONTENT, ALL_RUBRICS, SLOT_RUBRICS, SLOT_TIMES,
    iter_all_posts, Post,
)


def week_number(d: date) -> int:
    return d.isocalendar()[1]


def month_range(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def print_header(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def audit_month(year: int, month: int) -> int:
    posts = iter_all_posts(year, month)
    return _audit(posts, f"{year}-{month:02d}", year, month)


def audit_week(year: int, iso_week: int) -> int:
    posts = iter_all_posts(year)
    # Filter to ISO week
    filtered = [p for p in posts if p.publication_date.isocalendar()[1] == iso_week]
    return _audit(filtered, f"{year}-W{iso_week:02d}", year, None)


def audit_all() -> int:
    posts = iter_all_posts()
    return _audit(posts, "all content", None, None)


def _audit(posts: list[Post], label: str, year: int | None, month: int | None) -> int:
    errors = 0
    warnings = 0

    print_header(f"LEXICON ROTATION AUDIT — {label}")
    print(f"Posts found: {len(posts)}")
    if not posts:
        print("No posts to audit.")
        return 0

    # --- Slot distribution ---
    slot_counts = Counter(p.slot for p in posts)
    print_header("1. SLOT DISTRIBUTION (balance = 25% each)")
    total = len(posts)
    for slot in ["AURORA", "ANIMA", "LOCUS", "MYTHOS"]:
        count = slot_counts.get(slot, 0)
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        flag = " ⚠️" if pct < 20 else ""
        print(f"  {slot:8s} ({SLOT_TIMES[slot]}): {count:3d} posts ({pct:5.1f}%) {bar}{flag}")
    print()

    # --- Rubric distribution ---
    rubric_counts = Counter(p.rubric for p in posts)
    print_header("2. RUBRIC DISTRIBUTION")
    for slot_name in ["AURORA", "ANIMA", "LOCUS", "MYTHOS"]:
        slot_rubrics = SLOT_RUBRICS[slot_name]
        used = {r: rubric_counts.get(r, 0) for r in slot_rubrics if rubric_counts.get(r, 0) > 0}
        unused = slot_rubrics - set(used.keys())
        print(f"  [{slot_name}]")
        for r, c in sorted(used.items(), key=lambda x: -x[1]):
            print(f"    {r:20s}: {c}")
        if unused:
            print(f"    UNUSED: {', '.join(sorted(unused))}")
        print()

    # --- Daily completeness ---
    print_header("3. DAILY COMPLETENESS")
    by_date: dict[date, dict[str, Post]] = defaultdict(dict)
    for p in posts:
        by_date[p.publication_date][p.slot] = p

    missing_days = 0
    partial_days = 0
    complete_days = 0
    for d in sorted(by_date.keys()):
        slots = set(by_date[d].keys())
        expected = {"AURORA", "ANIMA", "LOCUS", "MYTHOS"}
        missing = expected - slots
        if not missing:
            complete_days += 1
        elif len(slots) == 0:
            missing_days += 1
        else:
            partial_days += 1
            print(f"  {d.isoformat()}: missing {', '.join(sorted(missing))}")
            warnings += 1

    print(f"  Complete days (4/4): {complete_days}")
    print(f"  Partial days: {partial_days}")
    print(f"  Empty days: {missing_days}")
    print()

    # --- Rubric repetition check ---
    print_header("4. RUBRIC REPETITION (same rubric within 7 days)")
    by_rubric_date: dict[str, list[date]] = defaultdict(list)
    for p in posts:
        by_rubric_date[p.rubric].append(p.publication_date)

    repetition_issues = 0
    for rubric, dates in sorted(by_rubric_date.items()):
        unique_dates = sorted(set(dates))
        for i in range(1, len(unique_dates)):
            gap = (unique_dates[i] - unique_dates[i - 1]).days
            if gap <= 3:
                print(f"  {rubric}: {unique_dates[i-1].isoformat()} -> {unique_dates[i].isoformat()} ({gap}d gap)")
                repetition_issues += 1
                warnings += 1
    if repetition_issues == 0:
        print("  No rubric repetition within 3 days detected.")
    print()

    # --- Series check ---
    print_header("5. SERIES TRACKING")
    series_posts = [p for p in posts if "SEQUENCE" in p.rubric.upper() or "SERIES" in (p.metadata.get("series_id", "") or "").upper()]
    if series_posts:
        series_ids = Counter(p.metadata.get("series_id", "unknown") for p in series_posts)
        for sid, count in series_ids.most_common():
            print(f"  Series '{sid}': {count} posts")
    else:
        print("  No active series detected in posts.")
    print()

    # --- Topic cooldown check ---
    print_header("6. TOPIC COOLDOWN (30-day rule)")
    by_topic_dates: dict[str, list[date]] = defaultdict(list)
    for p in posts:
        by_topic_dates[p.rubric].append(p.publication_date)

    cooldown_violations = 0
    for topic, dates in sorted(by_topic_dates.items()):
        unique = sorted(set(dates))
        for i in range(1, len(unique)):
            gap = (unique[i] - unique[i - 1]).days
            if gap < 30 and gap > 0:
                # Only report if not in a series context
                print(f"  {topic}: {unique[i-1].isoformat()} -> {unique[i].isoformat()} ({gap}d, <30d cooldown)")
                cooldown_violations += 1
                warnings += 1
    if cooldown_violations == 0:
        print("  No cooldown violations detected.")
    print()

    # --- Global coverage (cultural zones) ---
    print_header("7. CULTURAL ZONE COVERAGE")
    zone_counts: Counter[str] = Counter()
    no_zone = 0
    for p in posts:
        text = p.path.read_text(encoding="utf-8")
        # Look for cultural zone markers in text
        zones_found = []
        for zone in ["Европа", "Азия", "Африка", "Америка", "Океания",
                      "Europe", "Asia", "Africa", "Americas", "Oceania"]:
            if zone.lower() in text.lower():
                zones_found.append(zone)
        if zones_found:
            for z in zones_found:
                zone_counts[z] += 1
        else:
            no_zone += 1

    if zone_counts:
        for zone, count in zone_counts.most_common():
            print(f"  {zone:15s}: {count}")
    if no_zone:
        print(f"  No zone detected: {no_zone} posts")
    print()

    # --- Summary ---
    print_header("SUMMARY")
    print(f"  Total posts: {total}")
    print(f"  Complete days: {complete_days}/{complete_days + partial_days + missing_days}")
    print(f"  Unique rubrics used: {len(set(p.rubric for p in posts))}/{len(ALL_RUBRICS)}")
    print(f"  Errors: {errors}")
    print(f"  Warnings: {warnings}")
    print()

    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit LEXICON rubric and theme rotation")
    parser.add_argument("year", nargs="?", type=int)
    parser.add_argument("month", nargs="?", type=int)
    parser.add_argument("--week", type=int, help="ISO week number")
    args = parser.parse_args()

    if args.week and args.year:
        return audit_week(args.year, args.week)
    elif args.year and args.month:
        return audit_month(args.year, args.month)
    elif args.year:
        return audit_month(args.year, args.month or 1)
    else:
        return audit_all()


if __name__ == "__main__":
    sys.exit(main())
