# STORY LAYER SYSTEM

Effective from `2026-07-17`.

Stories are a derivative layer, not a second feed and not an archive substitute.
The archived source of truth remains the daily folder with `AL`, `SV`, and `SP`
files.

---

## Cadence

| Story Type | Frequency | Best Time | Purpose |
|------------|-----------|-----------|---------|
| Teaser Frame | 1-2 per week | `08:34` | One object/source before a strong `09:04` post. |
| Process Frame | 1 per week max | `14:34` | Food texture, tool, dough, syrup, steam, cut, crumb. |
| Route Frame | 1 per week max | `20:34` | Tonight's calendar route or tomorrow's threshold. |
| Poll Sticker | 1 per week max | any story slot | One observation or direction question. |
| Audio Story | 1 per two weeks max | `12:04`/story | Pronunciation, source line, bread crackle, field sound. |

Do not publish daily stories by default. A story must add one of these:
- evidence;
- sound;
- navigation;
- a poll that changes editorial judgment;
- a visual object that cannot fit cleanly into the core post.

---

## Templates

### Teaser Frame

```text
STORY: TEASER-FRAME
TIME: 08:34
LINKED_POST: AL-[date]-09-04-[rubric]-[slug]

Visual: [one object, crop, texture, source/page/detail]
Caption: [one line, no explanation]
Sticker: none / reaction
```

Example:

```text
Visual: a card corner, one hand, matte black table, no text.
Caption: Сегодня карта не отвечает. Она показывает, кто спрашивает.
```

### Process Frame

```text
STORY: PROCESS-FRAME
TIME: 14:34
LINKED_POST: AL-[date]-15-04-[rubric]-[slug]

Visual: [texture/process proof]
Caption: [one sensory test]
Sticker: optional poll with 2-4 concrete options
```

### Route Frame

```text
STORY: ROUTE-FRAME
TIME: 20:34
LINKED_POST: AL-[date]-21-04-[rubric]-[slug]

Visual: [calendar/object/threshold]
Caption: [one route line]
Sticker: optional reaction
```

---

## Visual Rules

Stories should look like evidence, not advertising:
- close crop;
- object or process in frame;
- no stock-like background;
- no fake ancient parchment;
- no text embedded in generated image;
- no ranking or comparison that flattens cultures.

Good story objects:
- card edge;
- handwritten source note;
- crumb shot;
- spoon surface;
- calendar mark;
- object shadow;
- source page corner;
- one tool in use.

Bad story objects:
- generic mystical smoke;
- glowing zodiac wheel without source;
- AI-fantasy deity portrait;
- decorative collage with unreadable text;
- "new post" banner.

---

## Archiving

Stories are not required in `02_CONTENT`, but when a story carries a source,
claim, poll result, or useful visual route, record it in the day folder as:

```text
STORY-DD.MM-HH-MM-[TYPE]-[Slug].md
```

This is optional documentation, not an `AL`/`SV` post.

Template:

```text
// ИД-ПОСТА: STORY-[ДД.ММ]-[ЧЧ-ММ]-[TYPE]-[SLUG]
// LINKED_POST: AL-[...]
// СТАТУС: PLANNED / POSTED

Visual:
Caption:
Sticker:
Result, if poll:
```

---

## Safety

No private reader screenshots without permission.
No invented source pages.
No health, finance, legal, fertility, death, or relationship predictions.
No "boost/share/comment" language.
