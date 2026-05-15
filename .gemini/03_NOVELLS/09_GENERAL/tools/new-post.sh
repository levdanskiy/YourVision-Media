#!/usr/bin/env bash
# new-post.sh - Создаёт скелет нового поста с заголовком и шаблоном по типу.
#
# Использование:
#   new-post.sh <project> <type> <date_DDMM> <time_HHMM> [slug]
#
# Примеры:
#   new-post.sh km verdict 1805 0945
#   new-post.sh km story 1805 1200 adrian-first-meeting
#   new-post.sh vs persona 1105 1700 alex
#   new-post.sh km dossier 2005 1200 adrian-schedule
#
# Типы: verdict, story, persona, cliffhanger, scoreboard, dossier, notebook,
#       velvet (= leak), audio, true-route (= tr), result

set -uo pipefail

NOVELLS_ROOT="/home/levdanskiy/.gemini/03_NOVELLS"

project_dir() {
  case "$1" in
    kingmaker|km) echo "02_KINGMAKER" ;;
    vienna_special|vs) echo "10_VIENNA_SPECIAL" ;;
    orchid) echo "05_ORCHID" ;;
    donor) echo "03_DONOR" ;;
    order) echo "06_ORDER" ;;
    horizon) echo "04_HORIZON" ;;
    code) echo "07_CODE" ;;
    anthropos) echo "08_ANTHROPOS" ;;
    eleyia) echo "01_ELEYIA" ;;
    *) echo "" ;;
  esac
}

project_prefix() {
  case "$1" in
    kingmaker|km) echo "KM" ;;
    vienna_special|vs) echo "VS" ;;
    orchid) echo "OR" ;;
    donor) echo "DN" ;;
    order) echo "OD" ;;
    horizon) echo "HZ" ;;
    code) echo "CD" ;;
    anthropos) echo "AT" ;;
    eleyia) echo "EY" ;;
    *) echo "" ;;
  esac
}

if [ "$#" -lt 4 ]; then
  echo "Использование: $0 <project> <type> <DDMM> <HHMM> [slug]"
  echo ""
  echo "Проекты: kingmaker (km), vienna_special (vs), orchid, donor,"
  echo "         order, horizon, code, anthropos, eleyia"
  echo ""
  echo "Типы:    verdict, story, persona, cliffhanger, scoreboard,"
  echo "         dossier, notebook, velvet (leak), audio, true-route (tr), result"
  echo ""
  echo "Пример:  $0 km story 1805 1200 adrian-first-meeting"
  exit 1
fi

PROJECT="$1"
TYPE="$2"
DDMM_RAW="$3"
HHMM_RAW="$4"
SLUG="${5:-}"

PROJ_DIR=$(project_dir "$PROJECT")
PROJ_PREFIX=$(project_prefix "$PROJECT")

if [ -z "$PROJ_DIR" ]; then
  echo "❌ Неизвестный проект: $PROJECT"
  exit 1
fi

# Парсим DDMM → DD.MM
if [[ ! "$DDMM_RAW" =~ ^[0-9]{4}$ ]]; then
  echo "❌ Дата должна быть в формате DDMM (4 цифры). Получено: $DDMM_RAW"
  exit 1
fi
DD="${DDMM_RAW:0:2}"
MM="${DDMM_RAW:2:2}"

# Парсим HHMM → HH-MM
if [[ ! "$HHMM_RAW" =~ ^[0-9]{4}$ ]]; then
  echo "❌ Время должно быть в формате HHMM (4 цифры). Получено: $HHMM_RAW"
  exit 1
fi
HH="${HHMM_RAW:0:2}"
MIN="${HHMM_RAW:2:2}"

