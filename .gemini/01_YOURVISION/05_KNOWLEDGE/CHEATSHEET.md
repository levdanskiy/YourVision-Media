# ⚡ ШПАРГАЛКА АЛИАСОВ YOURVISION 2.5

## 📋 Основные команды

```bash
# План на день
yv_plan                    # Сегодня
yv_plan 07.02.2026         # Конкретная дата

# Гид по эфирам
yv_guide                   # Список шоу на вечер

# Roadmap недели
yv_week                    # Главные события недели

# Исторический пост
yv_history 12.05           # Пост #EUROFLASHBACK

# Срочная публикация
yv_pub "Текст новости"     # Авто-определение грейда
```

## 📤 Публикация постов

```bash
# FLASH (Grade F: 501-1000 знаков)
python3 yv_publisher.py \
  --type flash \
  --title "ЗАГОЛОВОК" \
  --content "Текст..." \
  --country "Италия" \
  --flag "🇮🇹" \
  --theme "Sanremo" \
  --alert red

# STANDARD (Grade B/C: 1001-1800 знаков)
python3 yv_publisher.py \
  --type standard \
  --title "ЗАГОЛОВОК" \
  --content "Текст..." \
  --country "Швеция" \
  --flag "🇸🇪"

# POLL (Grade S: до 500 знаков)
python3 yv_publisher.py \
  --type poll \
  --title "Вопрос?" \
  --content "🔵 Да\n🔴 Нет" \
  --country "Испания" \
  --flag "🇪🇸"
```

## ✅ Валидация

```bash
# Проверить пост перед публикацией
python3 publish_tool.py путь/к/файлу.md

# Вывод:
# ✅ VALIDATED или ❌ REJECTED
# - Проверка грейда
# - Проверка запрещённых слов
# - Проверка пунктуации (длинное тире)
```

## 🔄 Тройная синхронизация

```bash
# Добавить новое событие
python3 triple_sync.py add \
  --date 2026-03-01 \
  --time 20:00 \
  --country SE \
  --country-name "Швеция" \
  --event "Melodifestivalen - Heat 5" \
  --type HEAT

# Обновить статус
python3 triple_sync.py status --id EVT001 --status COMPLETED

# Отметить задачу выполненной
python3 triple_sync.py complete \
  --date 07.02.2026 \
  --task "Sanremo Night 1"
```

## 🎨 Визуал (Midjourney)

```bash
# Генерация промпта
python3 visual_generator.py --type chart
python3 visual_generator.py --type winner --country IT
python3 visual_generator.py --type news --breaking

# Быстрые шаблоны
python3 visual_generator.py --quick chart_default
python3 visual_generator.py --quick winner_celebratory
```

## 📊 Грейды (Grade System)

| Grade | Символы | Тип поста |
|-------|---------|-----------|
| Q | 100-300 | Мини-заметка |
| S | 301-500 | POLL |
| F | 501-1000 | FLASH |
| B | 1001-1300 | SNAP |
| C | 1301-1800 | STANDARD |
| A | 1801-2400 | DEEP DIVE |

## 🔔 Alert Tiers

| Тир | Реакция | Триггеры |
|-----|---------|----------|
| 🔴 RED | 5 мин | Победитель, дисквалификация, снятие |
| 🟡 YELLOW | 30 мин | Релиз песни, анонс участника |
| 🟢 GREEN | По расписанию | Обычные новости |

## 📁 Git Workflow

```bash
# После успешной валидации
git add . && git commit -m "feat: post - [тема]" && git push

# При замечании оператора
# Добавить правило в .gemini/system/OPERATOR_DIRECTIVES.md
git add . && git commit -m "docs: operator directive" && git push
```

## ⏰ Wave Protocol

| Волна | Время | Контент |
|-------|-------|---------|
| 1 | T+0 | FLASH + POLL |
| 2 | T+15-30 | SNAP/DATA |
| 3 | T+60 | STANDARD |
| 4 | T+утро | DEEP DIVE |

## 📝 Заголовки

```
✅ [ФЛАГ] **[СТРАНА]: ТЕМА - ПОДТЕМА**
✅ 🚨 BREAKING: [ФЛАГ] **[СТРАНА]: ТЕМА**
❌ #NEWS_WIRE: [ФЛАГ] **СТРАНА: ТЕМА**
```

## 🚫 Запреты

- **Слова:** невероятный, потрясающий, ошеломительный, долгожданный
- **Пунктуация:** длинное тире (-), среднее тире (-)
- **Только:** дефис (-), кавычки-елочки (« »)

## 📎 Футер (обязательно)

```markdown
---
`⏱ Время чтения: X.X мин | [ФЛАГ] YourVision: [Тематика]`
***

**Grade:** F
**Prompt:** [Midjourney prompt]
```
