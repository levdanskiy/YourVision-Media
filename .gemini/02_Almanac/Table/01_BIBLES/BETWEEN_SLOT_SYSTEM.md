# BETWEEN SLOT SYSTEM

Effective from `2026-07-17`.

Core posts stay fixed:

```text
09:04 - core AL
15:04 - core AL, food only
21:04 - core AL
```

Free space between them is not a second content feed. It is a light service
layer used only when it gives navigation, interaction, sound, visual evidence,
or a real calendar/oracle reason.

---

## Slot Map

| Time | Layer | Frequency | Use |
|------|-------|-----------|-----|
| `12:04` | `SV` | Through 22.07: exact service pair. From 23.07: 0-2 recipe-service/week. | Before pivot: oracle + calendar radar. After pivot: recipe navigation only; non-recipe service moves to Almanac: Calendar. |
| `18:04` | `SP` or rare `SV` | 2-4 per month for `SP` | Threshold/special between food and evening: major date, strong series bridge, visual/audio event. |
| `08:34`, `14:34`, `20:34` | Story/external | optional | Teaser frame, poll sticker, behind-the-post visual. Not archived as `AL`. |

Do not use `06:04`, `00:04`, or extra night slots by default. Almanac should
feel precise, not noisy.

---

## Best Fillers

| Format | Prefix | Best Slot | What It Does |
|--------|--------|-----------|--------------|
| Weekly oracle | `SV ORACLE-NOTE` through 22.07; Almanac: Calendar after 23.07 | `12:04` before pivot; Almanac: Calendar `08:44` after pivot | Zodiac, tarot, omen, rune/I Ching as symbolic forecast. |
| Week-ahead calendar | `SV CALENDAR-RADAR` through 22.07; Almanac: Calendar after 23.07 | `12:04` before pivot; Almanac: Calendar `23:11` after pivot | 3-7 holidays/observances ahead. |
| Native poll | `SV POLL` | `12:04` | Direction, preference, field observation. |
| Micro quiz | `SV QUIZ` | `12:04` | One source/fact question with answer reveal. Max once per month. |
| Source note | `SV SOURCE-NOTE` | `12:04` | Why a source/translation/version was chosen. |
| Audio note | `SV AUDIO-NOTE` | `12:04` or `18:04` | 60-90 seconds: source reading, word pronunciation, bread crackle, field sound. |
| Reader note | `SV READER-NOTE` | `12:04` | One precise memory prompt. Max once per month. |
| Visual essay | `SV VISUAL-ESSAY` | `18:04` | 3-5 image/caption sequence when images explain better than another text. |
| Monthly album | `SV MONTHLY-ALBUM` | `12:04` | Release note for field file/PDF/carousel. Max once per month. |
| Series nav | `SV SERIES-NAV` | `12:04` | Map a series after at least 3 connected posts. |
| Archive note | `SV ARCHIVE-NOTE` | `12:04` | Reopen an older post because the current date changed its meaning. |
| Special threshold | `SP` | `18:04` | Major date, cycle finale, Lammas/Halloween/New Year-type bridge. |

---

## Weekly Rule

Default week through 22.07:

```text
12:04 Monday/Thursday - SV ORACLE-NOTE
12:04 Friday/useful lead day - SV CALENDAR-RADAR
```

From 23.07 in Almanac:

```text
12:04 optional - SV MENU-RADAR / SHOPPING-LIST / RECIPE-INDEX / PREP-NOTE
```

From 23.07 in Almanac: Calendar:

```text
08:44 - omens, divination, astrology, forecast, fragments
23:11 - chronos, cycles, calendar, source, etymology, modern folklore
```

Required-pair rule through 22.07:
- `DIRECTION-PULSE`, `RECAP`, `SERIES-NAV`, `AUDIO-NOTE`, `READER-NOTE`, `MONTHLY-ALBUM`, and `QUIZ` do not replace oracle or radar; fold them into the pair, use a justified `SP`, or omit them;
- do not publish three `SV` notes in one ISO week;
- do not use `18:04` to rescue weak planning.

---

## Telegram-Native Ideas

Use native platform affordances when they add function:

- poll with media/context for one visual choice;
- quiz mode for one source or calendar fact;
- story reaction sticker for a one-tap mood check;
- story with audio for pronunciation or texture;
- short voice/audio when sound is evidence.

These are derivatives. The archived source of truth remains the day folder.

---

## August Default Pattern

| Week | `SV 1` | `SV 2` | Optional |
|------|--------|--------|----------|
| Week 1 | `MENU-RADAR` | `SHOPPING-LIST` | `SP` only if Lammas needs recipe bridge. |
| Week 2 | `TECHNIQUE-POLL` | `RECIPE-INDEX` | Quiz only if it teaches a cooking decision. |
| Week 3 | `PREP-NOTE` | `MENU-RADAR` | Reader memory only as recipe memory. |
| Week 4 | `RECIPE-INDEX` | `SHOPPING-LIST` | End-month recap only as recipe index. |

This gives rhythm without turning Almanac into a notification machine.