# Нормализуем тип
case "$TYPE" in
  verdict|VERDICT) TYPE_UP="VERDICT" ;;
  story|STORY) TYPE_UP="STORY" ;;
  persona|PERSONA) TYPE_UP="PERSONA" ;;
  cliffhanger|CLIFFHANGER) TYPE_UP="CLIFFHANGER" ;;
  scoreboard|SCOREBOARD|status) TYPE_UP="STATUS" ;;
  dossier|DOSSIER) TYPE_UP="DOSSIER" ;;
  notebook|NOTEBOOK) TYPE_UP="NOTEBOOK" ;;
  velvet|leak|LEAK) TYPE_UP="LEAK" ;;
  audio|AUDIO) TYPE_UP="AUDIO" ;;
  true-route|tr|TR) TYPE_UP="TRUEROUTE" ;;
  result|RESULT) TYPE_UP="RESULT" ;;
  *) echo "❌ Неизвестный тип: $TYPE"; exit 1 ;;
esac

# Имя файла
SLUG_UP=""
if [ -n "$SLUG" ]; then
  SLUG_UP=$(echo "$SLUG" | tr 'a-z' 'A-Z' | tr '_' '-')
  FILENAME="${PROJ_PREFIX}-${DD}.${MM}-${HH}-${MIN}-${TYPE_UP}-${SLUG_UP}.md"
else
  FILENAME="${PROJ_PREFIX}-${DD}.${MM}-${HH}-${MIN}-${TYPE_UP}.md"
fi

POST_ID="${FILENAME%.md}"

# Папка
TARGET_DIR="${NOVELLS_ROOT}/${PROJ_DIR}/04_CONTENT/2026/${MM}/${DD}"
TARGET_FILE="${TARGET_DIR}/${FILENAME}"

# Проверка
if [ -f "$TARGET_FILE" ]; then
  echo "⚠️  Файл уже существует: $TARGET_FILE"
  echo "    Не перезаписываю. Удали вручную, если нужно создать заново."
  exit 1
fi

mkdir -p "$TARGET_DIR"

# Генерируем скелет по типу
HEADER="// ИД-ПОСТА: ${POST_ID}
// ТЕМА: [тема]
// ДАТА ПУБЛИКАЦИИ: ${DD}.${MM}.2026, ${HH}:${MIN}
// ТИП: ${TYPE_UP}
// СТАТУС: ЧЕРНОВИК"

case "$TYPE_UP" in
  VERDICT)
    BODY="**ВЕРДИКТ**

[Краткий итог опросов вчера - 2-3 строки, атмосферно]

---

[Что это значит. Афористическая интерпретация.]

[Что меняется - одна строка.]

[Анонс дня - одна строка.]"
    ;;
  STORY)
    BODY="**ДЕНЬ X / TIME / ЛОКАЦИЯ**
*[короткое уточнение пространства]*

---

[Сцена. Короткие абзацы. Действие через предметы и паузы.]

---

[Развитие. Что становится известно.]

---

[Дилемма. Часы тикают.]

---

**Что делаешь?**

🔘 [Опция 1]
🔘 [Опция 2]
🔘 [Опция 3]"
    ;;
  PERSONA)
    BODY="**[ИМЯ]**
*[Должность. Возраст. Одна строка.]*

---

[Кто он/она. Что окружающие неправильно думают. Что реально.]

---

[Один конкретный предмет.]
[Уязвимость через предмет.]

*Котировка: [статус].*"
    ;;
  CLIFFHANGER)
    BODY="**ДЕНЬ X / TIME / ЛОКАЦИЯ**

---

[Сцена-наблюдение. Один объект, одно движение.]

---

[Финальный удар - 1-3 строки.]"
    ;;
  STATUS)
    BODY="**DATA SCOREBOARD**
*Котировки обновлены. День X.*

---

| # | Артист | Страна | Котировка | Тренд |
|---|--------|--------|-----------|-------|
| 1 | [имя] | 🏳️ | X.X | → |

---

*[1-3 строки комментария к движениям]*

