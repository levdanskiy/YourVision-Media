#!/usr/bin/env python3
"""Audit current Almanac posts for V4 voice, visual, and divination rules."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_almanac import (  # noqa: E402
    AL_NAME,
    CONTENT,
    READY_STATUSES,
    ROOT,
    body_text,
    file_date,
    prompt_text,
    rel,
    service_metadata,
)


REGIONAL_ANCHOR_PATTERNS = (
    re.compile(r"(?i)\b(у нас|у меня|здесь)\b.*\b(в стране|в регионе|в городе|в риге|в латвии)\b"),
    re.compile(r"(?i)\b(наш|наша|наше|нашего|нашем)\b.*\b(город|страна|регион|широта|климат|традиция)\b"),
    re.compile(r"(?i)\b(publication_timezone|timezone)\b.*\b(editorial|оптик|центр|голос|якор)\b"),
    re.compile(r"(?i)\b(riga|latvia|baltic|baltics)\b.*\b(default|home|anchor|lens|voice)\b"),
    re.compile(r"(?i)\b(рига|латвия|балтийск)\w*\b.*\b(по умолчанию|домашн|оптик|центр|голос|якор)\b"),
)

ENGAGEMENT_BAIT = (
    "напишите в комментариях",
    "пишите в комментариях",
    "делитесь в комментариях",
    "оставьте комментарий",
    "сохрани пост",
    "сохраните пост",
    "отметь друга",
    "отметьте друга",
    "поделись",
    "поделитесь",
    "как тебе",
    "согласны?",
)

WEAK_OPENINGS = (
    "сегодня мы поговорим",
    "в этом посте",
    "давайте поговорим",
    "поговорим о",
    "расскажем о",
)

VISUAL_CLICHES = (
    "mystical glow",
    "glowing aura",
    "fantasy",
    "magical",
    "ethereal",
    "cinematic",
    "dramatic lighting",
)

DIVINATION_FORBIDDEN = (
    "карты говорят",
    "карты советуют",
    "звезды советуют",
    "звёзды советуют",
    "вам выпадет",
    "судьба говорит",
    "таро предсказывает",
    "гороскоп предсказывает",
    "если вы овен",
    "если вы телец",
    "если вы близнецы",
    "если вы рак",
    "если вы лев",
    "если вы дева",
    "если вы весы",
    "если вы скорпион",
    "если вы стрелец",
    "если вы козерог",
    "если вы водолей",
    "если вы рыбы",
)


@dataclass
class Finding:
    severity: str
    path: Path
    message: str


def iter_scope(args: list[str]) -> list[Path]:
    if len(args) == 3:
        year, month, day = args
        return sorted((ROOT / "02_CONTENT" / year / month / day).glob("AL-*.md"))
    if len(args) == 2:
        year, month = args
        return sorted((ROOT / "02_CONTENT" / year / month).rglob("AL-*.md"))
    if len(args) == 0:
        return [
            path
            for path in sorted(CONTENT.rglob("AL-*.md"))
            if AL_NAME.match(path.name) and file_date(AL_NAME.match(path.name)) >= (2026, 5, 16)
        ]
    raise SystemExit("Usage: audit_style.py [YYYY MM [DD]]")


def first_body_line(body: str) -> str:
    for line in body.splitlines():
        clean = line.strip()
        if clean:
            return clean
    return ""


def contains_any(text: str, needles: tuple[str, ...]) -> str | None:
    lowered = text.lower()
    for needle in needles:
        if needle in lowered:
            return needle
    return None


def regional_anchor_hit(text: str) -> str | None:
    for pattern in REGIONAL_ANCHOR_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


def audit_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    match = AL_NAME.match(path.name)
    if not match:
        return findings

    text = path.read_text(encoding="utf-8")
    metadata = service_metadata(text)
    status = metadata.get("status", "")
    rubric = match.group("rubric")
    body = body_text(text)
    prompt = prompt_text(text)

    regional = regional_anchor_hit(text)
    if regional:
        findings.append(Finding("ERROR", path, f"regional anchor framing found: {regional}"))

    bait = contains_any(body, ENGAGEMENT_BAIT)
    if bait:
        findings.append(Finding("ERROR", path, f"engagement-bait phrase found: {bait}"))

    opening = contains_any(first_body_line(body), WEAK_OPENINGS)
    if opening:
        findings.append(Finding("WARN", path, f"weak opening phrase: {opening}"))

    if "**Prompt:**" in text and "**Visual Prompt:**" not in text:
        findings.append(Finding("WARN", path, "old Prompt label; use Visual Prompt"))

    if status in READY_STATUSES and "**Grade:**" not in text:
        findings.append(Finding("WARN", path, "ready post has no Grade block"))

    if status in READY_STATUSES and "**Visual Prompt:**" not in text:
        findings.append(Finding("WARN", path, "ready post should use Visual Prompt label"))

    if prompt:
        lower_prompt = prompt.lower()
        for required in ("no text", "no logos"):
            if required not in lower_prompt:
                findings.append(Finding("WARN", path, f"visual prompt missing '{required}'"))
        cliche = contains_any(prompt, VISUAL_CLICHES)
        if cliche:
            findings.append(Finding("WARN", path, f"visual prompt cliche found: {cliche}"))
        if re.search(r'(?i)\btext\s*["\']', prompt):
            findings.append(Finding("ERROR", path, "visual prompt asks for visible text"))

    if rubric == "DIVINATION":
        forbidden = contains_any(body, DIVINATION_FORBIDDEN)
        if forbidden:
            findings.append(Finding("ERROR", path, f"predictive divination language found: {forbidden}"))
        for required in ("истор", "визуаль", "практик"):
            if required not in body.lower():
                findings.append(Finding("WARN", path, f"DIVINATION body may miss required frame: {required}"))

    if re.search(r"(?im)^//\s*V3", text):
        findings.append(Finding("ERROR", path, "legacy V3 service marker found"))

    return findings


def main() -> int:
    paths = iter_scope(sys.argv[1:])
    findings: list[Finding] = []
    for path in paths:
        findings.extend(audit_file(path))

    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARN"]

    print("# Almanac style audit")
    print()
    print(f"- Files checked: {len(paths)}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if findings:
        print()
        for item in findings:
            print(f"{item.severity}: {rel(item.path)} - {item.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
