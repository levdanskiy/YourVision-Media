#!/usr/bin/env python3
"""Generate an editorial rotation/status report for an Almanac month."""

from __future__ import annotations

import calendar
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "02_CONTENT" / "2026"
REPORTS = ROOT / "03_REPORTS"

AL_NAME = re.compile(
    r"^AL-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rubric>[A-Z]+)-?.*\.md$"
)
SERVICE_NAME = re.compile(
    r"^(?P<prefix>SV|SP)-(?P<day>\d{2})\.(?P<month>\d{2})-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<rest>.+)\.md$"
)

THEME_BY_SLOT = {
    "09:04": "morning_myth",
    "10:04": "morning_myth",
    "15:04": "food",
    "18:02": "evening_calendar",
    "21:04": "evening_calendar",
}

THEME_LABELS = {
    "morning_myth": "09:04 myth/source/omens/dossier",
    "food": "15:04 food",
    "evening_calendar": "21:04 calendar/ritual/time",
    "other": "other",
}

SWEET = {"CAKES", "BUNS", "PATISSERIE", "DESSERTS", "SWEETS"}
SAVORY_BAKE = {"BREAD", "FLATBREAD", "PIES"}
BROAD_FOOD = {
    "FERMENT",
    "PRESERVE",
    "SOUP",
    "CONDIMENTS",
    "RECIPE",
    "FOODWAYS",
    "PANTRY",
    "DRINKS",
    "TOOLS",
    "WORKFLOW",
    "LISTS",
}

MORNING_PRIORITY = [
    "PERSONAE",
    "BESTIARY",
    "OBJECTS",
    "OMENS",
    "DIVINATION",
    "ETYMON",
    "PROSE",
]
FOOD_PRIORITY = [
    "FERMENT",
    "PRESERVE",
    "SOUP",
    "CONDIMENTS",
    "DRINKS",
    "TOOLS",
    "FOODWAYS",
    "BREAD",
    "FLATBREAD",
    "PIES",
    "DESSERTS",
    "SWEETS",
]
EVENING_PRIORITY = ["FEAST", "RITES", "CYCLES", "MODERN", "HERITAGE", "CALENDAR", "WHEEL"]

VALID_ZONES = {
    "Africa",
    "African Diaspora",
    "Indigenous Americas",
    "Latin America",
    "North America",
    "East Asia",
    "South Asia",
    "Southeast Asia",
    "Central Asia",
    "West Asia",
    "Oceania",
    "Europe",
    "Arctic North",
    "Island Cultures",
    "Global Modern",
    "Cross-Cultural",
}
REQUIRED_ZONE_GROUPS = [
    ("Africa / African Diaspora", {"Africa", "African Diaspora"}),
    ("Indigenous Americas", {"Indigenous Americas"}),
    ("Oceania / Island Cultures", {"Oceania", "Island Cultures"}),
    ("South Asia / Southeast Asia", {"South Asia", "Southeast Asia"}),
    ("Global Modern", {"Global Modern"}),
]
TREND_REVIEW_START = date(2026, 7, 17)


@dataclass(frozen=True)
class Post:
    path: Path
    day: int
    slot: str
    rubric: str
    status: str
    zone: str
    axis: str
    source_type: str


def simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    metadata: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line == "---":
            break
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"').strip("'")
    return metadata


def service_metadata(text: str) -> dict[str, str]:
    metadata = simple_frontmatter(text)
    for line in text.splitlines()[:60]:
        if not line.startswith("//"):
            continue
        body = line[2:].strip()
        if ":" not in body:
            continue
        key, value = body.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key in {
            "status",
            "статус",
            "cultural_zone",
            "coverage_axis",
            "source_type",
            "secondary_zones",
        }:
            metadata.setdefault("status" if key == "статус" else key, value)
    return metadata


def month_dir(year: int, month: int) -> Path:
    return CONTENT / f"{month:02d}" if CONTENT.name == f"{year}" else CONTENT / f"{month:02d}"