*[Анонс следующего события]*"
    ;;
  DOSSIER)
    BODY="**[ТИП ДОКУМЕНТА] / [ИСТОЧНИК]**
*[Нарративное время] / [Уровень доступа]*

---

[Заголовок документа - 1-2 строки]

---

[Содержание нарративно, 4-7 строк.
Конкретные поля / числа / имена / даты.
Бюрократический регистр.]

---

[Одна деталь, выбивающаяся из бюрократии.]

---

[Что это значит / куда попало]"
    ;;
  NOTEBOOK)
    BODY="**[НАРРАТИВНОЕ ВРЕМЯ] / [ЛОКАЦИЯ]**

---

[Фраза-наблюдение]

[Дополнение]

~~[зачёркнутое]~~ [исправление]

---

Что проверить:
- [пункт 1]
- [пункт 2]
- [пункт 3]

---

[Финальный вопрос или решение]"
    ;;
  LEAK)
    BODY="**🗞 [НАЗВАНИЕ КАНАЛА] / VOL. [N]**

---

«[Цитата 2-4 строки, афористическая]»

---

[Конкретный факт, документ, дата, таймштамп]

---

*[Метрика чтения / кто это видел]*"
    ;;
  AUDIO)
    BODY="**🎙 [ТИП ЗАПИСИ] / [ДЛИНА] / [ИСТОЧНИК]**
*[Нарративное время] / [Локация] / [Доступ]*

---

[Заголовок-контекст: 1-2 строки.]

---

[00:00] [фоновый шум]
[00:03] [Имя]: «реплика»
[00:09] [Имя]: «реплика»
[00:14] [пауза N сек]

---

[Финальная строка - что после записи]"
    ;;
  TRUEROUTE)
    BODY="**🔓 TRUE ROUTE FRAGMENT / FR-[XX]**
*Условие разблокировки: [описание]*

---

[Сцена. Глубокое раскрытие.]

---

[Финальный удар - переосмысление прошлого.]

---

*Этот фрагмент видим тебе, потому что [условие]. Большинству читателей он недоступен.*"
    ;;
  RESULT)
    BODY="**ДЕНЬ X / TIME / ЛОКАЦИЯ**
*[событие]*

---

[Объявление мест. От низшего к высшему.]

[Победитель отдельной строкой.]

---

[Поведение победителя - одна деталь.]

---

[Где Алекс/ГГ в этот момент.]

---

[Что дальше - финальный ход / countdown.]"
    ;;
esac

# Determine project tag for hashtags
case "$PROJECT" in
  kingmaker|km) HASHTAG="#KINGMAKER" ;;
  vienna_special|vs) HASHTAG="#ViennaSpecial" ;;
  *) HASHTAG="#${PROJ_PREFIX}" ;;
esac

# Определяем layer-метку
case "$PROJECT" in
  kingmaker|km) LAYER="♟ Kingmaker Layer" ;;
  vienna_special|vs) LAYER="🎤 Vienna Special" ;;
  *) LAYER="$PROJ_PREFIX" ;;
esac

FOOTER="
\`⏱ X мин | ${LAYER} | День X\`
***

${HASHTAG} #Novells

**Grade:** A
**Prompt:** \`[Character name + scene + lighting + project palette + quality tags + aspect ratio]. No text, no logos.\`"

# Собираем файл
cat > "$TARGET_FILE" <<EOF
${HEADER}

---

${BODY}

---
${FOOTER}
EOF

echo "✅ Создано: $TARGET_FILE"
echo ""
echo "📋 ИД-ПОСТА: $POST_ID"
echo "📂 Папка:    $TARGET_DIR"
echo ""
echo "💡 Дальше:"
echo "  1. Заполни TEMA и СТАТУС в шапке"
echo "  2. Замени плейсхолдеры [...] на контент"
echo "  3. Дополни промпт изображения (имя персонажа обязательно)"
echo "  4. Проверь VOICE_LOCK проекта"
