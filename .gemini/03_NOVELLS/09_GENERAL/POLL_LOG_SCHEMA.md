// ИД-ФАЙЛА: POLL_LOG_SCHEMA
// ВЕРСИЯ: 1.0
// ТИП: ДОКУМЕНТАЦИЯ СХЕМЫ

# 🗳 POLL_LOG.json - схема

Структура файла `02_SYSTEM/POLL_LOG.json` в каждом проекте. Источник истины по опросам. `POLL_LOG.md` остаётся как человекочитаемая копия, генерируется из JSON.

См. [[NOVELLS_OS]] раздел 5, `tools/poll_log_render.py` для генерации .md из .json.

---

## ВЕРХНЕУРОВНЕВАЯ СТРУКТУРА

```json
{
  "version": "1.0",
  "project": "kingmaker",
  "season": 1,
  "last_updated": "2026-05-16",
  "polls": [ ... ]
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `version` | string | Версия схемы |
| `project` | string | Код проекта (kingmaker, vienna_special, orchid, etc.) |
| `season` | int | Номер сезона |
| `last_updated` | string | ISO дата последнего изменения (YYYY-MM-DD) |
| `polls` | array | Список опросов в хронологическом порядке |

---

## СТРУКТУРА ОДНОГО ОПРОСА

```json
{
  "id": "km-0-d1-q1",
  "phase": 0,
  "narrative_day": 1,
  "pub_date": "2026-05-05",
  "category": "setup",
  "question": "Кто она?",
  "options": [
    {"label": "Мужчина", "percent": 0, "votes": 0},
    {"label": "Женщина", "percent": 100, "votes": 1}
  ],
  "total_votes": 1,
  "winner": "Женщина",
  "winner_type": "absolute",
  "tie_resolution": null,
  "impact_scoreboard": "Параметр зафиксирован",
  "impact_content": "Все дальнейшие посты с Норой как женщиной",
  "stats_deltas": [],
  "post_id": null,
  "notes": null
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | string | Уникальный идентификатор: `{project_code}-{phase}-d{day}-q{seq}` |
| `phase` | int | Фаза: 0 = pre-story, 1/2/3 = фазы сезона, 4 = эпилог |
| `narrative_day` | int | Нарративный день |
| `pub_date` | string | Дата публикации (ISO YYYY-MM-DD) |
| `category` | string | `setup` / `live` / `black_velvet` / `endgame` |
| `question` | string | Текст вопроса |
| `options` | array | Опции с label, percent, votes |
| `total_votes` | int | Сумма голосов |
| `winner` | string | Победившая опция или описание ничьи |
| `winner_type` | enum | `absolute` (>50%), `unanimous` (100%), `tie` (равно), `plurality` (большинство, но не 50%) |
| `tie_resolution` | string\|null | Если ничья - как ГГ решила (третий путь) |
| `impact_scoreboard` | string | Влияние на котировки / параметры |
| `impact_content` | string | Влияние на следующие посты |
| `stats_deltas` | array | Машиночитаемые изменения STATS.json - см. ниже |
| `post_id` | string\|null | Имя файла поста, в котором был опрос |
| `notes` | string\|null | Свободные заметки |

---

## STATS_DELTAS

Каждый delta - объект:

```json
{
  "character": "adrian",
  "param": "reputation",
  "delta": +0.8,
  "reason": "Слив Black Velvet вскрыл скрытые блоки"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `character` | string | ID персонажа из `STATS.json` (lowercase: `adrian`, `theodora`, etc.) |
| `param` | enum | `reputation` или `affinity` |
| `delta` | float\|int | Изменение (±). Reputation в десятых, affinity целыми. |
| `reason` | string | Короткое объяснение |

---

## ID КОНВЕНЦИЯ

Формат: `{project_code}-{phase}-d{narrative_day}-q{seq}`

- `project_code`: `km`, `vs`, `or` (orchid), `dn` (donor), `od` (order), `hz` (horizon), `cd` (code), `at` (anthropos), `el` (eleyia)
- `phase`: 0 (pre-story setup), 1-3 (sezon phases), 4 (epilogue)
- `narrative_day`: число нарративного дня в проекте
- `seq`: q1, q2 - порядковый номер опроса в этом нарративном дне

Примеры:
- `km-0-d3-q2` - Kingmaker, pre-story, нарративный день 3, второй опрос
- `vs-1-d3-q1` - Vienna Special, Phase 1 (live week), нарративный день 3, первый опрос

---

## КАТЕГОРИИ ОПРОСОВ

- **`setup`** - предсезонные опросы конфигурации (пол ГГ, ориентация, стиль власти, и т.п.)
- **`live`** - стандартные сюжетные опросы в сезоне
- **`black_velvet`** - выбор цели / тона сливов (KM-специфичный)
- **`endgame`** - финальные опросы (фаза 3 финал, голосование)
- **`epilogue`** - постфинальные (фаза 4)

---

## РАБОЧИЙ ЦИКЛ ОБНОВЛЕНИЯ

1. Опрос закрылся → пользователь даёт результаты
2. Добавить запись в `POLL_LOG.json` (полная структура)
3. Применить `stats_deltas` к `STATS.json`
4. Обновить `last_updated` в обоих
5. (Опционально) Регенерировать `POLL_LOG.md` через `tools/poll_log_render.py <project>`

---

## ПРОСМОТР ТЕКУЩЕГО СОСТОЯНИЯ

```bash
# Все опросы проекта
jq '.polls[] | {id, day: .narrative_day, q: .question, winner}' \
  .gemini/03_NOVELLS/02_KINGMAKER/02_SYSTEM/POLL_LOG.json

# Последний опрос
jq '.polls | last' .gemini/03_NOVELLS/02_KINGMAKER/02_SYSTEM/POLL_LOG.json

# Опросы с ничьёй
jq '.polls[] | select(.winner_type == "tie")' \
  .gemini/03_NOVELLS/02_KINGMAKER/02_SYSTEM/POLL_LOG.json

# Суммарные деltas по персонажу
jq '[.polls[].stats_deltas[] | select(.character == "adrian")] | group_by(.param) | map({param: .[0].param, total: map(.delta) | add})' \
  .gemini/03_NOVELLS/02_KINGMAKER/02_SYSTEM/POLL_LOG.json
```

---

*Версия 1.0 - 16.05.2026.*
