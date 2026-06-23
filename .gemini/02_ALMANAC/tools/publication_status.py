#!/usr/bin/env python3
"""Maintain the authoritative publishing-state registry."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone

from almanac_common import DATABASES, ROOT, iter_posts


REGISTRY = DATABASES / "PUBLICATION_REGISTRY.json"
EFFECTIVE_FROM = date(2026, 7, 21)
STATUSES = {
    "idea", "draft", "needs_factcheck", "needs_rewrite", "ready", "scheduled",
    "published", "corrected", "archived",
}
TRANSITIONS = {
    "idea": {"draft", "archived"},
    "draft": {"needs_factcheck", "needs_rewrite", "ready", "archived"},
    "needs_factcheck": {"draft", "ready", "archived"},
    "needs_rewrite": {"draft", "ready", "archived"},
    "ready": {"scheduled", "published", "archived"},
    "scheduled": {"ready", "published", "archived"},
    "published": {"corrected"},
    "corrected": {"corrected"},
    "archived": {"draft"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: str) -> str:
    cleaned = value.strip().lower().replace(" ", "_")
    aliases = {
        "готов": "ready", "готово": "ready", "готовый": "ready", "готова": "ready",
        "черновик": "draft", "archive": "archived", "needs_fact_check": "needs_factcheck",
    }
    return aliases.get(cleaned, cleaned or "draft")


def load() -> dict:
    if not REGISTRY.exists():
        return {"schema_version": 1, "posts": []}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    DATABASES.mkdir(parents=True, exist_ok=True)
    data["posts"] = sorted(data.get("posts", []), key=lambda item: (item.get("date", ""), item["post_id"]))
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync() -> dict:
    data = load()
    known = {item["post_id"]: item for item in data.get("posts", [])}
    seen: set[str] = set()
    for post in iter_posts(prefixes={"AL", "SV", "SP"}):
        seen.add(post.post_id)
        content_status = normalize(post.metadata.get("status", "draft"))
        if content_status not in STATUSES:
            content_status = "draft"
        entry = known.get(post.post_id)
        if entry is None:
            entry = {
                "post_id": post.post_id,
                "date": post.publication_date.isoformat(),
                "path": str(post.path.relative_to(ROOT)),
                "content_status": content_status,
                "publication_status": content_status,
                "scheduled_at": None,
                "published_at": None,
                "telegram_message_id": None,
                "channel": None,
                "corrected_at": None,
                "state_source": "content_import",
                "verified_against_telegram": False,
                "last_updated": now(),
            }
            data.setdefault("posts", []).append(entry)
            known[post.post_id] = entry
        else:
            entry.update(
                date=post.publication_date.isoformat(),
                path=str(post.path.relative_to(ROOT)),
                content_status=content_status,
            )
            entry.setdefault("state_source", "content_import")
            entry.setdefault("verified_against_telegram", False)
    for entry in data.get("posts", []):
        entry["orphaned"] = entry["post_id"] not in seen
    save(data)
    print(f"PUBLICATIONS: {len(data.get('posts', []))} records -> {REGISTRY}")
    return data


def set_status(args) -> int:
    data = sync()
    entries = {item["post_id"]: item for item in data["posts"]}
    if args.post_id not in entries:
        print(f"ERROR: unknown post_id `{args.post_id}`")
        return 1
    entry = entries[args.post_id]
    old = entry["publication_status"]
    new = args.status
    if new != old and new not in TRANSITIONS.get(old, set()) and not args.force:
        print(f"ERROR: transition {old} -> {new} is not allowed; use --force only for repair")
        return 1
    entry["publication_status"] = new
    if args.scheduled_at:
        entry["scheduled_at"] = args.scheduled_at
    if args.published_at:
        entry["published_at"] = args.published_at
    elif new == "published" and not entry.get("published_at"):
        entry["published_at"] = now()
    if args.telegram_message_id:
        entry["telegram_message_id"] = args.telegram_message_id
    if args.channel:
        entry["channel"] = args.channel
    if new == "corrected":
        entry["corrected_at"] = now()
    entry["state_source"] = "manual"
    if new in {"published", "corrected"}:
        entry["verified_against_telegram"] = bool(entry.get("telegram_message_id") and entry.get("channel"))
    entry["last_updated"] = now()
    save(data)
    print(f"PUBLICATION: {args.post_id}: {old} -> {new}")
    return 0


def audit(target: str | None, strict: bool) -> int:
    data = sync()
    entries = {item["post_id"]: item for item in data["posts"]}
    posts = iter_posts(target, prefixes={"AL", "SV", "SP"}) if target else iter_posts(prefixes={"AL", "SV", "SP"})
    errors: list[str] = []
    warnings: list[str] = []
    for entry in data.get("posts", []):
        if entry.get("orphaned"):
            warnings.append(f"publication record points to missing content: {entry['post_id']}")
    for post in posts:
        entry = entries.get(post.post_id)
        if not entry:
            errors.append(f"missing registry record: {post.post_id}")
            continue
        status = entry["publication_status"]
        if entry["content_status"] in {"published", "corrected"} and status not in {"published", "corrected"}:
            errors.append(f"content says published but registry says {status}: {post.post_id}")
        if status in {"scheduled", "published", "corrected"} and entry["content_status"] not in {
            "scheduled", "published", "corrected", "ready"
        }:
            warnings.append(f"queue state {status} conflicts with content state {entry['content_status']}: {post.post_id}")
        prospective = post.publication_date >= EFFECTIVE_FROM
        if prospective and status == "scheduled" and not entry.get("scheduled_at"):
            warnings.append(f"scheduled_at missing: {post.post_id}")
        if prospective and status in {"published", "corrected"}:
            for field in ("published_at", "telegram_message_id", "channel"):
                if not entry.get(field):
                    warnings.append(f"{field} missing for published post: {post.post_id}")
            if not entry.get("verified_against_telegram"):
                warnings.append(f"published state is not verified against Telegram: {post.post_id}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    print(f"PUBLICATION AUDIT: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors or (strict and warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sync")
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target", nargs="?")
    audit_parser.add_argument("--strict", action="store_true")
    setter = sub.add_parser("set")
    setter.add_argument("post_id")
    setter.add_argument("status", choices=sorted(STATUSES))
    setter.add_argument("--scheduled-at")
    setter.add_argument("--published-at")
    setter.add_argument("--telegram-message-id")
    setter.add_argument("--channel")
    setter.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "sync":
        sync()
        return 0
    if args.command == "audit":
        return audit(args.target, args.strict)
    return set_status(args)


if __name__ == "__main__":
    raise SystemExit(main())
