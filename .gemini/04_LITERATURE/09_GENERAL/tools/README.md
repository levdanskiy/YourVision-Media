# 🔧 tools (OMNIVERSE / Literature)

Аналог `03_NOVELLS/09_GENERAL/tools/` - инструменты паритета для дерева Literature.

## `stats-check.py` - валидатор чисел

Схемо-агностичный чекер счётчиков всех работ дерева. Ловит ровно те ошибки, что раньше делались руками: арифметику, выход за кап/границы, пропущенные пороги, рассинхрон `STATS.json` ↔ `STATE.md`.

```bash
python3 stats-check.py --all       # все работы (ARCANA, ZODIAC…)
python3 stats-check.py arcana      # одна работа
python3 stats-check.py arcana --quiet   # только ⚠/❌
```

Что проверяет: `value == start + Σ(history.delta)` (для ресурса с `max` старт = max), границы `min/max/cap`, достигнутые `thresholds` (для сверки unlock-постов), гигиена истории (`post_id`, порядок по day/date) и **зеркало прозы** в `STATE.md` (раздел «СКРЫТЫЕ СЧЕТЧИКИ»).

Ошибка → exit code 1 (годится для pre-commit). Гонять в конце каждого круга перед коммитом.

**Схема-соглашение** (чтобы чекер видел счётчик): узел вида
```json
{ "value": 2, "start": 0, "cap": 99, "max": 100, "thresholds": [25,50,75],
  "history": [ { "delta": 1, "post_id": "…", "reason": "…", "date": "…" } ] }
```
`start/cap/max/min/thresholds` - опциональны. ZODIAC при запуске завести `STATS.json` в этом виде (ЭНТРОПИЯ: `start:2`, `max:10`, `thresholds:[3,5,7,10]`; affinity-линии: `cap:99`, `thresholds:[25,50,75,100]`).

Копия того же движка живёт в `03.5_CHRONICLES/09_GENERAL/tools/` (свой реестр работ). При правке движка синхронить обе.
