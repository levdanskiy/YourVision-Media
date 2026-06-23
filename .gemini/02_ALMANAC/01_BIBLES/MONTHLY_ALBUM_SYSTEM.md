# MONTHLY ALBUM SYSTEM

Effective from `2026-07` as a pilot.

The monthly album is a derivative product: a PDF, carousel pack, Telegram album,
or long-form archive note assembled from published posts. It does not replace
the daily rhythm.

---

## Purpose

Turn the month into a collectible archive:
- best objects;
- strongest sources;
- food techniques;
- calendar thresholds;
- oracle/radar traces;
- reader archive leads;
- one editorial thesis for the month.

The album should feel like a field file, not a newsletter dump.

---

## Cadence

| Moment | Action |
|--------|--------|
| Last 3 days of month | Select objects and proof receipts. |
| Last day or first 2 days next month | Draft album. |
| First week next month | Publish derivative or `SV MONTHLY-ALBUM` note if useful. |

If announced in Telegram, use one `SV MONTHLY-ALBUM` and count it as one of the
week's required oracle/radar service pair.

---

## Album Structure

Minimum viable album:

```text
Title: Almanac: [Month] Field File

1. Thesis of the month - 1 paragraph
2. 12 objects - one line each
3. 4 food technologies - test + post link
4. 4 calendar thresholds - date + mechanism
5. 3 source receipts - source + why it mattered
6. Oracle/radar trace - what the service layer noticed
7. Reader archive lead - only if permission/privacy is clear
8. Next month - 3 routes
```

Optional stronger version:
- 24-36 pages;
- one object per page;
- image/prompt/alt text;
- short source receipt;
- QR/link to Telegram post;
- no long essays.

---

## Selection Rules

Pick for variety, not popularity only:
- at least 3 cultural zones;
- at least one non-European myth/source;
- at least one food process, not only sweets;
- at least one calendar/ritual;
- at least one proof-heavy post;
- at least one quiet post that did not chase trend.

Do not include:
- factually uncertain claim without caveat;
- reader detail without permission;
- AI-generated image presented as real archive;
- weak post just to fill a category.

---

## `SV MONTHLY-ALBUM` Template

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-MONTHLY-ALBUM-[MONTH]
// ТЕМА: monthly album release
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, MONTHLY-ALBUM
// СТАТУС: ГОТОВ

Собрали месяц в один field file:

12 объектов.
4 пищевые технологии.
4 календарных порога.
3 source receipts.

→ [Link / note where the album lives.]
```

---

## Storage

Use:

```text
03_REPORTS/monthly/YYYY-MM-Monthly-Album.md
03_ASSETS/monthly/YYYY-MM/
```

The markdown file is the source. PDF/carousel exports are derivatives.
