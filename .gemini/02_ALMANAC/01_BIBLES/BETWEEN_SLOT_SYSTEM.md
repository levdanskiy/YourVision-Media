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
| `12:04` | `SV` | Exactly 2 per week from 20.07.2026 | Required oracle + calendar radar pair. |
| `18:04` | `SP` or rare `SV` | 2-4 per month for `SP` | Threshold/special between food and evening: major date, strong series bridge, visual/audio event. |
| `08:34`, `14:34`, `20:34` | Story/external | optional | Teaser frame, poll sticker, behind-the-post visual. Not archived as `AL`. |

Do not use `06:04`, `00:04`, or extra night slots by default. Almanac should
feel precise, not noisy.

---

## Best Fillers

| Format | Prefix | Best Slot | What It Does |
|--------|--------|-----------|--------------|
| Weekly oracle | `SV ORACLE-NOTE` | `12:04` Monday/Thursday | Zodiac, tarot, omen, rune/I Ching as symbolic forecast. |
| Week-ahead calendar | `SV CALENDAR-RADAR` | `12:04` Monday/Tuesday or useful lead day | 3-7 holidays/observances ahead. |
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

Default week:

```text
12:04 Monday/Thursday - SV ORACLE-NOTE
12:04 Friday/useful lead day - SV CALENDAR-RADAR
```

Required-pair rule:
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
| Week 1 | `ORACLE-NOTE` | `CALENDAR-RADAR` | `SP` only if Lammas needs bridge. |
| Week 2 | `ORACLE-NOTE` | `CALENDAR-RADAR` | Quiz may be embedded, not substituted. |
| Week 3 | `ORACLE-NOTE` | `CALENDAR-RADAR` | Reader memory may be embedded, not substituted. |
| Week 4 | `ORACLE-NOTE` | `CALENDAR-RADAR` | End-month recap only if it replaces one. |

This gives rhythm without turning Almanac into a notification machine.
