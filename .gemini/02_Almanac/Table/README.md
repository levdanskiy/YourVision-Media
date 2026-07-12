# ALMANAC: TABLE - OPERATING INDEX

This folder is the working archive for `ALMANAC: TABLE`: content rules, seasonal plans, source bibles, generated posts, assets, and operational checks. `ALMANAC: MARGINALIA` remains the archive-era name for pre-pivot material.

## Current Structure

| Path | Role |
|------|------|
| `01_BIBLES/` | Editorial source of truth: voice, rubrics, templates, calendars, sources, visual rules. |
| `02_CONTENT/2026/` | Published-ready and archive posts by date. |
| `legacy_from_yv/` | Legacy YourVision-era planning material. Keep for reference, do not use as current rules. |
| `tools/` | Local audit and validation scripts. |
| `03_REPORTS/` | Generated audit reports and handoff notes. |
| `03_ASSETS/` | Future generated/approved images, if visual files are stored locally. |
| `04_AUTOMATION/` | Project skills, agent-role notes, hooks, and automation sources. |
| `04_DATABASES/` | Approved local dataset policy, registry, and small source indexes. |

## Source Of Truth

Read these before creating or editing posts:

1. `01_BIBLES/ALMANAC_BIBLE.md` - project mission, themes, system navigation.
2. `01_BIBLES/RUBRIC_TAXONOMY.md` - short source of truth for rubrics and deprecated labels.
3. `01_BIBLES/WORLD_COVERAGE_MATRIX.md` - cultural zones, axes, quotas, coverage metadata.
4. `01_BIBLES/RUBRIC_RULES.md` - hard quality rules, slot rules, length limits.
5. `01_BIBLES/MONTHLY_PLANNING_TEMPLATE.md` - required month planning grid: slots, zones, axes, sources, V4 series.
6. `01_BIBLES/ARCHIVE_TEMPLATE.md` - post templates by rubric.
7. `01_BIBLES/VOICE_Almanac: Calendar.md` - allowed and forbidden language.
8. `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md` - current voice, carousel/search/screenshot structure, modern visual direction.
9. `01_BIBLES/VISUAL_SYSTEM.md` - image prompt rules.
10. `01_BIBLES/SOURCE_DATABASES.md` - approved external source stacks, trust levels, citation rules.
11. `01_BIBLES/INTERACTIVITY_SYSTEM.md` - polls, audience pulses, quizzes, and non-bait interaction rules.
12. `01_BIBLES/SLOT_STRATEGY.md` - time-slot meaning, rubric movement, and timing-test policy.
13. `01_BIBLES/SERVICE_AND_SPECIALS.md` - optional `SV` service notes, weekly oracle/calendar radar notes, and rare `SP` special posts.
14. `01_BIBLES/BETWEEN_SLOT_SYSTEM.md` - `12:04` service lane, `18:04` special lane, story/external frames.
15. `01_BIBLES/ORACLE_AND_RADAR_SYSTEM.md` - weekly zodiac/tarot/omen/oracle rotation and week-ahead calendar radar.
16. `01_BIBLES/BOLD_LAYER_ROADMAP.md` - six approved bold layers and pilot windows.
17. `01_BIBLES/STORY_LAYER_SYSTEM.md` - Telegram Story templates and limits.
18. `01_BIBLES/PROOF_OF_WORK_SYSTEM.md` - source receipts, technique tests, proof cards.
19. `01_BIBLES/READER_ARCHIVE_SYSTEM.md` - reader memory collection and verification.
20. `01_BIBLES/MONTHLY_ALBUM_SYSTEM.md` - monthly field file/PDF/carousel derivative.
21. `01_BIBLES/FORMAT_EXTENSIONS.md` - accepted lenses and divination subtypes such as TABLE, DREAM, TABOO, GESTURE, LOST, FEAST_TABLE.
22. `01_BIBLES/FOOD_TECHNOLOGY_MATRIX.md` - planning map for global food mechanisms and missing format coverage.
23. `01_BIBLES/CALENDAR_SYSTEMS_BANK.md` - planning bank for world calendars, cycles, modern holidays, fasts, and commemoration.
24. `01_BIBLES/ANALYTICS_REVIEW.md` - biweekly performance review, series failure rules, and non-viral iteration policy.
25. `01_BIBLES/DISTRIBUTION_RULES.md` - stories, cross-posting, audio/video, collaborations, and monetization boundary.
26. `01_BIBLES/AGENTS_AND_SKILLS.md` - recommended planner, writer, factcheck, style, and visual QA passes.
27. `01_BIBLES/Almanac: Calendar_ROUTING.md` - companion-channel routing for all standalone non-recipe material from 23.07.2026.
28. `01_BIBLES/RECIPE_ONLY_SYSTEM.md` - recipe-only pivot from 23.07.2026: slots, rubrics, promo week and service changes.
29. `01_BIBLES/PRE_PUBLISH_CHECKLIST.md` - final manual check.

