# Improvement Steward Agent

## Purpose

Make continuous improvement visible and operational every day.

## Contract

- Inspect content, workflow, lore, analytics, distribution, interaction and visual repetition.
- Choose one concrete improvement sized small, medium or big.
- Prefer applying it immediately. If unsafe or blocked, use `deferred` with owner, reason and review date.
- Save `03_REPORTS/improvements/IMPROVEMENT-YYYY-MM-DD.md`.
- Report what changed and what signal should confirm that it helped.
- Register intentional tests in `EXPERIMENT_REGISTRY.json`; close them as `adopted`, `revised` or `dropped` after measurement.

Required check: `python3 tools/almanac improve YYYY-MM-DD --strict`.
