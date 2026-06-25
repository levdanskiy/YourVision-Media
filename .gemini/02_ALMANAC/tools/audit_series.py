#!/usr/bin/env python3
"""Audit series deadlines and service/special publishing pressure."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date

from almanac_common import DATABASES, iter_posts, parse_date_target


RECIPE_ONLY_FROM = date(2026, 7, 23)


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
    oracle_count = sum(1 for post in week_posts if "ORACLE-NOTE" in post.path.name)
    radar_count = sum(1 for post in week_posts if "CALENDAR-RADAR" in post.path.name)
    errors: list[str] = []
    if weekly["SV"] > 2:
        warnings.append(f"ISO week has {weekly['SV']} SV posts; maximum is 2")
    if date(2026, 7, 20) <= day < RECIPE_ONLY_FROM:
        if oracle_count == 0 and day.isoweekday() >= 4:
            warnings.append("required weekly ORACLE-NOTE is missing")
        if radar_count == 0 and day.isoweekday() >= 2:
            warnings.append("required weekly CALENDAR-RADAR is missing")
        if day.isoweekday() == 7 and (oracle_count != 1 or radar_count != 1):
            errors.append("week cannot close without exactly one ORACLE-NOTE and one CALENDAR-RADAR")
    if day >= RECIPE_ONLY_FROM:
        non_recipe_service = [
            post.path.name
            for post in week_posts
            if not any(kind in post.path.name for kind in ("MENU-RADAR", "SHOPPING-LIST", "TECHNIQUE-POLL", "RECIPE-INDEX", "PREP-NOTE"))
            and post.publication_date >= RECIPE_ONLY_FROM
        ]
        if non_recipe_service:
            errors.append(f"recipe-only week has non-recipe service: {', '.join(non_recipe_service)}")
    if monthly["SP"] > 4:
        warnings.append(f"month has {monthly['SP']} SP posts; maximum is 4")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    if day >= RECIPE_ONLY_FROM:
        recipe_service_count = sum(
            1 for post in week_posts
            if any(kind in post.path.name for kind in ("MENU-RADAR", "SHOPPING-LIST", "TECHNIQUE-POLL", "RECIPE-INDEX", "PREP-NOTE"))
        )
        print(
            f"SERIES/SERVICE: recipe-only week SV={weekly['SV']}/0-2, recipe_service={recipe_service_count}; "
            f"month SP={monthly['SP']}/2-4; non-recipe service routed to LEXICON; {len(errors)} errors, {len(warnings)} warnings"
        )
    else:
        print(
            f"SERIES/SERVICE: week SV={weekly['SV']}/2, oracle={oracle_count}/1, radar={radar_count}/1; "
            f"month SP={monthly['SP']}/2-4; {len(errors)} errors, {len(warnings)} warnings"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
