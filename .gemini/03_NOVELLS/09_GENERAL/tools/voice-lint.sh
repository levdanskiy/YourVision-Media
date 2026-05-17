#!/usr/bin/env bash
# voice-lint.sh - Проверка поста по VOICE_LOCK правилам.
#
# Использование:
#   voice-lint.sh <project> <file>     # один файл
#   voice-lint.sh --auto <file>        # автодетект проекта по пути
#
# Returns:
#   0 - всё чисто
#   1 - есть ошибки (блокирующие)
#   2 - есть предупреждения (не блокирующие)

set -uo pipefail

MODE="${1:-}"
PROJECT=""
FILE=""

if [ "$MODE" = "--auto" ]; then
  FILE="${2:-}"
  if [ -z "$FILE" ]; then
    echo "Usage: $0 --auto <file>"
    exit 1
  fi
  # Detect project from path
  case "$FILE" in
    */02_KINGMAKER/*) PROJECT="km" ;;
    */10_VIENNA_SPECIAL/*) PROJECT="vs" ;;
    */05_ORCHID/*) PROJECT="orchid" ;;
    */03_DONOR/*) PROJECT="donor" ;;
    */06_ORDER/*) PROJECT="order" ;;
    */04_HORIZON/*) PROJECT="horizon" ;;
    */07_CODE/*) PROJECT="code" ;;
    */08_ANTHROPOS/*) PROJECT="anthropos" ;;
    */01_ELEYIA/*) PROJECT="eleyia" ;;
    */01_YOURVISION/*) PROJECT="yv" ;;
    *)
      echo "❌ Не удалось определить проект по пути: $FILE"
      exit 1
      ;;
  esac
else
  PROJECT="$MODE"
  FILE="${2:-}"
fi

if [ -z "$PROJECT" ] || [ -z "$FILE" ]; then
  echo "Usage: $0 <project> <file>"
  echo "       $0 --auto <file>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "❌ Файл не найден: $FILE"
  exit 1
fi

# ============================================
# Project-specific rules
# ============================================
UNIVERSAL_FORBIDDEN="очень|крайне|невероятно|совсем|жутко|безумно|вдруг|внезапно|неожиданно|ужасно|потрясающе|прекрасно|отвратительно"

PROJECT_NAME=""
FORBIDDEN_EXTRA=""
FORBIDDEN_BLOCKING=""
MODERN_TECH=""
MUSIC_CLICHES=""
HEDGES=""
PROMPT_REQUIRED=""

case "$PROJECT" in
  km|kingmaker)
    PROJECT_NAME="Kingmaker"
    FORBIDDEN_EXTRA="прикинь|короче|щас|чё|ага|клёво|прикольно"
    MODERN_TECH="iPhone|Айфон|WhatsApp|Ватсап|Telegram|Телеграм|Instagram|Инстаграм|TikTok|Тикток"
    ;;
  vs|vienna_special)
    PROJECT_NAME="Vienna Special"
    FORBIDDEN_EXTRA="прикинь|короче|щас|чё|ага"
    MUSIC_CLICHES="шедевр|потрясающий вокал|эмоциональный накал|культовый|легендарный|прорыв года|сенсация|douze points|европейская семья|победитель сердец|феерия"
    ;;
  yv|yourvision)
    PROJECT_NAME="YourVision (Sniper)"
    # §2 OS табу-лексика - блокирующая
    FORBIDDEN_BLOCKING="невероятный|невероятная|невероятно|потрясающий|потрясающая|потрясающе|ошеломительный|ошеломительная|ошеломительно|легендарный|легендарная|уникальный|уникальная|эпический|эпическая|грандиозный|грандиозная|долгожданный|долгожданная|культовый|культовая|феноменальный|феноменальная|мощный|мощная|яркий|яркая"
    # §2 OS хедж-обороты - предупреждение
    HEDGES="стоит отметить|интересно, что|интересно что|нельзя не сказать|как известно|по сути|в принципе"
    # §8 OS - промпт обязан содержать --ar 1:1
    PROMPT_REQUIRED="--ar 1:1"
    ;;
  *)
    PROJECT_NAME="$PROJECT (правила по умолчанию)"
    ;;
esac

# ============================================
# Extract body text (between first --- and footer)
# ============================================
BODY=$(awk '
  /^---$/ {
    if (after_first == 0) { after_first = 1; next }
  }
  after_first && /^`⏱/ { in_footer = 1 }
  after_first && /^\*\*Grade:/ { in_footer = 1 }
  after_first && /^\*\*Prompt:/ { in_footer = 1 }
  after_first && !in_footer { print }
' "$FILE")

# Extract prompt (image prompt section)
PROMPT=$(awk '
  /^\*\*Prompt:\*\*/ { in_prompt = 1 }
  in_prompt { print }
' "$FILE")

# ============================================
# Check 1: Forbidden lexicon in body
# ============================================
ERRORS=0
WARNINGS=0

ALL_FORBIDDEN="${UNIVERSAL_FORBIDDEN}"
if [ -n "$FORBIDDEN_EXTRA" ]; then
  ALL_FORBIDDEN="${ALL_FORBIDDEN}|${FORBIDDEN_EXTRA}"
fi

