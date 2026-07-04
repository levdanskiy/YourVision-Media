# 🔧 tools (BLACK BOX / Chronicles)

Аналог `03_NOVELLS/09_GENERAL/tools/` - инструменты паритета для дерева Chronicles.

## `stats-check.py` - валидатор чисел

Схемо-агностичный чекер счётчиков всех работ дерева (TOWER, PARALLAX, SOMNIUM). Ловит арифметику, выход за кап/границы, пропущенные пороги, рассинхрон `STATS.json` ↔ `STATE.md`.

```bash
python3 stats-check.py --all       # все работы
python3 stats-check.py tower       # одна работа
python3 stats-check.py tower --quiet    # только ⚠/❌
```

Что проверяет: `value == start + Σ(history.delta)` (для ресурса с `max` старт = max: полный бак), границы `min/max`, гигиена истории (`post_id`, порядок по `day`) и **зеркало прозы** в `STATE.md` (блок «Дизель / Рассудок / ПАРАНОЙЯ / ЛЮБОПЫТСТВО»).

Ошибка → exit code 1. Гонять в конце каждого дня-круга перед коммитом.

**Схема TOWER:** `resources.<x>` = `{value, max, history}` (старт с полного бака); `alignment.<paranoia|curiosity>` = `{value, history}` (старт 0, копится). `milestones` (флаги done) чекером игнорируются. PARALLAX/SOMNIUM при запуске завести `STATS.json` в том же виде.

Копия того же движка живёт в `04_LITERATURE/09_GENERAL/tools/`. При правке движка синхронить обе.
