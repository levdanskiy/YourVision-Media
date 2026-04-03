---
name: hub-engine
description: Техническое управление интерактивным Хабом (index.html). Контроль JavaScript-логики, Radio API, iTunes Search и News Feed. Гарантирует целостность кода при обновлении данных.
---

# 🛠 Hub Engine V1.0

Этот навык отвечает за техническое здоровье YourVision Hub.

## 🧱 СТРУКТУРА ДАННЫХ
- **`DATA` object:** Любые правки массива `news`, `qualifiers` или `wildcards` должны сохранять синтаксис JSON.
- **Таймеры:** Контроль объекта `DATES`. Время указывается в миллисекундах (Unix Timestamp).

## 📻 RADIO & MEDIA
- **API:** Поддержка работоспособности AllOrigins proxy для обхода CORS.
- **Covers:** Приоритет iTunes Search API перед MyRadio24.
- **History:** Контроль корректности записи 10 последних треков в `localStorage`.

## 🛡 ПРОВЕРКА ПЕРЕД СОХРАНЕНИЕМ
- После каждой правки `index.html` навык обязан убедиться, что не удалены закрывающие теги `</script>` или `</div>`.
