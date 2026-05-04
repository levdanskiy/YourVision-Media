---
name: deepseek-bridge
description: Делегирование технических задач DeepSeek — кодинг, рефакторинг, JS-логика Хаба. Главный Инженер системы.
---

# 🧠 DeepSeek Bridge V2.0 (Главный Инженер)

Этот мост делегирует технические задачи модели DeepSeek через `./ask-deepseek.sh`.

## 🛠 КОГДА ИСПОЛЬЗОВАТЬ

- Рефакторинг JS-логики в `index.html` (YV Editor Hub).
- Отладка Python-агентов (`argus_*.py`, `hive_commander.py`).
- Написание новых скриптов (bash, Python) для ENGINE.
- Сложная JSON/DB логика (`tournament_state.json`, `content_plan.db`).
- Code review перед деплоем.

## 🚫 КОГДА НЕ ИСПОЛЬЗОВАТЬ

- Написание контента (посты, тексты) — это задача `yv-editor`.
- Промпты Midjourney — это `yv-asset-manager`.
- Простые однострочные bash-команды — вызывать напрямую.

## 📞 ВЫЗОВ

```bash
./ask-deepseek.sh 'Отрефактори эту функцию JS: [код]'
```

## 🔗 ИНТЕГРАЦИЯ

- `bridge-controller` вызывает этот мост через пресет **YV_REFACTOR**.
- `code-sentinel` проверяет результат после DeepSeek.
- `hub-engine` передаёт задачи на рефакторинг Хаба.

## 📤 ОЖИДАЕМЫЙ ВЫВОД

Чистый код с комментариями на русском. Без объяснений "почему" — только "что".
