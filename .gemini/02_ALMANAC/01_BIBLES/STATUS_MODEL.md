# STATUS MODEL

Use one of these statuses in post metadata and planning files.

| Status | Meaning |
|--------|---------|
| `IDEA` | Seed only. Topic, angle, or source exists, but no post body. |
| `DRAFT` / `ЧЕРНОВИК` | Written but not yet checked against rubric, facts, length, or prompt rules. |
| `NEEDS_FACTCHECK` | Content contains claims that require verification before scheduling. |
| `NEEDS_REWRITE` | Structure or voice does not meet current Almanac rules. |
| `READY` / `ГОТОВ` | Passed rubric, voice, length, prompt, and fact checks. Ready to schedule. |
| `SCHEDULED` | Loaded into the publishing queue. |
| `PUBLISHED` | Published. Do not edit silently; use `CORRECTIONS.md` for meaningful changes. |
| `CORRECTED` | Published and meaningfully corrected with an incident/correction record. |
| `ARCHIVE` | Kept for reference, not part of the active calendar. |

The file status describes editorial readiness. Actual queue/publication state lives in `04_DATABASES/PUBLICATION_REGISTRY.json`; update it through `python3 tools/almanac publications ...`. Imported records use `state_source: content_import` and are not Telegram-verified. A `READY` file is not proof that Telegram published it.

## Ready Criteria

A post may be marked `READY` / `ГОТОВ` only when:

- required metadata is present;
- slot matches rubric family;
- no forbidden dash or visual prompt flags are present;
- body length fits the rubric limit in `RUBRIC_RULES.md`;
- factual claims that need verification have source confidence;
- visual prompt exists and ends with `shot on 35mm film Kodak Portra 800`;
- final line is an action, image, question, or silence, not a moral.

## Recommended YAML Frontmatter

Existing `//` metadata can stay, but new posts should prefer frontmatter because it is easier to audit.

```yaml
---
id: AL-29.05-15-04-BUNS-Elderflower
date: 2026-05-29
time: "15:04"
timezone: PUBLICATION_TIMEZONE
rubric: BUNS
status: READY
grade: A
image_status: needed
published: false
cultural_zone: Europe
coverage_axis: sweet dough
source_type: food_history
---
```

For new workflow use:

```bash
python3 tools/almanac publications sync
python3 tools/almanac publications set POST_ID scheduled --scheduled-at 2026-07-21T09:04:00+03:00
python3 tools/almanac publications set POST_ID published --telegram-message-id 123 --channel @channel
```
