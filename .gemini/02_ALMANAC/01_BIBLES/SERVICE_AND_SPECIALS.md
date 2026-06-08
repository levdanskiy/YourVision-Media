# SERVICE AND SPECIALS

Effective from `2026-07-07`.

This layer adds interaction and modern channel navigation without creating a fourth daily Almanac post.

## Core Rule

The daily Almanac contract remains exactly three `AL` posts:
- `10:04`
- `15:04`
- `18:02`

Service notes and special posts are optional overlays. They do not count as daily `AL` posts and must not be named `AL-*`.

## File Prefixes

| Prefix | Use | Counts As Daily Post |
|--------|-----|----------------------|
| `SV` | Service note: poll, recap, direction pulse, series navigation. | No |
| `SP` | Rare special slot at `21:04` for major dates or strong series. | No |

Filename format:

```text
SV-DD.MM-HH-MM-TYPE-Slug.md
SP-DD.MM-21-04-TYPE-Slug.md
```

Storage rule: place `SV` and `SP` files in the same day folder as the core
`AL` posts, so the whole publishing package is visible in one directory.
They remain separate overlays because their filenames do not start with `AL-`.

Examples:

```text
SV-07.07-12-04-DIRECTION-PULSE-After-First-Week.md
SV-12.07-12-04-SERIES-NAV-July-Routes.md
SP-31.07-21-04-LAMMAS-EVE-Threshold.md
```

## Service Notes

Frequency: 1-2 per week.

Allowed types:
- `POLL` - specific native poll, never engagement bait.
- `DIRECTION-PULSE` - what to strengthen in the channel.
- `RECAP` - short weekly recap.
- `SERIES-NAV` - navigation through a multi-post series.
- `SOURCE-NOTE` - short source/process note when useful.
- `AUDIO-NOTE` - 60-90 second voice/audio reading or field note, max once every two weeks.
- `ARCHIVE-NOTE` - route back to an older post/series with new context, not nostalgia.
- `COLLAB-NOTE` - guest/source/process note with named expertise and clear boundaries.
- `VISUAL-ESSAY` - 3-5 image sequence plan/caption set, no long article.
- `READER-NOTE` - reader memory/field note prompt or curated response, max once per month.
- `ORACLE-NOTE` - symbolic day/week/month reading, max twice per month during test.
- `CALENDAR-RADAR` - compact list of holidays/observances for today/week/month.

Length:
- 400-900 characters.
- No visual prompt required.
- No Grade required.
- No heavy source apparatus unless it makes a factual claim.

Tone:
- editorial, calm, precise;
- no “like/share/comment”;
- no apology;
- no marketing language.

Template:

```text
// ИД-ПОСТА: SV-[ДД.ММ]-[ЧЧ-ММ]-[TYPE]-[SLUG]
// ТЕМА: [service purpose]
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, ЧЧ:ММ] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, [TYPE]
// СТАТУС: ГОТОВ

[One concise editorial note.]

[If poll: 2-4 concrete options.]
```

## Direction Pulse

Use once per month after the first 10-14 `AL` posts are published and audited.

For July 2026, the first direction pulse is allowed from `2026-07-07`, because `2026-07-01` through `2026-07-06` are already prepared and `2026-07-07` has not been sent to scheduled Telegram posting.

Recommended poll:

```text
📊 Что усилить дальше?
Герои как досье / Существа и предметы / Еда за пределами выпечки / Праздники через стол
```

## Weekly Recap

Use once per week max.

Structure:
- 3-5 lines;
- one line per thread;
- point to next week, not backward nostalgia.

Do not summarize every post. Recap reveals pattern, not inventory.

## Series Navigation

Use when a series has at least 3 connected posts.

Allowed:
- midsummer cluster;
- divination sequence;
- foodways/pantry/drinks opening sequence;
- personae/bestiary/object dossier sequence;
- Lammas/Early harvest sequence.

## Audio Notes

Use `SV AUDIO-NOTE` only when sound adds evidence:
- reading a source line;
- pronouncing a word in an etymology;
- hearing bread crackle, syrup thread, rain on dry soil, or field sound;
- a 60-90 second seasonal note.

Never improvise facts in audio. The text source remains the authority.

## Archive And Visual Service

`SV ARCHIVE-NOTE` can route readers to a previous post when a new date changes its meaning.

`SV VISUAL-ESSAY` can plan or caption 3-5 images when the visual sequence explains a process better than another text post.

## Reader Notes

Use `SV READER-NOTE` when the channel needs lived material without turning the
core post into a comment request.