Older dated plans in `01_BIBLES/PLAN_*.md`, `JUNE_STRATEGY.md`, and `JULY_AUGUST_STRATEGY.md` are historical planning material. Before reusing any topic from them, rebuild it through `WORLD_COVERAGE_MATRIX.md` and current no-regional-anchor rules.

## Daily Publishing Contract

Current AL format expects three slots per day.

Expanded slot rules apply to new and rewritten posts from `2026-07-07`. Already prepared material through `2026-07-06` is not rewritten retroactively.
New posting times apply from `2026-07-17`. Legacy through `2026-07-16` keeps `10:04 / 15:04 / 18:02`.
Recipe-only rules apply from `2026-07-23`: every main `AL` post is a reproducible recipe with `ИНГРЕДИЕНТЫ` and `ПРИГОТОВЛЕНИЕ`. Myth, calendar, source, divination, language and holiday material may appear only as food context inside a recipe. Standalone non-recipe material moves to the companion project `Almanac: Calendar` at `/home/levdanskiy/.gemini/05_Almanac: Calendar` and channel `https://t.me/AlmanacCalendar`.

| Slot | Theme | Rubrics |
|------|-------|---------|
| `09:10` | Through 22.07: myths/sources. From 23.07: recipe prep/base. | Through 22.07: old morning rubrics. From 23.07: food rubrics only. |
| `14:00` | Food only; from 23.07: cook/table recipe. | Food rubrics only. |
| `20:40` | Through 22.07: calendar/time. From 23.07: slow/sweet/tomorrow recipe. | Through 22.07: old evening rubrics. From 23.07: food rubrics only. |

Between-slot layer:
- `10:00` - through 22.07.2026 use existing `SV` rules; from 23.07.2026 use recipe-only service notes such as `MENU-RADAR`, `SHOPPING-LIST`, `TECHNIQUE-POLL`, `RECIPE-INDEX`, `PREP-NOTE`.
- `17:00` - rare `SP` or visual/audio threshold, 2-4 per month max.
- story/external frames are derivatives, not extra `AL` posts.

`FERMENT`, `PRESERVE`, `SOUP`, and `CONDIMENTS` are real 15:04 filename rubrics. Labels such as `TABLE`, `GESTURE`, `DREAM`, `TABOO`, `LOST`, `FEAST_TABLE`, `FAST`, and `LIMINAL` are lenses/subtypes unless the taxonomy says otherwise. Use the real rubric in the filename and add the lens in planning or metadata when useful.

Publication timezone is an operational scheduling setting only. Do not turn any city, country, region, or timezone into an editorial anchor.

Country and city names are allowed when they do real work: comparison, origin, source context, calendar difference, technique history, ingredient ecology, language, or institutional record. The rule is not “delete geography”; the rule is “no geography becomes the channel’s default voice.”

## Max Mode

Default working mode is maximum application of the system:

- use all applicable rules from the source-of-truth docs, not a minimal subset;
- use local databases and indexes when they can improve source choice, coverage, or factcheck;
- apply coverage locks immediately: if an audit exposes debt, the next relevant planned day should close it;
- run `preflight_day.py` for every prepared day and fix every error and warning;
- keep geography when it supports evidence or comparison;
- do not edit an unrelated month/day only because of a likely typo when the active workflow clearly points to the current date sequence.

## File Naming

Preferred current format:

