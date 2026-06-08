---
name: almanac-style-v4
description: Use when revising Almanac posts for contemporary V4 tone, hook strength, visual prompt quality, no-regional-anchor discipline, no engagement bait, and modern carousel/search/screenshot-compatible structure.
---

# Almanac Style V4

Primary references:
- `01_BIBLES/VOICE_LEXICON.md`
- `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md`
- `01_BIBLES/VISUAL_SYSTEM.md`
- `01_BIBLES/PRE_PUBLISH_CHECKLIST.md`

Style rules:
- Open with a concrete image, conflict, object, date, or sensory detail.
- Keep the voice quiet, precise, tactile, and modern.
- Do not use engagement bait, moralizing endings, pseudo-mystical fog, or explanatory filler.
- Do not make Riga, Latvia, the Baltics, Europe, or any region the default editorial center.
- Divination content is cultural history and visual practice, not advice or prediction.
- Visual prompts must describe a photographable scene, include `no text` and `no logos`, and end with `shot on 35mm film Kodak Portra 800`.
- Use `**Visual Prompt:**`, not the old prompt label.

Run targeted checks:

```bash
python3 tools/audit_style.py YYYY MM DD
python3 tools/preflight_day.py YYYY MM DD
```
