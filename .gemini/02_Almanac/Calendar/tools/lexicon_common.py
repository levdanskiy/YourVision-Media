"""Common utilities for LEXICON tools."""
from __future__ import annotations

import re
from pathlib import Path
from datetime import date
from collections import namedtuple

ROOT = Path(__file__).resolve().parent.parent
DATABASES = ROOT / "04_DATABASES"
REPORTS = ROOT / "03_REPORTS"
CONTENT = ROOT / "02_CONTENT"

Post = namedtuple("Post", ["post_id", "publication_date", "path", "metadata", "prefix", "rubric", "slot"])

LX_NAME = re.compile(
    r"^(?:LX|AL)-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<slot>[A-Z]+)-?.*\.md$"
)

SLOT_TIME_MAP = {
    "08": "AURORA",
    "11": "ANIMA",
    "17": "LOCUS",
    "23": "MYTHOS",
}

SLOT_RUBRICS = {
    "AURORA": {"OMENS", "DIVINATION", "FORECAST", "ASTROLOGY", "FRAGMENT"},
    "ANIMA": {"BESTIARY", "CRYPTID", "ARCHETYPE", "PERSONAE", "PANTHEON", "DEITIES", "SPIRIT", "GUARDIAN", "HERITAGE", "FOLK"},
    "LOCUS": {"LOCUS", "SACRED_GEO", "ARTIFACT", "SYMBOL", "PRAXIS", "MAGIC", "BOUNDARY", "CROSSROAD", "HEARTH", "CRAFT", "BOTANICA"},
    "MYTHOS": {"MYTHOS", "MORPHOLOGY", "VERBUM", "ETYMOLOGY", "NEOMYTH", "URBAN", "CHRONOS", "CYCLES", "CALENDAR", "GUIDE", "SOURCE", "LISTS"},
}

ALL_RUBRICS = set()
for rubrics in SLOT_RUBRICS.values():
    ALL_RUBRICS |= rubrics

SLOT_TIMES = {
    "AURORA": "11:45",
    "ANIMA": "15:15",
    "LOCUS": "17:15",
    "MYTHOS": "20:15",
}


def parse_date_target(target: str) -> date:
    return date.fromisoformat(target)


def split_values(val):
    if not val:
        return []
    return [x.strip() for x in val.split(",") if x.strip()]


def parse_lx_header(text: str) -> dict[str, str]:
    """Parse // KEY: VALUE header lines from LX post."""
    meta = {}
    for line in text.splitlines()[:20]:
        if not line.startswith("//"):
            continue
        body = line[2:].strip()
        if ":" not in body:
            continue
        key, value = body.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def parse_rubric_from_text(text: str) -> str | None:
    """Extract #RUBRIC from the post body (first heading line)."""
    for line in text.splitlines():
        m = re.search(r"#([A-Z][A-Z_]+)", line)
        if m:
            return m.group(1)
    return None


def iter_all_posts(year: int | None = None, month: int | None = None) -> list[Post]:
    """Iterate over all LX posts, optionally filtered by year/month."""
    if not CONTENT.exists():
        return []
    posts = []
    search_pattern = "**/*.md"
    for path in sorted(CONTENT.rglob(search_pattern)):
        m = LX_NAME.match(path.name)
        if not m:
            continue
        day = int(m.group("day"))
        mo = int(m.group("month"))
        yr = 2026  # all content is 2026
        if year and yr != year:
            continue
        if month and mo != month:
            continue
        slot_name = m.group("slot")
        text = path.read_text(encoding="utf-8")
        header = parse_lx_header(text)
        rubric = parse_rubric_from_text(text)
        if not rubric:
            rubric = slot_name
        pub_date = date(yr, mo, day)
        posts.append(Post(
            post_id=path.stem,
            publication_date=pub_date,
            path=path,
            metadata=header,
            prefix="LX",
            rubric=rubric,
            slot=slot_name,
        ))
    return posts


def iter_posts(month_prefix: str | None = None, prefixes: set[str] | None = None) -> list[Post]:
    """Backwards-compatible wrapper. If month_prefix like '2026-07', filters."""
    if month_prefix and "-" in month_prefix:
        y, m = month_prefix.split("-", 1)
        return iter_all_posts(year=int(y), month=int(m))
    return iter_all_posts()
