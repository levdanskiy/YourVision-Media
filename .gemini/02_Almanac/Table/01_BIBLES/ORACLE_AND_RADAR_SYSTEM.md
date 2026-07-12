# ORACLE AND RADAR SYSTEM

Effective from `2026-07-10`.
Standalone oracle/radar service leaves Almanac from `2026-07-23` by `RECIPE_ONLY_SYSTEM.md`.
Continue these formats in `Almanac: Calendar` (`https://t.me/AlmanacCalendar`,
project `/home/levdanskiy/.gemini/05_Almanac: Calendar`).

This document controls two weekly service formats:
- `SV ORACLE-NOTE` - weekly symbolic forecast layer;
- `SV CALENDAR-RADAR` - weekly calendar/holiday radar.

They are not `AL` posts and do not create a fourth daily post.

From `2026-07-23`, do not create standalone Almanac `SV ORACLE-NOTE` or
`SV CALENDAR-RADAR`. Route them to Almanac: Calendar. In Almanac, use recipe-service formats instead:
`MENU-RADAR`, `SHOPPING-LIST`, `TECHNIQUE-POLL`, `RECIPE-INDEX`, `PREP-NOTE`.

---

## Position

Almanac can use real forecast formats because tarot, astrology, omens and
calendar lists are culturally active now. The format is allowed to feel like a
forecast, but it must stay editorially honest:

- not medical, financial, legal, fertility, death or relationship advice;
- not deterministic;
- not a claim that the future is factually known;
- not fear-based selling;
- not a substitute for `#DIVINATION` research posts.

Correct framing:

```text
Оракул недели - не приказ, а карта внимания.
```

Wrong framing:

```text
Звёзды требуют. Карты обещают. Это точно случится.
```

---

## Weekly Cadence

From the ISO week `20-26.07.2026`, service load was exactly `2 SV` per week through `2026-07-22`: one forecast and one calendar radar. From `2026-07-23`, this obligation is owned by Almanac: Calendar, not Almanac.

| Week Object | Default Day | Time | Type | Rule |
|-------------|-------------|------|------|------|
| Oracle week | Monday/Thursday | `12:04` | `SV ORACLE-NOTE` | Exactly 1 per ISO week. |
| Calendar radar | Monday/Tuesday or previous useful day | `12:04` | `SV CALENDAR-RADAR` | Exactly 1 per ISO week. |

Direction pulse, recap, reader note and series navigation no longer replace this pair. Fold them into the relevant radar/oracle post, move them to a justified `SP`, or omit them. Never publish three `SV` posts in one ISO week.

---

## Oracle Rotation

Use one mode per week. Do not mix all systems in one note.

| Mode | Frequency | Structure |
|------|-----------|-----------|
| `ZODIAC_WEEK` | 1 time per month | 12 signs, one short line each, or 4 elements if the week is dense. |
| `TAROT_WEEK` | 1 time per month | 1-3 cards: background / tension / question. Name deck/source family. |
| `OMEN_WEEK` | 1 time per month | One seasonal omen or superstition as the week's lens. |
| `ORACLE_SYSTEM` | 1 time per month | I Ching, rune, lot, moon phase, bibliomancy, cowrie, etc. |

Allowed forecast language:
- tone of week;
- attention point;
- friction;
- threshold;
- useful question;
- small observational action.

Forbidden forecast language:
- `вам выпадет`;
- `вы встретите`;
- `вы потеряете`;
- `вы заработаете`;
- `вы заболеете`;
- `отношения решатся`;
- `карты требуют`;
- `звёзды требуют`;
- `точно`, `гарантированно`, `неизбежно`, `предначертано`.

### Zodiac Week Template

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-ORACLE-NOTE-Zodiac-Week
// ТЕМА: oracle week / zodiac forecast
// FORMAT_SUBTYPE: ZODIAC_WEEK
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, ORACLE-NOTE
// СТАТУС: ГОТОВ

Оракул недели: [краткая небесная/календарная рамка].

Овен - [1 short symbolic line].
Телец - [1 short symbolic line].
...
Рыбы - [1 short symbolic line].

→ Не обещание, а способ заметить, где неделя меняет давление.
```

### Tarot Week Template

```text
Оракул недели: [Card 1] / [Card 2] / [Card 3].

Фон - ...
Напряжение - ...
Вопрос - ...

→ [One reflective action, not advice.]
```

---

## Calendar Radar Rotation

`SV CALENDAR-RADAR` gives the reader a weekly map of interesting holidays,
observances and ritual dates. It does not replace `21:04 #CALENDAR`, `#FEAST`,
`#MODERN`, `#WHEEL` or `#RITES`.

Use 3-7 items:
- one major global/cross-cultural item if present;
- one lesser-known living calendar item;
- one modern/internet/institutional observance when relevant;
- one food/feast route if it can later become a 15:04 or 21:04 post;
- exact date system: Gregorian, lunar, Hijri, Hebrew, liturgical, national,
  regional, modern/institutional.

Calendar radar must be source-checked before publication. If a date depends on
moon sighting, local religious authority, timezone or regional calendar, write:

```text
date varies by local sighting/calendar.
```

### Calendar Radar Template

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-CALENDAR-RADAR-Week-Ahead
// ТЕМА: calendar radar / week ahead
// FORMAT_SUBTYPE: WEEK_AHEAD
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, CALENDAR-RADAR
// СТАТУС: ГОТОВ

На неделе впереди:

1. [Дата] - [observance]: [one line].
2. [Дата] - [observance]: [one line].
3. [Дата] - [observance]: [one line].

→ Полный пост получит [strongest route].
```

---

## July 2026 Application

Existing service posts remain:
- `07.07 12:04` - `SV DIRECTION-PULSE`;
- `10.07 12:04` - `SV CALENDAR-RADAR`;
- `13.07 12:04` - `SV ORACLE-NOTE`.

Planned continuation through the recipe pivot:

| Week | Oracle | Radar | Note |
|------|--------|-------|------|
| `13-19.07` | `13.07 ORACLE-NOTE` | none | Do not add recap on `19.07` unless oracle/radar is skipped. |
| `20-26.07` | route to Almanac: Calendar from `23.07` | `21.07 CALENDAR-RADAR` | Recipe-only pivot moves the planned oracle out of Almanac. |
| `27-31.07` | none | use `27.07 MENU-RADAR` if needed | Recipe-service only. |

From August, Almanac uses recipe-service only. Standalone forecasts and
calendar radar belong to Almanac: Calendar.
