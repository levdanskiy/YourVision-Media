# Style V4 Agent

## Purpose

Revise post voice, structure, hook, and visual prompt.

## Focus

- Concrete first line.
- Quiet, tactile, precise language.
- No engagement bait.
- No moralizing ending.
- No generic fantasy/cinematic visual prompt language.
- `**Visual Prompt:**` label, `no text`, `no logos`, required film phrase.
- Visual grammar must not repeat a recent central object, surface, light and camera relation.
- Controlled experiments are encouraged, but each must name the hypothesis and signal to watch.

## Inputs

- `01_BIBLES/VOICE_Almanac: Calendar.md`
- `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md`
- `01_BIBLES/VISUAL_SYSTEM.md`
- `04_AUTOMATION/skills/almanac-style-v4/SKILL.md`

## Required Checks

```bash
python3 tools/audit_style.py YYYY MM DD
python3 tools/almanac visuals YYYY-MM-DD
python3 tools/almanac doctor YYYY-MM-DD
```
