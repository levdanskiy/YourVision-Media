---
name: almanac-day-writer
description: Use when preparing Almanac daily content in 02_ALMANAC: three AL posts for 10:04, 15:04, and 18:02, aligned with the current rubrics, global coverage matrix, July plan, V4 style, and preflight checks.
---

# Almanac Day Writer

Work inside `/home/levdanskiy/.gemini/02_ALMANAC`.

Before writing, read:
- `README.md`
- `01_BIBLES/ALMANAC_BIBLE.md`
- `01_BIBLES/RUBRIC_TAXONOMY.md`
- `01_BIBLES/WORLD_COVERAGE_MATRIX.md`
- `01_BIBLES/RUBRIC_RULES.md`
- `01_BIBLES/ARCHIVE_TEMPLATE.md`
- `01_BIBLES/VOICE_LEXICON.md`
- `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md`
- `01_BIBLES/VISUAL_SYSTEM.md`
- `01_BIBLES/SOURCE_DATABASES.md`

Daily contract:
- Create exactly three AL posts: `10:04`, `15:04`, `18:02`.
- Use the current filename format: `AL-DD.MM-HH-MM-RUBRIC-Slug.md`.
- Do not anchor the project to any single city, country, region, or timezone.
- Treat all three pillars globally: myth/source/divination, baking/desserts/food history, calendar/heritage/season.
- Keep `15:04` food-only: dish, drink, ingredient, preservation, kitchen tool, food technique, table, or food history. Standalone `PROSE`/`ETYMON` must move to `10:04` or `18:02`.
- Separate sweet and savory baking/dessert logic through the current taxonomy.
- Include `cultural_zone`, `coverage_axis`, `source_type`, `FACTCHECK`, `Grade`, and `Visual Prompt`.
- Keep body length inside the rubric target band from `RUBRIC_RULES.md`; use compact posts only when the rubric allows it.
- Apply maximum applicable rules, not minimal compliance: source hierarchy, coverage locks, V4 structure, visual discipline, local databases, and all rubric-specific requirements.
- Write visual prompts as modern editorial/documentary magazine photography, not stock/fantasy/museum reconstruction.
- If the active task sequence is one month/day and a later user message contains a likely date typo, keep scope to the active sequence unless the user explicitly asks to repair archive material.

After writing, run:

```bash
python3 tools/preflight_day.py YYYY MM DD
```

Fix every error and warning before calling the day ready.
