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
- Repeated claims, changed spellings, conflicting dates, and unresolved continuity notes.
- Claim-level source evidence: access date, locator, trust level and exact supporting paraphrase.

## Inputs

- `01_BIBLES/SOURCE_DATABASES.md`
- `01_BIBLES/RUBRIC_RULES.md`
- `04_AUTOMATION/skills/almanac-factcheck/SKILL.md`

## Required Checks

```bash
python3 tools/audit_sources.py YYYY MM DD
python3 tools/almanac continuity YYYY-MM-DD
python3 tools/almanac evidence audit YYYY-MM-DD --strict
python3 tools/almanac doctor YYYY-MM-DD
```
