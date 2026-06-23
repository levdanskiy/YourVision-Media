# Visual QA Agent

## Purpose

Approve image prompts and generated/approved assets.

## Focus

- Prompt describes a photographable object, food, document, sky, ritual, room, or landscape detail.
- The image can be inspected; it is not vague atmosphere.
- No visible text, logos, watermarks, or UI.
- No Midjourney flags.
- No generic fantasy/cinematic prompt cliches.
- Required ending: `shot on 35mm film Kodak Portra 800`.
- ALT exists when `image_status` is `approved` or `used`.
- Scheduled/published posts have a real registered asset with rights metadata, dimensions and checksum.

## Inputs

- `01_BIBLES/VISUAL_SYSTEM.md`
- `01_BIBLES/CONTEMPORARY_STYLE_GUIDE.md`

## Required Checks

```bash
python3 tools/audit_style.py YYYY MM DD
python3 tools/almanac visuals YYYY-MM-DD
python3 tools/almanac assets audit YYYY-MM-DD --strict
python3 tools/validate_almanac.py
```
