---
name: novells-writer
description: Автор тёмных нарративов Novells (кроме Eleyia). KINGMAKER — политический триллер, DONOR — вампирское bio-право. Жанровый ДНК, сцены, диалоги, визуальные промпты.
---

# 🖤 Novells Writer V1.0 (Тёмные Нарративы)

Этот навык обслуживает проекты KINGMAKER и DONOR — политический триллер и биопанк с вампирской механикой. Для Eleyia использовать отдельный `eleyia-writer`.

---

## 🏛 KINGMAKER — ПОЛИТИЧЕСКИЙ ТРИЛЛЕР

**Концепт:** Информационные войны, борьба за власть, биометрический контроль. Власть передаётся не по крови — по данным.

**Тон:** Холодный. Расчётливый. Никакого героизма — только прагматика и манипуляция. Диалоги как допрос: каждое слово — позиция.

**Запрещено:** Случайные совпадения, наивные персонажи, открытые эмоции без тактической цели. Никакого хэппи-энда.

**Ключевые слова:** `obsidian surfaces, heavy velvet drapes, cold strategic light, shadowed figures, political intrigue, closed cabinet rooms`

**Пресет диалогов:** `./ask-claude.sh` с пресетом **KM_INTERROGATE** — "Напиши диалог как политический допрос. Каждая реплика — скрытая угроза или торг. Никаких лишних слов."

---

## 🩸 DONOR — ВАМПИРСКОЕ БИО-ПРАВО

**Концепт:** Мир, где кровь — валюта, а вампиры — законная элита. Доноры — класс, не жертвы. Система формально легальна, фактически — кабальна.

**Тон:** Экзистенциальная тревога под стерильной оболочкой. Клиническая точность описаний. Красота и ужас неотделимы.

**Запрещено:** Готическая клише-эстетика (плащи, замки), романтизация без ambiguity. Никакого "спасения" как финала.

**Ключевые слова:** `clinical white interiors, chrome surfaces, biotech aesthetic, antiseptic light, existential dread, sterile elegance`

**Пресет диалогов:** `./ask-claude.sh` с пресетом **DN_CLINICAL** — "Напиши сцену в стиле медицинского протокола: точность, дистанция, скрытое насилие под легальной формой."

---

## 🛠 КОГДА ИСПОЛЬЗОВАТЬ

- Написание глав, сцен, диалогов для KINGMAKER или DONOR.
- Генерация визуальных промптов Midjourney под сцену.
- Разработка новых персонажей в рамках установленного ДНК.
- Планирование арок и сюжетных поворотов.

## 🚫 КОГДА НЕ ИСПОЛЬЗОВАТЬ

- Eleyia — это `eleyia-writer`.
- YV-контент — это `yv-editor`.
- Технический рефакторинг бибилий — это `deepseek-bridge`.

---

## 📞 MIDJOURNEY — ОБЯЗАТЕЛЬНЫЙ ХВОСТ

**KINGMAKER:**
`no text, no logos, obsidian surfaces, heavy velvet drapes, cold strategic light, political intrigue, shadowed figures, shot on 35mm film Kodak Portra 800, heavy film grain, Dazed magazine aesthetic, cinematic realism --v 6.1 --style raw --s 750 --ar 1:1`

**DONOR:**
`no text, no logos, clinical white interiors, chrome surfaces, biotech aesthetic, sterile elegance, existential mood, shot on 35mm film Kodak Portra 800, heavy film grain, Dazed magazine aesthetic, cinematic realism --v 6.1 --style raw --s 750 --ar 1:1`

---

## 🔗 ИНТЕГРАЦИЯ

- `yv-asset-manager` — финальный контроль визуальных промптов.
- `brand-integrity-officer` — проверка тона перед публикацией.
- `cross-project-syndicator` — синдикация после публикации главы.
- Бибилии: `03_NOVELLS/02_KINGMAKER/01_BIBLES/KINGMAKER_BIBLE.md`, `03_NOVELLS/03_DONOR/01_BIBLES/DONOR_BIBLE.md`
