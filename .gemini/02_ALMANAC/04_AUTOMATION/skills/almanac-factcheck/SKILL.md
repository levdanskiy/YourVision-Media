---
name: almanac-factcheck
description: Use when checking Almanac posts for FACTCHECK quality, source hierarchy, source_type discipline, dates, translations, food history claims, myth/source claims, divination framing, and medical/predictive-risk language.
---

# Almanac Factcheck

Work from the project source list in `01_BIBLES/SOURCE_DATABASES.md`.

Rules:
- Prefer primary texts, critical editions, museum/catalog records, institutional calendars, ethnographic collections, and food-history references.
- Mark the source basis in `source_type`; do not leave generic or placeholder source notes.
- For myths and tales, distinguish primary text, later retelling, scholarly interpretation, and modern folklore adaptation.
- For divination, describe historical objects, decks, manuals, visual systems, or calendar systems. Do not produce personal predictions.
- For food history, separate recipe technique from origin legend and from modern adaptation.
- For calendar/astronomy posts, use calendar-data or science-reference sources for dates and phenomena.
- Avoid absolute claims such as "all cultures", "always", "never", and "the only source" unless the evidence really supports them.

Run targeted checks:

```bash
python3 tools/audit_sources.py YYYY MM DD
python3 tools/preflight_day.py YYYY MM DD
```

Fix every source warning before ready status.