def load_posts(year: int, month: int) -> list[Post]:
    base = CONTENT / f"{month:02d}"
    if not base.exists():
        raise FileNotFoundError(f"Month directory not found: {base}")
    posts: list[Post] = []
    for path in sorted(base.rglob("AL-*.md")):
        match = AL_NAME.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8")
        metadata = service_metadata(text)
        day = int(match.group("day"))
        slot = f"{match.group('hour')}:{match.group('minute')}"
        posts.append(
            Post(
                path=path,
                day=day,
                slot=slot,
                rubric=match.group("rubric"),
                status=metadata.get("status", ""),
                zone=metadata.get("cultural_zone", ""),
                axis=metadata.get("coverage_axis", ""),
                source_type=metadata.get("source_type", ""),
            )
        )
    return posts


def load_services(year: int, month: int) -> list[Path]:
    base = CONTENT / f"{month:02d}"
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("[SS][VP]-*.md") if SERVICE_NAME.match(path.name))


def theme_for(slot: str) -> str:
    return THEME_BY_SLOT.get(slot, "other")


def first_unprepared_day(posts: list[Post], year: int, month: int) -> int | None:
    days_in_month = calendar.monthrange(year, month)[1]
    by_day: dict[int, list[Post]] = defaultdict(list)
    for post in posts:
        by_day[post.day].append(post)
    for day in range(1, days_in_month + 1):
        if len(by_day.get(day, [])) < 3:
            return day
    return None


def trend_review_due(year: int, month: int, day: int | None) -> bool:
    if day is None:
        return False
    current = date(year, month, day)
    if current < TREND_REVIEW_START:
        return False
    return (current - TREND_REVIEW_START).days % 5 == 0


def missing_priority(counts: Counter[str], priority: list[str]) -> list[str]:
    return [rubric for rubric in priority if counts[rubric] == 0]


def branch_name(rubric: str) -> str:
    if rubric in SWEET:
        return "sweet"
    if rubric in SAVORY_BAKE:
        return "savory_baking"
    if rubric in BROAD_FOOD:
        return "broad_food"
    return "other"


def recommendation_line(label: str, missing: list[str], fallback: str) -> str:
    if missing:
        return f"- {label}: next priority `{missing[0]}`; keep `{', '.join(missing[:4])}` in the queue."
    return f"- {label}: no zero-count priority rubrics; rotate by date. {fallback}"


def debt_status(condition: bool) -> str:
    return "DEBT" if condition else "OK"


