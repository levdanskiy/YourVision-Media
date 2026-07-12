---
name: almanac-series-keeper
description: Maintain recurring Almanac series and optional service/special cadence. Use when planning zodiac, tarot, oracle notes, calendar radar, multi-part arcs, reader formats, or reviewing an underperforming series.
---

# Almanac Series Keeper

Use `04_DATABASES/SERIES_REGISTRY.json` as the planning source.

## Rules

- Update `next_due`, status and notes after every installment.
- From 20.07.2026, require exactly one ORACLE-NOTE and one CALENDAR-RADAR per ISO week; keep SP at 2-4 per month.
- A series installment must have a distinct `angle_id`; repeated packaging is not continuity.
- If the first installment underperforms, pause and review instead of forcing the remaining parts.
- Run `python3 tools/almanac series YYYY-MM-DD` before adding optional content.
