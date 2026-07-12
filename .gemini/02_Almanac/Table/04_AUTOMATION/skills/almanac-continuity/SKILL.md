---
name: almanac-continuity
description: Track Almanac canon, entities, angles, series, claims and visual motifs. Use before reusing a myth, person, object, dish, holiday or recurring format, and when auditing archive contradictions or repetition.
---

# Almanac Continuity

## Workflow

1. Rebuild evidence with `python3 tools/almanac canon`.
2. Search `04_DATABASES/CANON_REGISTRY.json` for the entity and recent related axes.
3. Search meaning-level memory with `python3 tools/almanac semantic search "entity claim or motif"`.
4. Use `canon_id` for the stable entity, `angle_id` for this treatment, `series_id` for recurring formats and `continuity_notes` for variant or conflict decisions.
5. Run continuity and semantic audits for the date.

An intentional new cultural variant is allowed when the source tradition and angle are explicit. An identical claim, framing or image presented as new is not.
