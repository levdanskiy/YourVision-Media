# Day Writer Agent

## Purpose

Write or prepare one full publishing day.

## Contract

- Exactly three AL files. Through `2026-07-16`: `10:04`, `15:04`, `18:02`; from `2026-07-17`: `09:04`, `15:04`, `21:04`.
- Current filename format: `AL-DD.MM-HH-MM-RUBRIC-Slug.md`.
- Ready posts include status, date, time, rubric, cultural zone, coverage axis, source type, FACTCHECK, grade, and visual prompt.
- Body length should fit the rubric target band in `RUBRIC_RULES.md`; short formats must be intentional, not accidental.
- `15:04` is always food-related. Do not place standalone `PROSE` or `ETYMON` there; embed language/literature as a layer inside a food rubric.
- Visual prompts should read as modern editorial/documentary magazine photography, adapted to the rubric.
- Divination may use the approved entertainment/editorial forecast format, never deterministic personal medical, financial or legal advice.
- No local/regional default center.
- Use maximum applicable rules: coverage locks, source databases, V4 tone, visual rules, citation discipline, and strict preflight.
- Keep scope to the requested current day; do not repair another month/day unless explicitly requested.
- Before writing, show the generated rotation/continuity brief and identify the day's improvement.
- Every day from `2026-07-21` needs an improvement report with status `applied` or explicitly `deferred`.
- On every fifth day from `2026-07-17`, complete the current trend review before delivery.

## Inputs

- `README.md`
- `01_BIBLES/ARCHIVE_TEMPLATE.md`
- `01_BIBLES/RUBRIC_RULES.md`
- `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md`
- `01_BIBLES/SOURCE_DATABASES.md`
- `04_DATABASES/SOURCE_REGISTRY.md`
- `04_DATABASES/indexes/source_cards.csv`
- `04_AUTOMATION/skills/almanac-day-writer/SKILL.md`

## Required Check

```bash
python3 tools/almanac brief YYYY-MM-DD --write
python3 tools/almanac improve YYYY-MM-DD --init
python3 tools/almanac publish YYYY-MM-DD
```