Allowed:
- one precise question: family omen, household bread, market smell, fasting dish, local calendar practice;
- one curated anonymous response, if permission is clear;
- one follow-up source lead for later verification.

Rules:
- reader memory is not a fact source until checked;
- no full names, addresses, private medical/religious details, or identifying family conflict;
- no ranking of cultures, countries, religions, or families;
- max once per month unless an analytics review explicitly approves more.

## Oracle Notes

Use `SV ORACLE-NOTE` only as a clearly symbolic editorial layer. It may feel like
an actual reading, but it must not claim factual knowledge of the future.

Allowed:
- "карта/знак/примета недели" as a cultural lens;
- one tarot card, rune, I Ching hexagram, moon phase, omen, or zodiac weather;
- day/week/month tone: attention, friction, threshold, useful question;
- a small reflective action: observe, compare, write down, ask, wait.

Rules:
- max twice per month while testing;
- no personal predictions by sign;
- no "you will meet / lose / earn / recover";
- no medical, financial, legal, romantic, fertility, death, or fate advice;
- no deterministic language: "точно", "неизбежно", "предначертано";
- source the system if a named card, rune, hexagram, sign, or omen is used.

Template:

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-ORACLE-NOTE-[SLUG]
// ТЕМА: symbolic oracle note
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, ORACLE-NOTE
// СТАТУС: ГОТОВ

[One symbolic card/sign/omen.]

[What it makes visible this day/week/month.]

→ [One reflective action, not advice.]
```

## Calendar Radar

Use `SV CALENDAR-RADAR` for compact lists like "today in calendars", "this
week's observances", or "month ahead".

Allowed:
- 3-7 dates or observances;
- one-line explanation each;
- exact date system when relevant: Gregorian, lunar, Hijri, Hebrew, liturgical,
  national, modern/institutional;
- note "verify local date" when moon sighting, regional calendar, or timezone
  matters.

Rules:
- this is navigation, not a replacement for `18:02 CALENDAR`;
- no ranking of religions, countries, cultures, or political memories;
- major items can become full `AL` posts later;
- factual dates require source checking before publication.

Template:

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-CALENDAR-RADAR-[SLUG]
// ТЕМА: calendar radar
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, CALENDAR-RADAR
// СТАТУС: ГОТОВ

На этой неделе:

1. [Дата] - [observance]: [one line, source-checked].
2. [Дата] - [observance]: [one line, source-checked].
3. [Дата] - [observance]: [one line, source-checked].

→ [Which route will get a full post.]
```

## 21:04 Special Slot

Frequency: 2-4 per month max.

Use only for:
- major calendar thresholds;
- strong myth-cycle finale;
- solstice/equinox/Wheel points;
- Lammas, Halloween, New Year-type dates;
- one-off editorial event that cannot fit inside the three-post day.

Length:
- 900-1600 characters.
- Visual prompt optional but recommended.
- Must feel like a night note, threshold, or afterimage.

Never use `21:04` to compensate for weak planning. If the idea fits `10:04`, `15:04`, or `18:02`, it goes there.

Template:

```text
// ИД-ПОСТА: SP-[ДД.ММ]-21-04-[TYPE]-[SLUG]
// ТЕМА: [special threshold]
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 21:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SPECIAL
// СТАТУС: ГОТОВ

[Night hook.]

[One source/mechanism paragraph.]

[One image or threshold.]

→ [quiet final line.]

---
`⏱ [X.X] мин | Almanac: Special`
```

## July 2026 Application

Start from `2026-07-07`.

| Date | Type | Purpose |
|------|------|---------|
| `07.07 12:04` | `SV DIRECTION-PULSE` | Ask what to strengthen now that new rules start. |
| `10.07 12:04` | `SV CALENDAR-RADAR` | Start calendar radar: upcoming observances and calendar nodes. |
| `13.07 12:04` | `SV ORACLE-NOTE` | Start symbolic oracle note: one non-predictive weekly lens. |
| `19.07 12:04` | `SV RECAP` | Mid-July pattern recap. |
| `31.07 21:04` | `SP` | Lammas Eve / first harvest threshold. |

Optional only if a week needs it:
- `SP` for a strong myth-cycle finale.
- `SV SOURCE-NOTE` if a post uses a difficult corpus.

## Validation Policy

`SV` and `SP` files are not checked by daily `AL` preflight.

They must still obey:
- no engagement bait;
- no regional default anchor;
- no personal divination advice;
- no medical/financial/legal advice;
- no unreadable text/logos in prompts if a prompt exists.
