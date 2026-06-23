#!/usr/bin/env python3
"""Append a Telegram post measurement to the editorial analytics ledger."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone

from almanac_common import REPORTS


FIELDS = [
    "captured_at", "post_id", "views", "subscribers", "reactions", "forwards", "comments",
    "reach_rate", "engagement_rate", "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_id")
    parser.add_argument("--views", type=int, required=True)
    parser.add_argument("--subscribers", type=int, required=True)
    parser.add_argument("--reactions", type=int, default=0)
    parser.add_argument("--forwards", type=int, default=0)
    parser.add_argument("--comments", type=int, default=0)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    reach = args.views / args.subscribers * 100 if args.subscribers else 0
    engagement = (args.reactions + args.forwards + args.comments) / max(1, args.views) * 100
    row = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "post_id": args.post_id,
        "views": args.views,
        "subscribers": args.subscribers,
        "reactions": args.reactions,
        "forwards": args.forwards,
        "comments": args.comments,
        "reach_rate": f"{reach:.2f}",
        "engagement_rate": f"{engagement:.2f}",
        "notes": args.notes,
    }
    path = REPORTS / "analytics" / "post_metrics.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"METRICS: reach={reach:.2f}% engagement={engagement:.2f}% -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
