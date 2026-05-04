---
name: hub-engine
description: Техническое управление интерактивным Хабом (YV_Editor_Hub.html + data.js). Контроль JavaScript-логики, Radio API, iTunes Search и News Feed. Гарантирует целостность кода при обновлении данных.
---

# 🛠 Hub Engine V2.0

Этот навык отвечает за техническое здоровье YourVision Hub.

## 📁 ФАЙЛЫ

- **`/home/levdanskiy/YV_Editor_Hub.html`** — основной интерфейс
- **`/home/levdanskiy/data.js`** — данные: `news`, `qualifiers`, `wildcards`, `DATES`

## 🧱 СТРУКТУРА ДАННЫХ

- **`DATA` object:** Любые правки массива `news`, `qualifiers` или `wildcards` должны сохранять синтаксис JSON.
- **Таймеры:** Контроль объекта `DATES`. Время указывается в миллисекундах (Unix Timestamp).

## 📻 RADIO & MEDIA

- **API:** Поддержка работоспособности AllOrigins proxy для обхода CORS.
- **Covers:** Приоритет iTunes Search API перед MyRadio24.
- **History:** Контроль корректности записи 10 последних треков в `localStorage`.

## 🤖 ИНТЕГРАЦИЯ С HIVE

- **HEPHAESTUS** автоматически проверяет Hub при каждом тике: `python3 hephaestus_builder.py`
  - Результат в: `01_YOURVISION/_SHARED/build_report.json`
  - Если статус `FAIL` — передать ошибку в `code-sentinel` → `deepseek-bridge`
- **HELIOS** сканирует `content_plan.json` и флагует посты в `publish_queue.json`
  - Hub отображает только посты со статусом `published`

## 🛡 ПРОВЕРКА ПЕРЕД СОХРАНЕНИЕМ

- После каждой правки `YV_Editor_Hub.html` убедиться, что не удалены закрывающие теги `</script>` или `</div>`.
- Запустить: `node -c /home/levdanskiy/data.js` — должен пройти без ошибок.
- Вызвать `code-sentinel` для финальной валидации.

## 🔗 ИНТЕГРАЦИЯ

- `code-sentinel` — валидация JS/HTML перед коммитом
- `deepseek-bridge` — рефакторинг и исправление ошибок кода
- `hive_commander.py` → HEPHAESTUS — автоматический мониторинг целостности
