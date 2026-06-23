#!/usr/bin/env python3
"""Index and validate real visual assets, not only prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import struct
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from almanac_common import DATABASES, ROOT, iter_posts
from publication_status import load as load_publications, sync as sync_publications


ASSETS_ROOT = ROOT / "03_ASSETS"
REGISTRY = DATABASES / "ASSET_REGISTRY.json"
EFFECTIVE_FROM = date(2026, 7, 21)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
STATUSES = {"discovered", "generated", "approved", "used", "rejected"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def image_size(path: Path) -> tuple[int | None, int | None]:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 9 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            marker = data[offset + 1]
            offset += 2
            if marker in {0xD8, 0xD9}:
                continue
            if offset + 2 > len(data):
                break
            length = int.from_bytes(data[offset:offset + 2], "big")
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB}:
                return int.from_bytes(data[offset + 5:offset + 7], "big"), int.from_bytes(data[offset + 3:offset + 5], "big")
            offset += max(length, 2)
    return None, None


def load() -> dict:
    if not REGISTRY.exists():
        return {"schema_version": 1, "assets": []}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    data["assets"] = sorted(data.get("assets", []), key=lambda item: item["path"])
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync() -> dict:
    data = load()
    by_path = {item["path"]: item for item in data.get("assets", [])}
    post_ids = {post.post_id for post in iter_posts(prefixes={"AL", "SV", "SP"})}
    seen: set[str] = set()
    for path in sorted(ASSETS_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative = str(path.relative_to(ROOT))
        seen.add(relative)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        width, height = image_size(path)
        entry = by_path.get(relative)
        if entry is None:
            matched_id = path.stem if path.stem in post_ids else None
            entry = {
                "asset_id": f"asset-{digest[:16]}",
                "path": relative,
                "kind": "post" if matched_id else "branding",
                "post_id": matched_id,
                "status": "discovered",
                "alt": "",
                "rights": "",
                "source": "",
                "sha256": digest,
                "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "width": width,
                "height": height,
                "last_updated": now(),
            }
            data.setdefault("assets", []).append(entry)
            by_path[relative] = entry
        else:
            entry.update(sha256=digest, width=width, height=height)
    for entry in data.get("assets", []):
        entry["missing"] = entry["path"] not in seen
    save(data)
    print(f"ASSETS: {len(data.get('assets', []))} records -> {REGISTRY}")
    return data


def register(args) -> int:
    path = Path(args.path).expanduser().resolve()
    try:
        path.relative_to(ASSETS_ROOT)
        relative = str(path.relative_to(ROOT))
    except ValueError:
        print("ERROR: asset must live inside 03_ASSETS")
        return 1
    if not path.exists():
        print(f"ERROR: asset does not exist: {path}")
        return 1
    data = sync()
    entry = next((item for item in data["assets"] if item["path"] == relative), None)
    if not entry:
        print("ERROR: unsupported asset type")
        return 1
    entry.update(
        post_id=args.post_id or entry.get("post_id"),
        kind="post" if args.post_id else entry.get("kind", "branding"),
        status=args.status,
        alt=args.alt or entry.get("alt", ""),
        rights=args.rights or entry.get("rights", ""),
        source=args.source or entry.get("source", ""),
        last_updated=now(),
    )
    save(data)
    print(f"ASSET REGISTERED: {relative} -> {entry.get('post_id') or entry['kind']} [{entry['status']}]")
    return 0


def audit(target: str | None, strict: bool) -> int:
    data = sync()
    sync_publications()
    publication_entries = {item["post_id"]: item for item in load_publications().get("posts", [])}
    assets_by_post: dict[str, list[dict]] = defaultdict(list)
    hashes: dict[str, list[dict]] = defaultdict(list)
    for asset in data.get("assets", []):
        if asset.get("post_id"):
            assets_by_post[asset["post_id"]].append(asset)
            hashes[asset.get("sha256", "")].append(asset)
    posts = iter_posts(target, prefixes={"AL", "SV", "SP"}) if target else iter_posts(prefixes={"AL", "SV", "SP"})
    errors: list[str] = []
    warnings: list[str] = []
    for post in posts:
        publication_state = publication_entries.get(post.post_id, {}).get("publication_status", "ready")
        image_state = post.metadata.get("image_status", "").lower()
        required = post.publication_date >= EFFECTIVE_FROM and publication_state in {"scheduled", "published", "corrected"}
        candidates = [asset for asset in assets_by_post.get(post.post_id, []) if not asset.get("missing")]
        if required and not candidates:
            warnings.append(f"no registered image for {publication_state} post: {post.post_id}")
            continue
        for asset in candidates:
            if asset["status"] in {"approved", "used"} or required or image_state in {"approved", "used"}:
                if not asset.get("alt"):
                    warnings.append(f"ALT missing: {asset['path']}")
                if not asset.get("rights"):
                    warnings.append(f"rights missing: {asset['path']}")
                if not asset.get("width") or not asset.get("height"):
                    warnings.append(f"image dimensions unavailable: {asset['path']}")
            if publication_state in {"scheduled", "published", "corrected"} and asset["status"] not in {"approved", "used"}:
                warnings.append(f"asset is not approved: {post.post_id} -> {asset['status']}")
            if publication_state in {"published", "corrected"} and asset["status"] != "used":
                warnings.append(f"published post asset is not marked used: {post.post_id}")
    for digest, assets in hashes.items():
        if digest and len(assets) > 1:
            warnings.append("exact duplicate image: " + ", ".join(asset["path"] for asset in assets))
    for asset in data.get("assets", []):
        if asset.get("missing"):
            errors.append(f"registered asset missing from disk: {asset['path']}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(f"ASSET AUDIT: {len(errors)} errors, {len(set(warnings))} warnings")
    return 1 if errors or (strict and warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sync")
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target", nargs="?")
    audit_parser.add_argument("--strict", action="store_true")
    register_parser = sub.add_parser("register")
    register_parser.add_argument("path")
    register_parser.add_argument("--post-id")
    register_parser.add_argument("--status", choices=sorted(STATUSES), default="generated")
    register_parser.add_argument("--alt")
    register_parser.add_argument("--rights")
    register_parser.add_argument("--source")
    args = parser.parse_args()
    if args.command == "sync":
        sync()
        return 0
    if args.command == "audit":
        return audit(args.target, args.strict)
    return register(args)


if __name__ == "__main__":
    raise SystemExit(main())
