#!/usr/bin/env python3
"""Shared archive parsing for Almanac automation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "02_CONTENT"
REPORTS = ROOT / "03_REPORTS"
DATABASES = ROOT / "04_DATABASES"

POST_NAME = re.compile(
    r"^(?P<prefix>AL|SV|SP)-(?P<day>\d{2})\.(?P<month>\d{2})-"
    r"(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<tail>.+)\.md$"
)
WORD = re.compile(r"[\w-]+", re.UNICODE)


@dataclass(frozen=True)
class Post:
    path: Path
    prefix: str
    publication_date: date
    slot: str
    rubric: str
    metadata: dict[str, str]
    text: str

    @property
    def post_id(self) -> str:
        return self.metadata.get("post_id") or self.path.stem

    @property
    def title(self) -> str:
        return self.metadata.get("title", "")

    @property
    def slug(self) -> str:
        return self.metadata.get("slug", "")

    @property
    def canon_id(self) -> str:
        return self.metadata.get("canon_id", "")

    @property
    def angle_id(self) -> str:
        return self.metadata.get("angle_id", "")

    @property
    def series_id(self) -> str:
        return self.metadata.get("series_id", "")


def parse_frontmatter(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    if text.startswith("---\n"):
        for line in text.splitlines()[1:]:
            if line.strip() == "---":
                break
            if ":" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split(":", 1)
            metadata[key.strip().lower()] = value.strip().strip('"').strip("'")

    comment_keys = {
        "ид-поста": "post_id",
        "тема": "title",
        "статус": "status",
        "рубрика": "rubric",
        "cultural_zone": "cultural_zone",
        "secondary_zones": "secondary_zones",
        "coverage_axes": "coverage_axes",
        "coverage_axis": "coverage_axis",
        "source_types": "source_types",
        "source_type": "source_type",
        "canon_id": "canon_id",
        "angle_id": "angle_id",
        "series_id": "series_id",
        "continuity_notes": "continuity_notes",
    }
    for line in text.splitlines()[:80]:
        if not line.startswith("//") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        normalized = comment_keys.get(key.strip().lower())
        if normalized:
            metadata.setdefault(normalized, value.strip().lstrip("#"))
    return metadata


def rubric_from_name(tail: str) -> str:
    return tail.split("-", 1)[0].upper()


def load_post(path: Path) -> Post | None:
    match = POST_NAME.match(path.name)
    if not match:
        return None
    try:
        year = int(path.parts[path.parts.index("02_CONTENT") + 1])
    except (ValueError, IndexError):
        return None
    publication_date = date(year, int(match.group("month")), int(match.group("day")))
    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    rubric = metadata.get("rubric", rubric_from_name(match.group("tail"))).lstrip("#").upper()
    return Post(
        path=path,
        prefix=match.group("prefix"),
        publication_date=publication_date,
        slot=f"{match.group('hour')}:{match.group('minute')}",
        rubric=rubric,
        metadata=metadata,
        text=text,
    )


def iter_posts(target: str | None = None, prefixes: set[str] | None = None) -> list[Post]:
    prefixes = prefixes or {"AL", "SV", "SP"}
    paths: Iterable[Path]
    if target and len(target) == 10:
        year, month, day = target.split("-")
        base = CONTENT / year / month / day
        paths = base.glob("*.md") if base.exists() else []
    elif target and len(target) == 7:
        year, month = target.split("-")
        base = CONTENT / year / month
        paths = base.rglob("*.md") if base.exists() else []
    else:
        paths = CONTENT.rglob("*.md")
    posts = [post for path in sorted(paths) if (post := load_post(path)) and post.prefix in prefixes]
    return posts


def parse_date_target(target: str) -> date:
    return date.fromisoformat(target)


def slots_for(day: date) -> tuple[str, str, str]:
    if day >= date(2026, 7, 17):
        return ("09:04", "15:04", "21:04")
    return ("10:04", "15:04", "18:02")


def split_values(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,;|]", value) if part.strip()]


def normalized_words(value: str) -> set[str]:
    return {word.lower() for word in WORD.findall(value) if len(word) > 2}


def visual_prompt(text: str) -> str:
    match = re.search(r"\*\*Visual Prompt:\*\*\s*(.+?)(?:\n\n|\Z)", text, re.S | re.I)
    return " ".join(match.group(1).split()) if match else ""
