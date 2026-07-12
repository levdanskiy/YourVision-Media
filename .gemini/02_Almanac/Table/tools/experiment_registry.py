#!/usr/bin/env python3
"""Maintain hypotheses, measurements and adoption decisions."""

from __future__ import annotations

import argparse
import json
from datetime import date

from almanac_common import DATABASES


REGISTRY = DATABASES / "EXPERIMENT_REGISTRY.json"
STATUSES = {"planned", "running", "adopted", "revised", "dropped"}
SIZES = {"small", "medium", "big"}


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {"schema_version": 1, "experiments": []}


def save(data: dict) -> None:
    data["experiments"] = sorted(data.get("experiments", []), key=lambda item: item["experiment_id"])
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add(args) -> int:
    data = load()
    if any(item["experiment_id"] == args.experiment_id for item in data["experiments"]):
        print(f"ERROR: duplicate experiment_id `{args.experiment_id}`")
        return 1
    data["experiments"].append(
        {
            "experiment_id": args.experiment_id,
            "title": args.title,
            "hypothesis": args.hypothesis,
            "change": args.change,
            "size": args.size,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "metric": args.metric,
            "baseline": args.baseline,
            "target": args.target,
            "status": "planned",
            "related_posts": [],
            "result": "",
            "decision_note": "",
        }
    )
    save(data)
    print(f"EXPERIMENT ADDED: {args.experiment_id}")
    return 0


def update(args) -> int:
    data = load()
    entry = next((item for item in data["experiments"] if item["experiment_id"] == args.experiment_id), None)
    if not entry:
        print(f"ERROR: unknown experiment `{args.experiment_id}`")
        return 1
    if args.status in {"adopted", "revised", "dropped"} and (not args.result or not args.decision_note):
        print("ERROR: closed experiment requires --result and --decision-note")
        return 1
    entry["status"] = args.status
    if args.result:
        entry["result"] = args.result
    if args.decision_note:
        entry["decision_note"] = args.decision_note
    if args.related_post:
        entry.setdefault("related_posts", []).append(args.related_post)
        entry["related_posts"] = sorted(set(entry["related_posts"]))
    save(data)
    print(f"EXPERIMENT: {args.experiment_id} -> {args.status}")
    return 0


def audit(target: str, strict: bool) -> int:
    day = date.fromisoformat(target)
    data = load()
    errors: list[str] = []
    warnings: list[str] = []
    required = ("title", "hypothesis", "change", "size", "start_date", "end_date", "metric", "baseline", "target", "status")
    for item in data.get("experiments", []):
        for field in required:
            if not item.get(field):
                errors.append(f"{item.get('experiment_id', '?')} missing {field}")
        if item.get("size") not in SIZES:
            errors.append(f"invalid size: {item.get('experiment_id', '?')}")
        if item.get("status") not in STATUSES:
            errors.append(f"invalid status: {item.get('experiment_id', '?')}")
        if item.get("status") in {"planned", "running"} and item.get("end_date") and date.fromisoformat(item["end_date"]) <= day:
            warnings.append(f"experiment review due: {item['experiment_id']} ends {item['end_date']}")
        if item.get("status") in {"adopted", "revised", "dropped"} and not item.get("decision_note"):
            errors.append(f"closed experiment lacks decision note: {item['experiment_id']}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    active = sum(1 for item in data.get("experiments", []) if item.get("status") == "running")
    print(f"EXPERIMENT AUDIT: active={active}; {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors or (strict and warnings) else 0


def list_items() -> int:
    for item in load().get("experiments", []):
        print(f"- {item['experiment_id']} [{item['status']}] {item['title']} | review {item['end_date']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target")
    audit_parser.add_argument("--strict", action="store_true")
    add_parser = sub.add_parser("add")
    add_parser.add_argument("experiment_id")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--hypothesis", required=True)
    add_parser.add_argument("--change", required=True)
    add_parser.add_argument("--size", choices=sorted(SIZES), required=True)
    add_parser.add_argument("--start-date", required=True)
    add_parser.add_argument("--end-date", required=True)
    add_parser.add_argument("--metric", required=True)
    add_parser.add_argument("--baseline", required=True)
    add_parser.add_argument("--target", required=True)
    update_parser = sub.add_parser("set")
    update_parser.add_argument("experiment_id")
    update_parser.add_argument("status", choices=sorted(STATUSES))
    update_parser.add_argument("--result")
    update_parser.add_argument("--decision-note")
    update_parser.add_argument("--related-post")
    args = parser.parse_args()
    if args.command == "list":
        return list_items()
    if args.command == "audit":
        return audit(args.target, args.strict)
    if args.command == "add":
        return add(args)
    return update(args)


if __name__ == "__main__":
    raise SystemExit(main())
