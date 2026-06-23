---
name: almanac-factcheck
description: Verify Almanac dates, translations, etymologies, myth variants, food-history claims, calendars, divination framing, source hierarchy, and continuity before a post is marked ready.
---

# Almanac Factcheck

Use `01_BIBLES/SOURCE_DATABASES.md` and the local source registry first.

## Rules

- Separate primary text, later retelling, scholarship and modern adaptation.
- Separate food technique, origin evidence and origin legend.
- Verify moving dates and astronomy with institutional data.
- Keep forecasts explicitly editorial/entertainment-oriented and remove deterministic health, legal or financial advice.
- Avoid universal claims unless the evidence is universal.
- Check previous uses of the same entity, date, spelling and claim in the canon registry.
- Store support for each strong claim in `EVIDENCE_REGISTRY.json`, including trust level, access date and locator.

Run:

```bash
python3 tools/audit_sources.py YYYY MM DD
python3 tools/almanac evidence audit YYYY-MM-DD --strict
python3 tools/almanac continuity YYYY-MM-DD
python3 tools/almanac doctor YYYY-MM-DD
```

Resolve every source error; record defensible uncertainty instead of hiding it.
