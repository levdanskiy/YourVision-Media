# PROOF OF WORK SYSTEM

Effective from `2026-07-17`.

Almanac competes against smooth generic content by showing evidence of work:
source, object, translation choice, technique test, date mechanism, or visual
receipt. The goal is not academic heaviness. The goal is trust.

---

## Core Rule

Every fact-heavy `AL` post should contain at least one visible proof element.
High-risk posts should contain three.

High-risk means:
- primary text or translation claim;
- etymology;
- historical date;
- religious or ritual claim;
- food origin claim;
- divination history;
- Indigenous or living-community material;
- health/safety/temperature/food-science claim.

---

## Proof Shapes

| Shape | Use In | What It Looks Like |
|-------|--------|--------------------|
| `SOURCE RECEIPT` | `SOURCE`, `LORE`, `DIVINATION`, `CALENDAR` | Edition, translator, year, page/chapter, why this version. |
| `THREE RECEIPTS` | `MODERN`, `HERITAGE`, `CALENDAR`, `SOURCE` | 3 dated facts in short proof-card form. |
| `TECHNIQUE TEST` | food posts | Temperature, texture, sound, failure point, sensory readiness. |
| `DATE MECHANISM` | `CALENDAR`, `WHEEL`, `CYCLES`, `CHRONOS` | Exact calendar system, conversion, timezone, lunar/local caveat. |
| `TRANSLATION NOTE` | `SOURCE`, `ETYMON`, `PROSE` | Original word/phrase, why common translation is narrow or misleading. |
| `OBJECT RECEIPT` | `OBJECTS`, `TOOLS`, `BESTIARY`, `PERSONAE` | Material, image/source family, museum/catalogue/field source. |

---

## In-Post Blocks

Use sparingly. One proof block is enough unless the post is dense.

```text
SOURCE RECEIPT
Text: [source / edition / translator / year]
Anchor: [chapter/page/line/object]
Why this version: [one sentence]
```

```text
THREE RECEIPTS
1. [date/source/fact]
2. [date/source/fact]
3. [date/source/fact]
```

```text
TECHNIQUE TEST
Ready when: [sensory marker]
Fails when: [failure marker]
Why: [mechanism]
```

---

## Service Layer

Use `SV SOURCE-NOTE` when the source choice is interesting enough to stand
alone but too heavy for the core post.

Best cases:
- disputed translation;
- several versions of one myth;
- named collector or informant;
- deck/image rights note;
- calendar conversion;
- food origin dispute.

Template:

```text
// ИД-ПОСТА: SV-[ДД.ММ]-12-04-SOURCE-NOTE-[SLUG]
// ТЕМА: source receipt
// ДАТА ПУБЛИКАЦИИ: [ДД.ММ.ГГГГ, 12:04] (PUBLICATION_TIMEZONE)
// ПРОТОКОЛЫ: Almanac, SERVICE, SOURCE-NOTE
// СТАТУС: ГОТОВ

Почему взята эта версия:

[Source / edition / date / reason.]

→ [What changes if another version is used.]
```

---

## Anti-Slop Rules

Do:
- show one concrete source or material detail early;
- name uncertainty when it exists;
- separate legend from documented history;
- use "one version says" when tradition varies.

Do not:
- fake precision;
- overcite obvious claims;
- hide weak evidence behind poetic language;
- use "ancient people believed" without naming corpus/source;
- use AI-generated images as historical evidence.
