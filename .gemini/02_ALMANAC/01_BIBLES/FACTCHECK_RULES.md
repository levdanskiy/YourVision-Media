# FACTCHECK RULES

Almanac can sound poetic, but factual load-bearing points must be checkable.

## Claims That Require Verification

- Astronomical data: solstices, equinoxes, moon phases, sunrise/sunset, day length.
- Calendar dates: Christian movable feasts, national holidays, local observances, sabbats.
- Etymology: original forms, roots, language families, cognates.
- Historical claims: first uses, centuries, named inventors, publication years, ritual disappearance.
- Botanical and food chemistry claims: bloom windows, aromatic compounds, temperatures, storage safety.
- Direct quotations: exact text, author, title, year or edition context.
- Living or current events: competitions, releases, schedules, public events.

## Source Quality

Prefer:

- primary texts for quotations;
- official calendars or observatory/time services for dates and astronomy;
- museum, university, encyclopedia, or publisher pages for historical context;
- specialist dictionaries or academic sources for etymology;
- food science or professional baking references for technical process.

Avoid:

- unsourced social posts;
- AI-generated summaries as sources;
- repeating one blog's claim without a second confirmation;
- exact dates for folk practice when only a seasonal range is defensible.

## Metadata Recommendation

For new or revised posts, add a short source note in service metadata:

```text
// FACTCHECK: timeanddate solstice table; OED etymology; primary text checked
```

If a claim is evocative but uncertain, write it as tradition or version, not fact:

- Better: `в латышской традиции это связывают с...`
- Risky: `латыши всегда делали...`

## Correction Policy

Use `03_REPORTS/CORRECTIONS.md` for meaningful corrections after publication:

```text
2026-06-21 - AL-21.06-18-02-WHEEL-Lita
Issue: ...
Correction: ...
Public correction needed: yes/no
```

Correction levels:

| Level | Use | Action |
|-------|-----|--------|
| Typo | Misspelling that does not change meaning. | Edit silently if unpublished; if published, edit without report unless repeated. |
| Clarity | Ambiguous wording, weak source phrasing, missing caveat. | Edit and log if published. |
| Factual | Wrong date, source, quote, mechanism, attribution, safety-relevant food claim. | Edit, log in `CORRECTIONS.md`, and mark public correction needed if readers could be misled. |
| Structural | Wrong rubric/slot/status or regional-anchor framing. | Fix file and log if already published. |

Never delete a published post to hide a factual correction. Corrections are part of trust.
