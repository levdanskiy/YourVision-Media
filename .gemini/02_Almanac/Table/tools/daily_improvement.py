#!/usr/bin/env python3
"""Create and validate the visible daily improvement record."""

from __future__ import annotations

import argparse
import re
from datetime import date

from almanac_common import REPORTS, parse_date_target


EFFECTIVE_FROM = date(2026, 7, 21)
VALID_STATUSES = {"applied", "deferred"}


def report_path(day: date):
    return REPORTS / "improvements" / f"IMPROVEMENT-{day.isoformat()}.md"


def template(day: date) -> str:
    return f"""# Daily Improvement - {day.isoformat()}

## Observation

What is limiting the channel, archive, workflow or reader experience today?

## Improvement

One concrete change. It may be small, medium or big.

- Size: small
- Area: workflow
- Status: proposed
- Applied in:
- Evidence:
- Review date:

## Visible Summary

- Changed today:
- Why it matters:
- Next signal to watch:
"""


def status(text: str) -> str:
    match = re.search(r"^- Status:\s*([a-z_]+)\s*$", text, re.I | re.M)
    return match.group(1).lower() if match else "missing"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    day = parse_date_target(args.target)
    path = report_path(day)
    if args.init and not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template(day), encoding="utf-8")
        print(f"CREATED: {path}")

    required = day >= EFFECTIVE_FROM
    if not path.exists():
        print(f"DAILY IMPROVEMENT: {'required' if required else 'not required'}; missing: {path}")
        return 1 if args.strict and required else 0
    current_status = status(path.read_text(encoding="utf-8"))
    print(f"DAILY IMPROVEMENT: status={current_status}; {path}")
    if args.strict and required and current_status not in VALID_STATUSES:
        print("ERROR: daily improvement must be `applied` or explicitly `deferred`.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