```text
AL-DD.MM-HH-MM-RUBRIC-Slug.md
```

Example:

```text
AL-29.05-15-04-BUNS-Elderflower.md
```

Legacy `AC`, `NB`, and `SW` posts are archive material and are not validated against current AL rules.

## Status Model

Use the status vocabulary in `01_BIBLES/STATUS_MODEL.md`.

Minimum rule: do not mark a post `ГОТОВ` until it passes `PRE_PUBLISH_CHECKLIST.md` and the local validator.

Published posts are not silently rewritten for meaningful factual changes. Use `03_REPORTS/CORRECTIONS.md` and `FACTCHECK_RULES.md`.

## Commands

Validate current AL content:

```bash
python3 tools/validate_almanac.py
```

Validate current AL content with coverage metadata warnings:

```bash
python3 tools/validate_almanac.py --strict-coverage
```

Audit one month:

```bash
python3 tools/audit_month.py 2026 06
```

The month audit checks slot completeness, rubric counts, Sunday `FRAGMENT`, weekly `LISTS` / `HERITAGE` rotation, and long posts.

Audit global coverage metadata and debt:

```bash
python3 tools/audit_coverage.py 2026 07
```

Run biweekly analytics review manually using:

```text
01_BIBLES/ANALYTICS_REVIEW.md
```

Audit system docs for stale rubric or regional-anchor language:

```bash
python3 tools/audit_system_docs.py
```

Run a strict preflight for one ready publishing day:

```bash
python3 tools/preflight_day.py 2026 07 04
```

The daily preflight requires exactly three AL posts: legacy `10:04 / 15:04 / 18:02` through `2026-07-16`, then `09:04 / 15:04 / 21:04`; ready status; strict coverage metadata; V4 style; target body length; visual prompt discipline; and source-note discipline.

Audit V4 tone, visual prompts, regional anchors, engagement bait, and divination framing:

```bash
python3 tools/audit_style.py 2026 07 04
```

Audit FACTCHECK/source metadata and source-type discipline:

```bash
python3 tools/audit_sources.py 2026 07 04
```

Audit body length against rubric target bands:

```bash
python3 tools/audit_lengths.py 2026 07 04
```

Audit rubric and theme rotation (repetition, balance, cultural zones):

```bash
python3 tools/audit_rotation.py 2026 07
```

Run the general prepublish check, or pass a date for strict day mode:

```bash
tools/prepublish.sh
tools/prepublish.sh 2026 07 20
```

Optional local git hook:

```bash
git -C /home/levdanskiy config core.hooksPath .gemini/02_ALMANAC/.githooks
```

The pre-commit hook checks staged publishing days, continuity and system docs. Pre-push runs global audits; post-merge rebuilds indexes. Use `tools/prepublish.sh YYYY MM DD` for final post-day approval, including required trend and daily-improvement evidence.

Unified commands:

```bash
python3 tools/almanac brief YYYY-MM-DD --write
python3 tools/almanac improve YYYY-MM-DD --init
python3 tools/almanac doctor YYYY-MM-DD
python3 tools/almanac publish YYYY-MM-DD
python3 tools/almanac canon
python3 tools/almanac series YYYY-MM-DD
python3 tools/almanac publications sync
python3 tools/almanac assets sync
python3 tools/almanac evidence audit YYYY-MM-DD --strict
python3 tools/almanac semantic search "topic or claim"
python3 tools/almanac experiments list
python3 tools/almanac incidents audit YYYY-MM-DD --strict
```

Download and index approved local source datasets:

```bash
python3 tools/download_databases.py
```

Rebuild indexes from already downloaded raw files:

```bash
python3 tools/build_database_indexes.py
```

Write a report:

```bash
python3 tools/audit_month.py 2026 06 > 03_REPORTS/audit-2026-06.md
```

## Operational Priorities

1. Keep content stable. Do not move large archive folders unless a migration plan exists.
2. Make rules machine-checkable before adding more rules.
3. Treat astronomical, calendar, historical, and etymological claims as factcheck-required.
4. Keep prompts and post bodies separate in the mind: Telegram caption limits apply to the body, not service metadata.
5. Preserve the voice: quiet, tactile, precise, no moralizing endings.
