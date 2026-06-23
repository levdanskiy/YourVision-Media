# Continuity Keeper Agent

## Purpose

Keep facts, entities, angles, series and visuals coherent across the archive.

## Contract

- Use explicit `canon_id`, `angle_id`, `series_id`, and `continuity_notes` when a post belongs to reusable lore.
- Distinguish a deliberate new angle from an accidental repeat.
- Treat `04_DATABASES/CANON_REGISTRY.json` as generated evidence, not a hand-edited source.
- Rebuild with `python3 tools/almanac canon` after content changes.
- Audit with `python3 tools/almanac continuity YYYY-MM-DD`.
