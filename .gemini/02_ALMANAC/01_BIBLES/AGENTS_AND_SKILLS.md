# AGENTS AND SKILLS

This file defines the working roles for Almanac. These are not separate editorial centers; they are repeatable passes over the same global system.

## Operating Rule

Every pass must preserve the current principles:

- global coverage across all cultural zones;
- no default Riga / Latvia / Baltic / Europe anchor;
- three daily slots: myth/source/divination/personae, food-only baking/dessert/foodways, calendar/heritage/season/feast;
- sweet and savory baking/dessert branches stay separated;
- divination is historical and visual culture, not personal prediction;
- every ready post carries coverage metadata, source metadata, FACTCHECK, grade, and visual prompt.

## Max Mode

Almanac work is not a minimal compliance pass. Use the whole rule system every time:

- source-of-truth docs;
- local source databases and indexes;
- coverage locks and monthly quotas;
- source hierarchy and citation rules;
- V4 tone, visual, and carousel/search structure;
- strict daily preflight.

If a user asks for a day in the current sequence, keep work scoped to that day unless they explicitly ask to repair archive material. If a date looks like a typo, do not edit a different month just to be literal.

## Recommended Agent Passes

### Planner

Purpose: build a month or week plan before writing.

Agent card:
- `04_AUTOMATION/agents/planner.md`

Checks:
- coverage zones and axes;
- source-type diversity;
- no repeated region as hidden center;
- rotation across myth, tales, superstitions, divination, personae, bestiary, objects, food history, foodways, pantry, drinks, tools, calendar systems, heritage, rites, feasts, and modern practices.

Required command after planning:

```bash
python3 tools/audit_coverage.py YYYY MM
```

### Day Writer

Purpose: create the three posts for one date.

Uses:
- `04_AUTOMATION/skills/almanac-day-writer/SKILL.md`

Agent card:
- `04_AUTOMATION/agents/day-writer.md`

Required command:

```bash
python3 tools/preflight_day.py YYYY MM DD
```

### Factcheck

Purpose: harden factual claims, dates, translations, source notes, and source hierarchy.

Uses:
- `04_AUTOMATION/skills/almanac-factcheck/SKILL.md`

Agent card:
- `04_AUTOMATION/agents/factcheck.md`

Required command:

```bash
python3 tools/audit_sources.py YYYY MM DD
```

### Style V4

Purpose: revise voice, hook, structure, and visual prompt so the post feels current without becoming clickbait.

Uses:
- `04_AUTOMATION/skills/almanac-style-v4/SKILL.md`

Agent card:
- `04_AUTOMATION/agents/style-v4.md`

Required command:

```bash
python3 tools/audit_style.py YYYY MM DD
```

### Visual QA

Purpose: approve image prompts and generated assets.

Agent card:
- `04_AUTOMATION/agents/visual-qa.md`

Checks:
- no visible text or logos;
- no Midjourney flags;
- no generic fantasy/cinematic prompt cliches;
- object, ritual, food, sky, or document is inspectable;
- prompt ends with the required film phrase.

## Hook

Optional local hook:

```bash
git config core.hooksPath .githooks
```

The hook runs:

```bash
python3 tools/validate_almanac.py
python3 tools/audit_system_docs.py
```

Use the stricter daily gate before publication:

```bash
tools/prepublish.sh YYYY MM DD
```

## Installing Project Skills Later

Project skill sources live in `04_AUTOMATION/skills/`. If Codex global skills are writable, copy each skill directory into:

```text
~/.codex/skills/
```

Do not create extra README files inside skill directories; `SKILL.md` is the source of truth.
