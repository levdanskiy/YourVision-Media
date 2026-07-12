---
name: almanac-trend-scout
description: Run the Almanac five-day trend review. Use on due dates or when current Telegram formats, editorial voice, visuals, interaction patterns, food culture or folklore media trends may have changed.
---

# Almanac Trend Scout

## Review

1. Check due state with `python3 tools/almanac trends YYYY-MM-DD`.
2. Research current authoritative or primary sources. Mark inference as inference.
3. Compare signals against channel identity; reject generic platform mimicry.
4. Propose one small, one medium and one large experiment.
5. Register the adopted change in `EXPERIMENT_REGISTRY.json`, name its hypothesis and metric, and save `03_REPORTS/trends/TREND-YYYY-MM-DD.md`.
6. Verify with `python3 tools/almanac trends YYYY-MM-DD --strict`.

Keep source links and access dates in the report.
