#!/usr/bin/env python3
"""Record and resolve editorial incidents and public corrections."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone

from almanac_common import DATABASES, REPORTS, iter_posts
from publication_status import load as load_publications, save as save_publications, sync as sync_publications


REGISTRY = DATABASES / "EDITORIAL_INCIDENTS.json"
CORRECTIONS = REPORTS / "CORRECTIONS.md"
SEVERITIES = {"low", "medium", "high", "critical"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {"schema_version": 1, "incidents": []}


def save(data: dict) -> None:
    data["incidents"] = sorted(data.get("incidents", []), key=lambda item: item["incident_id"])
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add(args) -> int:
    if args.post_id not in {post.post_id for post in iter_posts(prefixes={"AL", "SV", "SP"})}:
        print(f"ERROR: unknown post_id `{args.post_id}`")
        return 1
    data = load()
    sequence = len(data.get("incidents", [])) + 1
    incident_id = f"INC-{date.today().isoformat()}-{sequence:03d}"
    data.setdefault("incidents", []).append(
        {
            "incident_id": incident_id,
            "post_id": args.post_id,
            "severity": args.severity,
            "issue": args.issue,
            "detected_at": args.detected_at or now(),
            "public_correction_required": args.public_correction == "yes",
            "status": "open",
            "correction": "",
            "public_notice": "",
            "resolved_at": None,
        }
    )
    save(data)
    print(f"INCIDENT OPENED: {incident_id}")
    return 0


def resolve(args) -> int:
    data = load()
    entry = next((item for item in data.get("incidents", []) if item["incident_id"] == args.incident_id), None)
    if not entry:
        print(f"ERROR: unknown incident `{args.incident_id}`")
        return 1
    if entry.get("public_correction_required") and not args.public_notice:
        print("ERROR: public notice is required for this incident")
        return 1
    entry.update(
        status="resolved",
        correction=args.correction,
        public_notice=args.public_notice or "not required",
        resolved_at=now(),
    )
    save(data)
    with CORRECTIONS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {date.today().isoformat()} - {entry['post_id']}\n\n"
            f"- Incident: `{entry['incident_id']}`\n"
            f"- Issue: {entry['issue']}\n"
            f"- Correction: {args.correction}\n"
            f"- Public notice: {args.public_notice or 'not required'}\n"
        )
    sync_publications()
    publications = load_publications()
    publication = next((item for item in publications.get("posts", []) if item["post_id"] == entry["post_id"]), None)
    if publication and publication.get("publication_status") in {"published", "corrected"}:
        publication["publication_status"] = "corrected"
        publication["corrected_at"] = now()
        publication["last_updated"] = now()
        save_publications(publications)
    print(f"INCIDENT RESOLVED: {args.incident_id}")
    return 0


def audit(target: str | None, strict: bool) -> int:
    data = load()
    target_ids = {post.post_id for post in iter_posts(target, prefixes={"AL", "SV", "SP"})} if target else None
    errors: list[str] = []
    warnings: list[str] = []
    for item in data.get("incidents", []):
        if item.get("severity") not in SEVERITIES:
            errors.append(f"invalid severity: {item.get('incident_id', '?')}")
        if item.get("status") == "open" and item.get("severity") in {"high", "critical"}:
            if item.get("severity") == "critical" or target_ids is None or item.get("post_id") in target_ids:
                warnings.append(f"open {item['severity']} incident: {item['incident_id']} / {item['post_id']}")
        if item.get("status") == "resolved" and not item.get("correction"):
            errors.append(f"resolved incident lacks correction: {item.get('incident_id', '?')}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    open_count = sum(1 for item in data.get("incidents", []) if item.get("status") == "open")
    print(f"INCIDENT AUDIT: open={open_count}; {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors or (strict and warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target", nargs="?")
    audit_parser.add_argument("--strict", action="store_true")
    add_parser = sub.add_parser("add")
    add_parser.add_argument("post_id")
    add_parser.add_argument("--severity", choices=sorted(SEVERITIES), required=True)
    add_parser.add_argument("--issue", required=True)
    add_parser.add_argument("--public-correction", choices=["yes", "no"], required=True)
    add_parser.add_argument("--detected-at")
    resolve_parser = sub.add_parser("resolve")
    resolve_parser.add_argument("incident_id")
    resolve_parser.add_argument("--correction", required=True)
    resolve_parser.add_argument("--public-notice")
    args = parser.parse_args()
    if args.command == "audit":
        return audit(args.target, args.strict)
    if args.command == "add":
        return add(args)
    return resolve(args)


if __name__ == "__main__":
    raise SystemExit(main())