def render_report(year: int, month: int, posts: list[Post], services: list[Path]) -> str:
    days_in_month = calendar.monthrange(year, month)[1]
    days_with_content = len({post.day for post in posts})
    next_day = first_unprepared_day(posts, year, month)
    trend_due = trend_review_due(year, month, next_day)

    slot_counts = Counter(post.slot for post in posts)
    theme_counts = Counter(theme_for(post.slot) for post in posts)
    rubric_counts = Counter(post.rubric for post in posts)
    status_counts = Counter(post.status or "missing" for post in posts)
    service_counts = Counter(SERVICE_NAME.match(path.name).group("prefix") for path in services if SERVICE_NAME.match(path.name))

    food_branch_counts = Counter(branch_name(post.rubric) for post in posts if theme_for(post.slot) == "food")
    theme_rubrics: dict[str, Counter[str]] = defaultdict(Counter)
    theme_zones: dict[str, Counter[str]] = defaultdict(Counter)
    zone_counts = Counter()
    missing_metadata: list[Post] = []
    invalid_zones: list[Post] = []

    for post in posts:
        theme = theme_for(post.slot)
        theme_rubrics[theme][post.rubric] += 1
        if not post.zone or not post.axis or not post.source_type:
            missing_metadata.append(post)
        elif post.zone not in VALID_ZONES:
            invalid_zones.append(post)
        else:
            zone_counts[post.zone] += 1
            theme_zones[theme][post.zone] += 1

    known_zones = sum(zone_counts.values())
    non_european = sum(count for zone, count in zone_counts.items() if zone != "Europe")

    morning_missing = missing_priority(theme_rubrics["morning_myth"], MORNING_PRIORITY)
    food_missing = missing_priority(theme_rubrics["food"], FOOD_PRIORITY)
    evening_missing = missing_priority(theme_rubrics["evening_calendar"], EVENING_PRIORITY)

    food_debt = []
    if food_branch_counts["sweet"] > food_branch_counts["savory_baking"] + food_branch_counts["broad_food"]:
        food_debt.append("sweet-heavy")
    if food_branch_counts["savory_baking"] == 0:
        food_debt.append("no savory baking")
    if food_branch_counts["broad_food"] == 0:
        food_debt.append("no broad food")
    zone_debt = []
    for label, group in REQUIRED_ZONE_GROUPS:
        if not (set(zone_counts) & group):
            zone_debt.append(label)

    lines: list[str] = []
    lines.append(f"# ROTATION STATUS REPORT - {year}-{month:02d}")
    lines.append("")
    lines.append("## Visual Dashboard")
    lines.append("")
    lines.append("| Block | Already Visible | Risk | Next Editorial Move |")
    lines.append("|-------|-----------------|------|----------------------|")
    lines.append(
        f"| 09:04 | {', '.join(f'{k}:{v}' for k, v in theme_rubrics['morning_myth'].most_common(4)) or 'none'} | "
        f"{debt_status(bool(morning_missing))}: {', '.join(morning_missing[:3]) or 'balanced'} | "
        f"{morning_missing[0] if morning_missing else 'rotate strongest source/date'} |"
    )
    lines.append(
        f"| 15:04 | sweet:{food_branch_counts['sweet']} / savory:{food_branch_counts['savory_baking']} / broad:{food_branch_counts['broad_food']} | "
        f"{debt_status(bool(food_debt))}: {', '.join(food_debt) or 'balanced'} | "
        f"{food_missing[0] if food_missing else 'keep branch mix'} |"
    )
    lines.append(
        f"| 21:04 | {', '.join(f'{k}:{v}' for k, v in theme_rubrics['evening_calendar'].most_common(4)) or 'none'} | "
        f"{debt_status(bool(evening_missing))}: {', '.join(evening_missing[:3]) or 'balanced'} | "
        f"{evening_missing[0] if evening_missing else 'rotate by date'} |"
    )
    lines.append(
        f"| Coverage | zones:{len(zone_counts)} / metadata:{known_zones} | "
        f"{debt_status(bool(zone_debt) or len(zone_counts) < 6)}: {', '.join(zone_debt[:2]) or 'balanced'} | "
        f"{zone_debt[0] if zone_debt else 'maintain global spread'} |"
    )
    lines.append(
        f"| Service | {', '.join(f'{key}:{value}' for key, value in service_counts.most_common()) or 'none'} | "
        f"{'WATCH' if sum(service_counts.values()) > 0 else 'OK'}: non-daily | "
        "SV/SP only if it clarifies navigation |"
    )
    lines.append(
        f"| Trend review | next date {f'{year}-{month:02d}-{next_day:02d}' if next_day else 'none'} | "
        f"{'CLOSE TODAY' if trend_due else 'OK'}: {'5-day trigger' if trend_due else 'not due'} | "
        f"{'show trend panel + apply feature' if trend_due else 'rotation dashboard only'} |"
    )
    lines.append("")

    lines.append("## Scope")
    lines.append("")
    lines.append(f"- AL posts found: {len(posts)}")
    lines.append(f"- Days with content: {days_with_content} / {days_in_month}")
    lines.append(f"- Next unprepared or incomplete day: {f'{year}-{month:02d}-{next_day:02d}' if next_day else 'none'}")
    lines.append(f"- Statuses: {', '.join(f'{key}={value}' for key, value in status_counts.most_common()) or 'none'}")
    lines.append("")

    lines.append("## Slot And Theme Counts")
    lines.append("")
    for slot, count in sorted(slot_counts.items()):
        lines.append(f"- `{slot}`: {count}")
    lines.append("")
    for theme, label in THEME_LABELS.items():
        if theme_counts[theme]:
            lines.append(f"- `{label}`: {theme_counts[theme]}")
    lines.append("")

    lines.append("## Rubric Counts")
    lines.append("")
    for rubric, count in rubric_counts.most_common():
        lines.append(f"- `{rubric}`: {count}")
    lines.append("")

    lines.append("## Food Balance")
    lines.append("")
    lines.append(f"- Sweet branch: {food_branch_counts['sweet']}")
    lines.append(f"- Savory baking branch: {food_branch_counts['savory_baking']}")
    lines.append(f"- Broad food/process branch: {food_branch_counts['broad_food']}")
    lines.append("")
    lines.append("Target for a full 31-day month: sweet 16-20, savory baking 8-12, broad food/process 8-12.")
    lines.append("")

    lines.append("## Coverage")
    lines.append("")
    lines.append(f"- Posts with full coverage metadata: {known_zones}")
    lines.append(f"- Missing coverage metadata: {len(missing_metadata)}")
    lines.append(f"- Cultural zones represented: {len(zone_counts)}")
    if known_zones:
        lines.append(f"- Non-Europe/cross-global share: {non_european}/{known_zones} ({non_european / known_zones:.0%})")
    if zone_counts:
        lines.append("")
        for zone, count in zone_counts.most_common():
            lines.append(f"- `{zone}`: {count}")
    lines.append("")

    lines.append("## Theme Zone Counts")
    lines.append("")
    for theme in ("morning_myth", "food", "evening_calendar"):
        lines.append(f"### {THEME_LABELS[theme]}")
        zones = theme_zones.get(theme, Counter())
        if zones:
            for zone, count in zones.most_common():
                lines.append(f"- `{zone}`: {count}")
        else:
            lines.append("- No zone metadata yet.")
        lines.append("")

    lines.append("## Editorial Debt")
    lines.append("")
    debt_lines: list[str] = []
    for label, group in REQUIRED_ZONE_GROUPS:
        if not (set(zone_counts) & group):
            debt_lines.append(f"- Missing required zone group: {label}.")
    for theme in ("morning_myth", "food", "evening_calendar"):
        if len(theme_zones.get(theme, {})) < 3:
            debt_lines.append(f"- `{THEME_LABELS[theme]}` needs 3+ cultural zones; now {len(theme_zones.get(theme, {}))}.")
    if missing_metadata:
        debt_lines.append("- Some posts are missing `cultural_zone`, `coverage_axis`, or `source_type`.")
    if invalid_zones:
        debt_lines.append("- Some posts use invalid `cultural_zone` values.")
    if not debt_lines:
        debt_lines.append("- No structural coverage debt detected.")
    lines.extend(debt_lines)
    lines.append("")

    lines.append("## Next Moves")
    lines.append("")
    lines.append(recommendation_line("09:04", morning_missing, "Use the strongest date/source hook."))
    lines.append(recommendation_line("15:04", food_missing, "Keep sweet/savory/broad-food rotation even."))
    lines.append(recommendation_line("21:04", evening_missing, "Use FEAST/RITES/CYCLES when the date supports it."))
    if service_counts:
        lines.append(f"- Service layer already present: {', '.join(f'{key}={value}' for key, value in service_counts.most_common())}. Keep it non-daily.")
    else:
        lines.append("- Service layer: none yet in this month.")
    lines.append("")

    lines.append("## Bolder Tone Tests")
    lines.append("")
    lines.append("- Use one `FIELD FILE` or `DOSSIER` morning post in the next 7 days: person/creature/object as if it has evidence, address, tools, trace.")
    lines.append("- Make the first line sharper: contradiction, object in action, or exact source. Avoid soft openings.")
    lines.append("- In food, lead with failure point or texture test before history.")
    lines.append("- In calendar, lead with mechanism: who repeats what, what the date changes, what is excluded.")
    lines.append("- Visuals should look like evidence from a magazine shoot: one object, tactile surface, analog flash or controlled side light, no symbolic collage.")
    lines.append("")

    lines.append("## Report Cadence")
    lines.append("")
    lines.append("- Run after every prepared day block and before writing the next date.")
    lines.append("- Use analytics/ER later; this report is for editorial balance before performance data exists.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    write = False
    if "--write" in args:
        args.remove("--write")
        write = True
    if len(args) != 2:
        print("Usage: rotation_report.py YYYY MM [--write]", file=sys.stderr)
        return 2

    year = int(args[0])
    month = int(args[1])
    try:
        posts = load_posts(year, month)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    services = load_services(year, month)
    report = render_report(year, month, posts, services)

    if write:
        REPORTS.mkdir(parents=True, exist_ok=True)
        target = REPORTS / f"{year}-{month:02d}-ROTATION-STATUS.md"
        target.write_text(report + "\n", encoding="utf-8")
        print(f"Wrote {target}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
