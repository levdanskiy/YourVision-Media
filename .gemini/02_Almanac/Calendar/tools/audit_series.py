#!/usr/bin/env python3
"""Audit series deadlines and service/special publishing pressure."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date

from lexicon_common import DATABASES, iter_posts, parse_date_target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=date.today().isoformat())
    args = parser.parse_args()
    day = parse_date_target(args.target)
    data = json.loads((DATABASES / "SERIES_REGISTRY.json").read_text(encoding="utf-8"))
    warnings: list[str] = []
    for series in data.get("series", []):
        due = series.get("next_due")
        if due and series.get("status") in {"active", "pilot"} and date.fromisoformat(due) < day:
            warnings.append(f"overdue series `{series['series_id']}` since {due}")

    month_posts = iter_posts(day.strftime("%Y-%m"), prefixes={"SV", "SP"})
    monthly = Counter(post.prefix for post in month_posts)
    week_posts = [
        post for post in month_posts
        if post.publication_date.isocalendar()[:2] == day.isocalendar()[:2]
    ]
    weekly = Counter(post.prefix for post in week_posts)
    errors: list[str] = []
    if weekly["SV"] > 2:
        warnings.append(f"ISO week has {weekly['SV']} SV posts; maximum is 2")
    if monthly["SP"] > 4:
        warnings.append(f"month has {monthly['SP']} SP posts; maximum is 4")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    print(
        f"SERIES/SERVICE: week SV={weekly['SV']}/2; "
        f"month SP={monthly['SP']}/2-4; {len(errors)} errors, {len(warnings)} warnings"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
