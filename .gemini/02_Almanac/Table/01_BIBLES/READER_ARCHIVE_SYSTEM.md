# READER ARCHIVE SYSTEM

Effective from `2026-08-01`, with pilots allowed from late July.

Reader material is a living lead, not a verified source. Almanac may collect
memories, household practices, words, foods, omens, and calendar habits from
readers, but must verify or clearly label them before reuse.

---

## Cadence

| Format | Frequency | Prefix | Rule |
|--------|-----------|--------|------|
| Reader prompt | max 1 per month | `SV READER-NOTE` | One precise question. |
| Curated response | max 1 per month | `SV READER-NOTE` | Anonymous unless permission is explicit. |
| Follow-up AL post | as earned | `AL` | Only after source-checking. |

Through `2026-07-22`, if a month uses a reader prompt, it replaces one weekly
`SV ORACLE-NOTE` or `SV CALENDAR-RADAR`. From `2026-07-23`, non-recipe reader
prompts route to Almanac: Calendar; Almanac reader prompts must be recipe-memory or
technique-memory only.

---

## What To Ask

Good prompts:
- family omen around food, threshold, mirror, salt, birds, weather;
- household bread, soup, preserve, sauce, fasting dish;
- local name for a season, plant, wind, holiday, tool;
- object nobody threw away;
- calendar practice: how a family knew a holiday was near;
- sound or smell that marked a month.

Bad prompts:
- "tell us everything";
- trauma mining;
- private religious confession;
- medical, legal, financial, fertility or death details;
- ranking cultures or families;
- identity bait: "what myth creature are you?".

---

## Reader Note Template

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-READER-NOTE-[SLUG]
// ТЕМА: reader archive prompt
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, READER-NOTE
// СТАТУС: ГОТОВ

Reader Archive:

[One precise question.]

Можно ответить одним словом, запахом, предметом или короткой сценой.
Имена, адреса и частные детали не нужны.
```

---

## Verification Pipeline

Reader response stages:

```text
RECEIVED -> ANONYMIZED -> TAGGED -> SOURCE_CHECKED -> USABLE / PRIVATE / REJECTED
```

Metadata for internal notes:

```yaml
reader_archive_id:
received_date:
topic:
zone_if_known:
privacy: anonymous / permission_named / private
claim_type: memory / recipe / omen / date / word / object
verification_status: unverified / checked / unusable
source_followup:
usable_in:
```

---

## Use In Posts

Allowed phrasing:

```text
Один читатель вспомнил семейную формулу. Это не источник факта, а след практики.
```

Forbidden phrasing:

```text
Наши читатели доказали, что...
```

Reader memories can become:
- a lead for `OMENS`;
- a foodways question;
- a source note;
- a monthly album object;
- a future poll option;
- a clue for database/source research.

They cannot become:
- proof of origin;
- medical advice;
- a named cultural claim without verification;
- content published with identifying details.
