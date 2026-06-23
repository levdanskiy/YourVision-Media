# AGENTS AND SKILLS

This file defines the working roles for Almanac. These are not separate editorial centers; they are repeatable passes over the same global system.

## Operating Rule

Every pass must preserve the current principles:

- global coverage across all cultural zones;
- geography serves evidence and comparison rather than a fixed editorial center;
- three daily slots: myth/source/divination/personae, food-only baking/dessert/foodways, calendar/heritage/season/feast;
- sweet and savory baking/dessert branches stay separated;
- divination may include approved weekly editorial predictions and oracle formats, but never deterministic medical, legal or financial advice;
- every ready post carries coverage metadata, source metadata, FACTCHECK, grade, and visual prompt.
- every prepared day from `2026-07-21` carries a visible improvement record with an applied or explicitly deferred change;
- every fifth day from `2026-07-17` carries a current trend review.

## Max Mode

Almanac work is not a minimal compliance pass. Use the whole rule system every time:

- source-of-truth docs;
- local source databases and indexes;
- coverage locks and monthly quotas;
- source hierarchy and citation rules;
- V4 tone, visual, and carousel/search structure;
- strict daily preflight.
- canon, series and recent visual checks;
- a visible rotation report before writing.

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
python3 tools/almanac brief YYYY-MM-DD --write
python3 tools/almanac improve YYYY-MM-DD --init
python3 tools/almanac publish YYYY-MM-DD
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

### Editorial Orchestrator

Purpose: coordinate the entire request and make rotation, trend and improvement decisions visible.

Uses:
- `04_AUTOMATION/skills/almanac-orchestrator/SKILL.md`
- `04_AUTOMATION/agents/editorial-orchestrator.md`

### Continuity Keeper

Purpose: prevent accidental repetition and preserve factual/entity continuity.

Required commands:

```bash
python3 tools/almanac canon
python3 tools/almanac continuity YYYY-MM-DD
```

### Series Keeper

Purpose: track recurring formats and the SV/SP limits.

Required command: `python3 tools/almanac series YYYY-MM-DD`.

### Trend Scout

Purpose: complete the five-day current-market review and apply one controlled experiment.

Required command: `python3 tools/almanac trends YYYY-MM-DD --strict` when due.

### Improvement Steward

Purpose: apply or formally defer one concrete improvement for every prepared day.

Required command: `python3 tools/almanac improve YYYY-MM-DD --strict`.

## Operational Registries

From `2026-07-21`, a new ready day also passes these layers:

```bash
python3 tools/almanac publications audit YYYY-MM-DD --strict
python3 tools/almanac assets audit YYYY-MM-DD --strict
python3 tools/almanac evidence audit YYYY-MM-DD --strict
python3 tools/almanac semantic audit YYYY-MM-DD --strict
python3 tools/almanac experiments audit YYYY-MM-DD --strict
python3 tools/almanac incidents audit YYYY-MM-DD --strict
```

- Publication registry separates content readiness from scheduling and publication.
- Asset registry validates real image files, ALT and rights.
- Evidence registry maps claims to supporting sources.
- Semantic memory finds meaning-level repetition.
- Experiment registry forces measurement and adoption/drop decisions.
- Incident registry blocks unresolved high/critical problems on affected posts.

## Hook

Optional local hook:

```bash
git -C /home/levdanskiy config core.hooksPath .gemini/02_ALMANAC/.githooks
```

The hooks run focused day checks before commit, global audits before push, and rebuild generated indexes after merge.

```bash
python3 tools/hook_pre_commit.py
```

Use the stricter daily gate before publication:

```bash
tools/prepublish.sh YYYY MM DD
```

## Installed Project Skills

Project skill sources live in `04_AUTOMATION/skills/`. Install each skill directory into:

```text
~/.codex/skills/
```

After editing a skill, validate it and refresh the installed copy. Do not create extra README files inside skill directories; `SKILL.md` is the source of truth.
