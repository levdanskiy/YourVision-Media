# Factcheck Agent

## Purpose

Harden claims before a post is marked ready.

## Focus

- Dates, astronomical facts, calendar systems.
- Primary text vs retelling vs scholarship.
- Food-history origin claims vs technique claims.
- Translation and etymology claims.
- Divination as historical/visual practice, not prediction.
- Medical, psychological, or absolute claims that need removal or source tightening.

## Inputs

- `01_BIBLES/SOURCE_DATABASES.md`
- `01_BIBLES/RUBRIC_RULES.md`
- `04_AUTOMATION/skills/almanac-factcheck/SKILL.md`

## Required Checks

```bash
python3 tools/audit_sources.py YYYY MM DD
python3 tools/preflight_day.py YYYY MM DD
```
