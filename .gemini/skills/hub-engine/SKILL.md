---
name: hub-engine
description: Техническое управление интерактивным Хабом (YV_Editor_Hub.html + data.js). Контроль JavaScript-логики, Radio API, iTunes Search и News Feed. Гарантирует целостность кода при обновлении данных.
---

# 🛠 Hub Engine V2.0

Этот навык отвечает за техническое здоровье YourVision Hub.

## 📁 ФАЙЛЫ

- **`/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/index.html`** — основной интерфейс (был `YV_Editor_Hub.html` в /home/levdanskiy/, перенесён 17.05.2026)
- **`/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/data.js`** — данные: `news`, `qualifiers`, `wildcards`, `DATES`
- **`/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/README.md`** — workflow и security warnings
- **Deploy:** `/home/levdanskiy/YourEurovision_Hub_Deploy/` (отдельный git, GitHub Pages)

## 🧱 СТРУКТУРА ДАННЫХ

- **`DATA` object:** Любые правки массива `news`, `qualifiers` или `wildcards` должны сохранять синтаксис JSON.
- **Таймеры:** Контроль объекта `DATES`. Время указывается в миллисекундах (Unix Timestamp).

## 📻 RADIO & MEDIA

- **API:** Поддержка работоспособности AllOrigins proxy для обхода CORS.
- **Covers:** Приоритет iTunes Search API перед MyRadio24.
- **History:** Контроль корректности записи 10 последних треков в `localStorage`.

## 🤖 ИНТЕГРАЦИЯ С HIVE (DEPRECATED 17.05.2026)

Hive-инфраструктура (HEPHAESTUS, HELIOS, hive_commander.py) архивирована в `01_YOURVISION/07_ARCHIVE/02_ENGINE/`. Канал управляется вручную Claude по правилам `01_YOURVISION/01_GENERAL/YOURVISION_OS.md`.

## 🛡 ПРОВЕРКА ПЕРЕД СОХРАНЕНИЕМ

- После каждой правки `index.html` убедиться, что не удалены закрывающие теги `</script>` или `</div>`.
- Запустить: `node -c /home/levdanskiy/.gemini/01_YOURVISION/08_HUB/data.js` — должен пройти без ошибок.
