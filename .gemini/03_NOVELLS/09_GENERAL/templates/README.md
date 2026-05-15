// ИД-ФАЙЛА: TEMPLATES_README
// ВЕРСИЯ: 1.0

# 📐 NOVELLS POST TEMPLATES

Шаблоны новых форматов постов (помимо ядра VERDICT / STORY+POLL / PERSONA / CLIFFHANGER / SCOREBOARD).

См. [[NOVELLS_OS.md]] раздел 2 для общего списка типов.

---

## ШАБЛОНЫ

| Тип | Файл | Когда использовать |
|-----|------|--------------------|
| **DOSSIER** | [template_dossier.md](./template_dossier.md) | Утечённый документ - email, отчёт, расписание, медсправка. Affinity 25%. Лор-плотность. |
| **NOTEBOOK PAGE** | [template_notebook_page.md](./template_notebook_page.md) | Страница из блокнота ГГ. Affinity 50%. Внутренние заметки, наблюдения. |
| **BLACK VELVET LEAK** (KM) / **CHANNEL SIX** (VS) / эквивалент | [template_black_velvet.md](./template_black_velvet.md) | Анонимная утечка. Один факт + контекст + кто читает. |
| **AUDIO TEMPLATE** | [template_audio.md](./template_audio.md) | Голосовое сообщение / запись в текстовом формате. Таймкоды, паузы. |
| **TRUE ROUTE FRAGMENT** | [template_true_route.md](./template_true_route.md) | Скрытый фрагмент, доступный при определённых условиях. Affinity 100% или комбинации выборов. |

---

## ПРАВИЛА ИСПОЛЬЗОВАНИЯ

1. **Перед написанием** - прочитать VOICE_LOCK проекта + шаблон формата.
2. **Длина** - короче чем STORY (60-150 слов основного текста, по типу).
3. **Адаптация под проект** - каждый шаблон имеет per-project секцию. KM использует Black Velvet, VS использует Channel Six, и т.д.
4. **Pre-commit** - те же правила: эм-тире нет, имена персонажей в промптах.

---

## ВСТРАИВАНИЕ В РИТМ ДНЯ

Стандартный ритм - VERDICT, STORY+POLL × 2, PERSONA/SUPPORTING, CLIFFHANGER, SCOREBOARD.

Новые форматы встраиваются как **SUPPORTING POST** (обычно слот 17:00, реже отдельный) или как unlock-пост вне ритма (по триггеру affinity).

Пример встраивания (KM Phase 2):
```
09:45 VERDICT
12:00 STORY + POLL
14:00 BLACK VELVET LEAK     ← новый формат вместо второй STORY
17:00 PERSONA               ← или DOSSIER если триггер сработал
20:00 STORY (без опроса)
21:00 STATS POST            ← раз в фазу
```

---

*Версия 1.0 - 16.05.2026.*