found=$(echo "$BODY" | grep -iE "(^|[^а-яё])(${ALL_FORBIDDEN})([^а-яё]|\$)" 2>/dev/null || true)
if [ -n "$found" ]; then
  echo "⚠️  Запрещённые слова найдены в теле поста:"
  echo "$found" | grep -iE -o "(${ALL_FORBIDDEN})" | sort -u | sed 's/^/    - /'
  echo "    См. VOICE_LOCK проекта \"${PROJECT_NAME}\""
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# Check 2: Modern tech (KM only)
# ============================================
if [ -n "$MODERN_TECH" ]; then
  found=$(echo "$BODY" | grep -E "(${MODERN_TECH})" 2>/dev/null || true)
  if [ -n "$found" ]; then
    echo "❌ Современные технологии без переинтерпретации (запрещено в ${PROJECT_NAME}):"
    echo "$found" | grep -E -o "(${MODERN_TECH})" | sort -u | sed 's/^/    - /'
    echo "    Использовать: «зашифрованный телефон без маркировки», «закрытый канал», etc."
    ERRORS=$((ERRORS + 1))
  fi
fi

# ============================================
# Check 3: Music cliches (VS only)
# ============================================
if [ -n "$MUSIC_CLICHES" ]; then
  found=$(echo "$BODY" | grep -iE "(${MUSIC_CLICHES})" 2>/dev/null || true)
  if [ -n "$found" ]; then
    echo "⚠️  Музыкально-фанатские клише в Vienna Special:"
    echo "$found" | grep -iE -o "(${MUSIC_CLICHES})" | sort -u | sed 's/^/    - /'
    echo "    См. VOICE_LOCK Vienna Special - не оценивать выступления"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================
# Check 4: Exclamation marks in body
# ============================================
found=$(echo "$BODY" | grep -E "!" 2>/dev/null || true)
if [ -n "$found" ]; then
  count=$(echo "$BODY" | grep -c -E "!" 2>/dev/null || echo "0")
  echo "⚠️  Восклицательные знаки в теле поста: $count"
  echo "    VOICE_LOCK: эмоция через краткость, не через знак"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# Check 5: Body length
# ============================================
WORD_COUNT=$(echo "$BODY" | wc -w)
if [ "$WORD_COUNT" -lt 30 ]; then
  echo "⚠️  Тело поста слишком короткое: $WORD_COUNT слов"
  echo "    Минимум 30 слов, обычно 60-250"
  WARNINGS=$((WARNINGS + 1))
elif [ "$WORD_COUNT" -gt 400 ]; then
  echo "⚠️  Тело поста слишком длинное: $WORD_COUNT слов"
  echo "    Обычно 60-300, максимум 400 - дальше теряется ритм"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# Check 6: Image prompt has character name (Novells only, skip for YV)
# ============================================
if [ "$PROJECT" != "yv" ] && [ "$PROJECT" != "yourvision" ] && [ -n "$PROMPT" ]; then
  KNOWN_NAMES="Alex|Theodora|Erik|Marco|KORYNNYA|Korynnya|Julien|Klara|Linus|Klavis|Adrian|Leon|Damien|Beatrice|Isabella|Khloe|Chloe|Nora|Max|Lukas|Berg|Vossen|Johansson"
  GENERIC="young woman|young man|professional woman|tall woman|tall man|petite woman|young professional|woman in her|man in his"

  has_generic=$(echo "$PROMPT" | grep -E -i "$GENERIC" || true)
  has_name=$(echo "$PROMPT" | grep -E "$KNOWN_NAMES" || true)

  if [ -n "$has_generic" ] && [ -z "$has_name" ]; then
    echo "⚠️  Промпт изображения - обобщённое описание без имени персонажа"
    echo "    Правило: имя персонажа всегда в промпте"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================
# Check 7: YV blocking forbidden lexicon (Sniper §2)
# ============================================
if [ -n "$FORBIDDEN_BLOCKING" ]; then
  found=$(echo "$BODY" | grep -iE "(^|[^а-яё])(${FORBIDDEN_BLOCKING})([^а-яё]|\$)" 2>/dev/null || true)
  if [ -n "$found" ]; then
    echo "❌ YV Sniper: запрещённые слова (§2 OS, табу-лексика):"
    echo "$found" | grep -iE -o "(${FORBIDDEN_BLOCKING})" | sort -u | sed 's/^/    - /'
    echo "    Sniper: заменить точным фактом или удалить эпитет"
    ERRORS=$((ERRORS + 1))
  fi
fi

# ============================================
# Check 8: YV hedge phrases (warning)
# ============================================
if [ -n "$HEDGES" ]; then
  found=$(echo "$BODY" | grep -iE "(${HEDGES})" 2>/dev/null || true)
  if [ -n "$found" ]; then
    echo "⚠️  YV Sniper: хедж-обороты (§2 OS):"
    echo "$found" | grep -iE -o "(${HEDGES})" | sort -u | sed 's/^/    - /'
    echo "    Sniper: убрать хедж, начать предложение с факта"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================
# Check 9: YV prompt requirements (warning)
# ============================================
if [ -n "$PROMPT_REQUIRED" ] && [ -n "$PROMPT" ]; then
  if ! echo "$PROMPT" | grep -q -- "$PROMPT_REQUIRED"; then
    echo "⚠️  YV §8: промпт не содержит обязательное \`$PROMPT_REQUIRED\`"
    echo "    Все YV-промпты должны быть квадратными (--ar 1:1)"
    WARNINGS=$((WARNINGS + 1))
  fi
  if ! echo "$PROMPT" | grep -q "Dazed magazine aesthetic"; then
    echo "⚠️  YV §8: промпт без стандартного хвоста \"Dazed magazine aesthetic\""
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================
# Result
# ============================================
if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "❌ voice-lint: $ERRORS ошибок, $WARNINGS предупреждений"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo ""
  echo "⚠️  voice-lint: $WARNINGS предупреждений (не блокируют)"
  exit 2
else
  exit 0
fi
