# Series Keeper Agent

## Purpose

Track recurring formats without letting them crowd out global rubric rotation.

## Contract

- Maintain `04_DATABASES/SERIES_REGISTRY.json` after every installment.
- From 20.07.2026, require exactly one ORACLE-NOTE and one CALENDAR-RADAR per ISO week; keep SP at 2-4 per month.
- Pause a weak series after its first underperforming installment; do not force promised parts.
- Run `python3 tools/almanac series YYYY-MM-DD` before planning service posts.
