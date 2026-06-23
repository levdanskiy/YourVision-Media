#!/usr/bin/env python3
"""Create three non-destructive draft post shells for one publishing day."""

from __future__ import annotations

import argparse
import re

from almanac_common import CONTENT, parse_date_target, slots_for


FOOD = {
    "CAKES", "BUNS", "PATISSERIE", "DESSERTS", "SWEETS", "BREAD", "FLATBREAD", "PIES",
    "FERMENT", "PRESERVE", "SOUP", "CONDIMENTS", "GRAIN", "STREET", "FASTING_FOOD",
    "RECIPE", "FOODWAYS", "PANTRY", "DRINKS", "TOOLS", "WORKFLOW", "LISTS",
}


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value or "Working-Title"


def content(day, slot: str, rubric: str) -> str:
    date_text = day.isoformat()
    human = day.strftime("%d.%m")
    post_id = f"AL-{human}-{slot.replace(':', '-')}-{rubric}-Working-Title"
    return f'''---
post_id: "{post_id}"
title: "Working title"
slug: "{slugify(rubric.lower())}-working-title"
date: "{date_text}"
time: "{slot}"
timezone: "PUBLICATION_TIMEZONE"
status: "DRAFT"
rubric: "{rubric}"
cultural_zone: ""
secondary_zones: ""
coverage_axes: ""
source_types: ""
canon_id: ""
angle_id: ""
series_id: ""
continuity_notes: ""
factcheck_notes: ""
sources_used: ""
v4_techniques: ""
---

// ИД-ПОСТА: {post_id}
// РУБРИКА: #{rubric}
// СТАТУС: DRAFT
// СЛОТ: {slot}

**#{rubric}: WORKING TITLE**

[First line is an image in the present tense.]

[Post body.]

***

**Grade:** DRAFT
**Visual Prompt:** [Concrete subject, action, environment, light, camera logic; no text or logos]
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--rubrics", required=True, help="Exactly three comma-separated rubrics")
    args = parser.parse_args()
    day = parse_date_target(args.target)
    rubrics = [part.strip().lstrip("#").upper() for part in args.rubrics.split(",") if part.strip()]
    if len(rubrics) != 3:
        parser.error("--rubrics requires exactly three values")
    if rubrics[1] not in FOOD:
        parser.error(f"middle rubric `{rubrics[1]}` is not a food rubric")
    base = CONTENT / day.strftime("%Y/%m/%d")
    base.mkdir(parents=True, exist_ok=True)
    created = 0
    for slot, rubric in zip(slots_for(day), rubrics, strict=True):
        name = f"AL-{day.strftime('%d.%m')}-{slot.replace(':', '-')}-{rubric}-Working-Title.md"
        path = base / name
        if path.exists():
            print(f"SKIP: {path}")
            continue
        path.write_text(content(day, slot, rubric), encoding="utf-8")
        print(f"CREATED: {path}")
        created += 1
    print(f"SCAFFOLD: {created} created, {3 - created} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
