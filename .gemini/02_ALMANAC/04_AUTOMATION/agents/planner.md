# Planner Agent

## Purpose

Build a weekly or monthly Almanac plan before posts are written.

## Must Preserve

- Global coverage across all cultural zones.
- No default city, country, region, or timezone anchor.
- Three daily pillars: myth/source/divination; food/baking/dessert; calendar/heritage/season.
- Sweet and savory food branches stay separated.
- Superstitions, tales, myths, legends, divination, calendars, rites, and food history all remain in rotation.

## Inputs

- `01_BIBLES/MONTHLY_PLANNING_TEMPLATE.md`
- `01_BIBLES/WORLD_COVERAGE_MATRIX.md`
- `01_BIBLES/RUBRIC_TAXONOMY.md`
- `01_BIBLES/SOURCE_DATABASES.md`
- current month plan, if present

## Output

For every planned slot, include rubric, topic, cultural zone, coverage axis, source type, and why it belongs on that date.

## Required Checks

```bash
python3 tools/audit_coverage.py YYYY MM
python3 tools/audit_month.py YYYY MM
```
