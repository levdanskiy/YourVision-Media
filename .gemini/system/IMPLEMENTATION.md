# 🚀 РУКОВОДСТВО ПО ВНЕДРЕНИЮ YOURVISION 2.5 В GEMINI CLI

## 📋 Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Структура файлов](#структура-файлов)
3. [Настройка Gemini CLI](#настройка-gemini-cli)
4. [Алиасы и команды](#алиасы-и-команды)
5. [Workflow публикации](#workflow-публикации)
6. [Тройная синхронизация](#тройная-синхронизация)
7. [Работа с чартами](#работа-с-чартами)

---

## 🚀 Быстрый старт

### Шаг 1: Копирование файлов

```bash
# Создание структуры директорий
mkdir -p ~/.gemini/{CONTENT/posts,ENGINE/scripts,KNOWLEDGE/Live_Calendars,TIMELINE/{database,master_plans},system}

# Копирование файлов
cp yourvision-gemini/GEMINI.md ~/.gemini/
cp yourvision-gemini/scripts/*.py ~/.gemini/ENGINE/scripts/
cp yourvision-gemini/templates/*.md ~/.gemini/CONTENT/
cp yourvision-gemini/config/*.json ~/.gemini/TIMELINE/database/

# Сделать скрипты исполняемыми
chmod +x ~/.gemini/ENGINE/scripts/*.py
```

### Шаг 2: Настройка алиасов

Добавить в `~/.bashrc` или `~/.zshrc`:

```bash
# YourVision алиасы
alias yv_plan='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py plan'
alias yv_guide='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py guide'
alias yv_week='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py week'
alias yv_history='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py history'
alias yv_pub='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py pub'
alias yv_validate='python3 ~/.gemini/ENGINE/scripts/publish_tool.py'
alias yv_sync='python3 ~/.gemini/ENGINE/scripts/triple_sync.py'

# Перезагрузить
source ~/.bashrc
```

### Шаг 3: Инициализация Git

```bash
cd ~/.gemini
git init
git add .
git commit -m "feat: initial YourVision 2.5 setup"
git remote add origin <your-repo>
git push -u origin main
```

---

## 📁 Структура файлов

```
~/.gemini/
├── GEMINI.md                          # Главный файл инструкций
├── CONTENT/
│   ├── posts/
│   │   └── YYYY/MM/DD/                # Посты по датам
│   └── templates/                     # Шаблоны
├── ENGINE/
│   └── scripts/
│       ├── yv_publisher.py            # Основной модуль публикации
│       ├── yv_aliases.py              # Обработчик алиасов
│       ├── publish_tool.py            # Валидация постов
│       ├── triple_sync.py             # Тройная синхронизация
│       ├── alert_system.py            # Система оповещений
│       └── visual_generator.py        # Генератор промптов
├── KNOWLEDGE/
│   └── Live_Calendars/
│       ├── YV_ESC_Live_Calendar.md    # Календарь ESC
│       └── YV_Charts_Calendar.md      # Календарь чартов
├── TIMELINE/
│   ├── database/
│   │   └── yv_season_2026.json        # База данных сезона
│   └── master_plans/
│       └── MM/
│           └── YV_Plan_MM.md          # Планы по месяцам
└── system/
    └── OPERATOR_DIRECTIVES.md         # Директивы оператора
```

---

## ⚙️ Настройка Gemini CLI

### Вариант 1: Контекстный файл

```bash
# В сессии Gemini CLI
/load_context ~/.gemini/GEMINI.md
```

### Вариант 2: Переменная окружения

```bash
# Добавить в ~/.bashrc
export GEMINI_CONTEXT=~/.gemini/GEMINI.md
```

### Вариант 3: Автозагрузка

Создать `~/.gemini/init.sh`:

```bash
#!/bin/bash
echo "🎛️ YourVision 2.5 loaded"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "Доступные команды:"
echo "  yv_plan [дата]    - План на день"
echo "  yv_guide          - Гид по эфирам"
echo "  yv_week           - Roadmap недели"
echo "  yv_history [дата] - Исторический пост"
echo "  yv_pub 'текст'    - Срочная публикация"
```

---

## 📋 Алиасы и команды

### yv_plan - План на день

```bash
yv_plan                # План на сегодня
yv_plan 07.02.2026     # План на конкретную дату
```

**Что делает:**
- Загружает события из JSON базы
- Проверяет незакрытые задачи (долги)
- Генерирует `daily_plan_DD.MM.md`
- Предлагает закрыть долги

### yv_guide - Гид по эфирам

```bash
yv_guide
```

**Что делает:**
- Загружает события на сегодня
- Фильтрует вечерние шоу (после 18:00)
- Генерирует пост Grade F
- Добавляет ссылки на трансляции

### yv_week - Roadmap недели

```bash
yv_week
```

**Что делает:**
- Загружает события на 7 дней
- Группирует по датам
- Генерирует пост Grade B/C

### yv_history - Исторический пост

```bash
yv_history 12.05       # События 12 мая в истории
```

**Что делает:**
- Ищет события в базе истории
- При отсутствии предлагает веб-поиск
- Генерирует пост #EUROFLASHBACK

### yv_pub - Срочная публикация

```bash
yv_pub "Angelina Mango выиграла Sanremo 2026"
```

**Что делает:**
- Анализирует контент (определяет Alert Tier)
- Выбирает тип поста (FLASH/STANDARD)
- Авто-определяет страну и флаг
- Валидирует и публикует
- Синхронизирует с Git

---

## 📤 Workflow публикации

### Обычная публикация

```bash
# 1. Проверка времени
date

# 2. Создание поста (используя шаблон)
cp ~/.gemini/CONTENT/templates/flash_template.md ~/.gemini/CONTENT/posts/2026/02/07/post.md

# 3. Редактирование
# ... заполнить шаблон ...

# 4. Валидация
yv_validate ~/.gemini/CONTENT/posts/2026/02/07/post.md

# 5. Если VALIDATED - публикация
git add . && git commit -m "feat: flash - Sanremo results" && git push
```

### Срочная публикация (RED ALERT)

```bash
# Одна команда
yv_pub "🇮🇹 SANREMO 2026: ANGELINA MANGO - ПОБЕДИТЕЛЬ. Песня «La noia» набрала 48% голосов."

# Автоматически:
# - Определит RED ALERT
# - Создаст FLASH
# - Валидирует
# - Опубликует
# - Синхронизирует Git
```

### Wave Protocol

```bash
# WAVE 1 (T+0): FLASH + POLL
yv_pub "..." --type flash
yv_pub "..." --type poll

# WAVE 2 (T+15): DATA
python3 ~/.gemini/ENGINE/scripts/yv_publisher.py --type snap --content "Полные результаты..."

# WAVE 3 (T+60): STANDARD
python3 ~/.gemini/ENGINE/scripts/yv_publisher.py --type standard --content "Аналитика..."

# WAVE 4 (следующее утро): DEEP DIVE
python3 ~/.gemini/ENGINE/scripts/yv_publisher.py --type deep_dive --content "Подробный разбор..."
```

---

## 🔄 Тройная синхронизация

При появлении нового события обновляются три источника:

### Добавление события

```bash
yv_sync add \
  --date 2026-03-01 \
  --time 20:00 \
  --country SE \
  --country-name "Швеция" \
  --event "Melodifestivalen - Final" \
  --type FINAL
```

**Обновляется:**
1. `yv_season_2026.json` - добавляется объект в events[]
2. `YV_ESC_Live_Calendar.md` - добавляется строка
3. `YV_Plan_03.md` - добавляется задача

### Обновление статуса

```bash
yv_sync status --id EVT001 --status COMPLETED
```

### Отметка задачи выполненной

```bash
yv_sync complete --date 07.02.2026 --task "Sanremo Night 1"
```

---

## 📊 Работа с чартами

### Lifecycle чарта

```
TBA           → Обновление YV_Charts_Calendar.md
За день (20:30) → Анонс номинантов
День (12:00)   → Официальный релиз
День (17:50)   → #CHART_REMINDER
День (19:20)   → #CHART_RESULTS
```

### Генерация промпта для чарта

```bash
python3 ~/.gemini/ENGINE/scripts/visual_generator.py --type chart
```

**Вывод:**
```
group of stylish young people, a guy, a girl, and a romantic couple,
minimalist studio with warm backlighting, shot on 35mm film Kodak Portra 800,
heavy film grain, cinematic realism, high-end fashion editorial,
Dazed magazine aesthetic, moody lighting,
minimalist plain text "YourVision" and "levdanskiy" at the bottom corner
--ar 1:1 --v 6.1 --style raw --s 750
```

---

## ✅ Чек-лист внедрения

- [ ] Файлы скопированы в `~/.gemini/`
- [ ] Алиасы добавлены в `.bashrc`/`.zshrc`
- [ ] Git репозиторий инициализирован
- [ ] `yv_plan` работает
- [ ] `yv_validate` работает
- [ ] Протестирован полный цикл публикации
- [ ] Протестирована тройная синхронизация
- [ ] GEMINI.md загружен в контекст Gemini CLI

---

## 🆘 Решение проблем

### "Grade mismatch"

```bash
# Пост отклонён из-за несоответствия грейда
# Решение: изменить Grade в футере на рекомендованный

**Grade:** B  # было F
```

### "Запрещено длинное тире"

```bash
# Найти и заменить
sed -i 's/-/-/g' файл.md
sed -i 's/-/-/g' файл.md
```

### "Отсутствует промпт"

```bash
# Добавить в футер
**Prompt:** [описание сцены], shot on 35mm film Kodak Portra 800, heavy film grain, cinematic realism --ar 1:1 --v 6.1 --style raw --s 750
```

---

## 📚 Дополнительные ресурсы

- **Шпаргалка:** `CHEATSHEET.md`
- **Шаблоны:** `templates/*.md`
- **Конфиг:** `config/yv_season_2026.json`
- **Инструкции:** `GEMINI.md`

---

**Конец руководства по внедрению YourVision 2.5**
