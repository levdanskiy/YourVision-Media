---
name: almanac-day-writer
description: Prepare or revise one Almanac publishing day. Use for requests to write daily posts, select three rubrics, apply current slots and tone, show rotation status, or validate a day before Telegram scheduling.
---

# Almanac Day Writer

Work inside `/home/levdanskiy/.gemini/02_Almanac/Table`.

## Workflow

1. Read `README.md`, `01_BIBLES/CHANNEL_CANON.yaml`, the current month plan, `RUBRIC_RULES.md`, `CONTEMPORARY_STYLE_GUIDE.md`, `VISUAL_SYSTEM.md`, and `SOURCE_DATABASES.md`.
2. Run `python3 tools/almanac brief YYYY-MM-DD --write`. Show the useful rotation, series, trend and improvement information before the posts.
3. Run `python3 tools/almanac improve YYYY-MM-DD --init`; apply one concrete improvement and mark it `applied`, or document a real `deferred` decision.
4. If `python3 tools/almanac trends YYYY-MM-DD` says `DUE`, complete the current trend report before writing.
5. Create exactly three AL posts. Through `2026-07-16` use `10:04`, `15:04`, `18:02`; from `2026-07-17` use `09:04`, `15:04`, `21:04`.
6. Keep `15:04` food-only and separate sweet from savory. Geography may support evidence and comparison but cannot become the channel's default center.
7. Add complete metadata, factcheck notes, source types, grade and a distinct editorial visual prompt. Add `canon_id`, `angle_id`, `series_id` and `continuity_notes` when relevant.
8. Record claim-level evidence or a reviewed `no_strong_claims` decision for each new ready post. Search semantic memory before reusing an entity or central claim.
9. Run `python3 tools/almanac publish YYYY-MM-DD` and fix all failures before delivery.

Use controlled experiments, not random novelty. Name the changed device and the signal that will show whether it works.
