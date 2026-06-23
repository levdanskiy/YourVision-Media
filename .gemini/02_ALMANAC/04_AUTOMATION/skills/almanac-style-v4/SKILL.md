---
name: almanac-style-v4
description: Revise Almanac hooks, pacing, structure, endings and visual prompts into the current bold editorial voice. Use for tone modernization, post rewrites, visual QA, or format experiments.
---

# Almanac Style V4

Read `VOICE_LEXICON.md`, `CONTEMPORARY_STYLE_GUIDE.md` and `VISUAL_SYSTEM.md`.

## Edit Standard

- Open with a concrete image or action in the present tense.
- Prefer tactile nouns, precise verbs and visible evidence over explanation.
- Vary post architecture: dossier, field note, split-screen comparison, ledger, timeline, recipe protocol or compact list.
- Do not moralize, beg for reactions or append generic questions.
- Keep visual prompts photographable, inspectable and distinct from the previous 30 days.
- For scheduled/published posts, validate the real image file, ALT, rights and approval/use state.
- Treat trend devices as experiments with a hypothesis, not permanent decoration.

Run:

```bash
python3 tools/audit_style.py YYYY MM DD
python3 tools/almanac visuals YYYY-MM-DD
python3 tools/almanac assets audit YYYY-MM-DD --strict
python3 tools/almanac doctor YYYY-MM-DD
```
