#!/usr/bin/env python3
"""Maintain claim-to-source evidence cards for publishable posts."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone

from almanac_common import DATABASES, iter_posts
from publication_status import load as load_publications, sync as sync_publications


REGISTRY = DATABASES / "EVIDENCE_REGISTRY.json"
EFFECTIVE_FROM = date(2026, 7, 21)
TRUST_LEVELS = {"A", "B", "C", "D"}
EVIDENCE_TYPES = {
    "primary_text", "critical_edition", "institutional_record", "scholarship", "dataset",
    "ethnography", "reference_work", "oral_history", "journalism", "discovery_only",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load() -> dict:
    if not REGISTRY.exists():
        return {"schema_version": 1, "posts": []}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    data["posts"] = sorted(data.get("posts", []), key=lambda item: item["post_id"])
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def known_post_ids() -> set[str]:
    return {post.post_id for post in iter_posts(prefixes={"AL", "SV", "SP"})}


def get_or_create(data: dict, post_id: str) -> dict:
    entry = next((item for item in data.get("posts", []) if item["post_id"] == post_id), None)
    if entry is None:
        entry = {
            "post_id": post_id,
            "review_outcome": "pending",
            "reviewer_note": "",
            "checked_at": None,
            "claims": [],
        }
        data.setdefault("posts", []).append(entry)
    return entry


def add_claim(args) -> int:
    if args.post_id not in known_post_ids():
        print(f"ERROR: unknown post_id `{args.post_id}`")
        return 1
    data = load()
    entry = get_or_create(data, args.post_id)
    claim_id = f"{args.post_id}:claim:{len(entry['claims']) + 1}"
    entry["claims"].append(
        {
            "claim_id": claim_id,
            "claim": args.claim,
            "source_title": args.source_title,
            "url": args.url or "",
            "local_path": args.local_path or "",
            "accessed_at": args.accessed_at or date.today().isoformat(),
            "trust_level": args.trust_level,
            "evidence_type": args.evidence_type,
            "locator": args.locator or "",
            "support": args.support,
            "notes": args.notes or "",
        }
    )
    entry["review_outcome"] = "evidenced"
    entry["checked_at"] = now()
    save(data)
    print(f"EVIDENCE ADDED: {claim_id}")
    return 0


def review(args) -> int:
    if args.post_id not in known_post_ids():
        print(f"ERROR: unknown post_id `{args.post_id}`")
        return 1
    if args.outcome == "no_strong_claims" and len(args.note.strip()) < 20:
        print("ERROR: no_strong_claims requires a concrete reviewer note")
        return 1
    data = load()
    entry = get_or_create(data, args.post_id)
    entry.update(review_outcome=args.outcome, reviewer_note=args.note, checked_at=now())
    save(data)
    print(f"EVIDENCE REVIEW: {args.post_id} -> {args.outcome}")
    return 0


def audit(target: str | None, strict: bool) -> int:
    data = load()
    entries = {item["post_id"]: item for item in data.get("posts", [])}
    sync_publications()
    states = {item["post_id"]: item["publication_status"] for item in load_publications().get("posts", [])}
    posts = iter_posts(target, prefixes={"AL", "SV", "SP"}) if target else iter_posts(prefixes={"AL", "SV", "SP"})
    errors: list[str] = []
    warnings: list[str] = []
    for post in posts:
        state = states.get(post.post_id, "draft")
        required = post.publication_date >= EFFECTIVE_FROM and state in {"ready", "scheduled", "published", "corrected"}
        entry = entries.get(post.post_id)
        if required and not entry:
            warnings.append(f"evidence review missing: {post.post_id}")
            continue
        if not entry:
            continue
        outcome = entry.get("review_outcome", "pending")
        if required and outcome == "pending":
            warnings.append(f"evidence review pending: {post.post_id}")
        if outcome == "no_strong_claims" and len(entry.get("reviewer_note", "").strip()) < 20:
            warnings.append(f"weak no-strong-claims note: {post.post_id}")
        if outcome == "evidenced" and not entry.get("claims"):
            errors.append(f"evidenced post has no claim cards: {post.post_id}")
        for claim in entry.get("claims", []):
            for field in ("claim", "source_title", "accessed_at", "trust_level", "evidence_type", "support"):
                if not claim.get(field):
                    errors.append(f"claim `{claim.get('claim_id', '?')}` missing {field}")
            if claim.get("trust_level") not in TRUST_LEVELS:
                errors.append(f"invalid trust level: {claim.get('claim_id', '?')}")
            if claim.get("evidence_type") not in EVIDENCE_TYPES:
                errors.append(f"invalid evidence type: {claim.get('claim_id', '?')}")
            if not claim.get("url") and not claim.get("local_path"):
                warnings.append(f"claim has no URL or local path: {claim.get('claim_id', '?')}")
    for message in sorted(set(errors)):
        print(f"ERROR: {message}")
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(f"EVIDENCE AUDIT: {len(set(errors))} errors, {len(set(warnings))} warnings")
    return 1 if errors or (strict and warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target", nargs="?")
    audit_parser.add_argument("--strict", action="store_true")
    claim = sub.add_parser("add")
    claim.add_argument("post_id")
    claim.add_argument("--claim", required=True)
    claim.add_argument("--source-title", required=True)
    claim.add_argument("--url")
    claim.add_argument("--local-path")
    claim.add_argument("--accessed-at")
    claim.add_argument("--trust-level", choices=sorted(TRUST_LEVELS), required=True)
    claim.add_argument("--evidence-type", choices=sorted(EVIDENCE_TYPES), required=True)
    claim.add_argument("--locator")
    claim.add_argument("--support", required=True)
    claim.add_argument("--notes")
    review_parser = sub.add_parser("review")
    review_parser.add_argument("post_id")
    review_parser.add_argument("--outcome", choices=["evidenced", "no_strong_claims"], required=True)
    review_parser.add_argument("--note", required=True)
    args = parser.parse_args()
    if args.command == "init":
        save(load())
        print(f"EVIDENCE: initialized {REGISTRY}")
        return 0
    if args.command == "audit":
        return audit(args.target, args.strict)
    if args.command == "add":
        return add_claim(args)
    return review(args)


if __name__ == "__main__":
    raise SystemExit(main())
