#!/usr/bin/env python3
"""Report and enforce the five-day editorial trend review cadence."""

from __future__ import annotations

import argparse
import json
from datetime import date

from almanac_common import REPORTS, parse_date_target


START = date(2026, 7, 17)
INTERVAL = 5


def is_due(day: date) -> bool:
    return day >= START and (day - START).days % INTERVAL == 0


def report_path(day: date):
    return REPORTS / "trends" / f"TREND-{day.isoformat()}.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    day = parse_date_target(args.target)
    path = report_path(day)
    result = {"date": day.isoformat(), "due": is_due(day), "exists": path.exists(), "path": str(path)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        state = "DUE" if result["due"] else "not due"
        evidence = "ready" if result["exists"] else "missing"
        print(f"TREND REVIEW: {state}; report {evidence}: {path}")
    return 1 if args.strict and result["due"] and not result["exists"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
