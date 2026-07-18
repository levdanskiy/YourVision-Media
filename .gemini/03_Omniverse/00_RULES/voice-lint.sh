#!/usr/bin/env bash
# voice-lint.sh - лёгкий формат-осведомлённый линтер поста (OMNIVERSE / BLACK BOX).
#
# Философия та же, что у 03_NOVELLS/09_GENERAL/tools/voice-lint.sh, но:
#   - НЕ навязывает Novells-длину (романы ARCANA/ZODIAC = длинная форма 3500-4000
#     символов; дневник TOWER/PARALLAX = короткая). Длина проверяется ПО ФОРМАТУ.
#   - Главная ценность - универсальные блокеры на все деревья: тире, мусорные
#     символы, ЧУЖИЕ сигнатуры (анти-протечка голоса между работами библиотеки).
#
# Использование:
#   voice-lint.sh --auto <file>        # автодетект работы по пути
#   voice-lint.sh <work> <file>        # work: arcana|zodiac|tower|parallax
#
# Exit: 0 чисто · 1 ошибки (блок) · 2 предупреждения.

set -uo pipefail

MODE="${1:-}"; WORK=""; FILE=""
if [ "$MODE" = "--auto" ]; then
  FILE="${2:-}"
  case "$FILE" in
    *01_ARCANA/*)           WORK="arcana" ;;
    *02_ZODIAC/*)           WORK="zodiac" ;;
    *01_TOWER/*)            WORK="tower" ;;
    *02_CINNAMON_CASE/*)    WORK="cinnamon_case" ;;
    *03_PARALLAX/*)         WORK="parallax" ;;
    *01_KOCHEVYE/*)         WORK="kochevye" ;;
    *02_VENSKAYA_KROV/*)    WORK="venskaya_krov" ;;
    *03_ORDER_OF_SIGNS/*)   WORK="order_of_signs" ;;
    *04_TYULPAN_I_PEPEL/*)  WORK="tyulpan_i_pepel" ;;
    *05_PANTEON/*)          WORK="panteon" ;;
    *01_ELEYIA/*)           WORK="eleyia" ;;
    *02_KINGMAKER/*)        WORK="kingmaker" ;;
    *03_ORCHID/*)           WORK="orchid" ;;
    *04_WHITE_LADY/*)       WORK="white_lady" ;;
    *) echo "❌ Не удалось определить работу по пути: $FILE"; exit 1 ;;
  esac
else
  WORK="$MODE"; FILE="${2:-}"
fi
[ -z "$WORK" ] || [ -z "$FILE" ] && { echo "Usage: $0 --auto <file> | $0 <work> <file>"; exit 1; }
[ -f "$FILE" ] || { echo "❌ Файл не найден: $FILE"; exit 1; }

# Формат работы: long (роман) | short (дневник)
case "$WORK" in
  arcana|zodiac|eleyia|kingmaker|orchid|white_lady|kochevye|venskaya_krov|order_of_signs|tyulpan_i_pepel|panteon)
                          FORMAT="long" ;;
  tower|parallax|somnium|cinnamon_case)
                          FORMAT="short" ;;
  *)                      FORMAT="long" ;;
esac

ERRORS=0; WARNINGS=0
UNIVERSAL_FORBIDDEN="очень|крайне|невероятно|совсем|жутко|безумно|вдруг|внезапно|неожиданно|ужасно|потрясающе|прекрасно|отвратительно"

# Сигнатурные слои всей библиотеки (colon-префиксы). Своя пропускается.
declare -A SIGS=(
  [eleyia]="Вкус момента:"
  [orchid]="Расклад:"
  [km]="Под этим:"
  [snegurochka]="Иней:"
  [zodiac]="Карта часа:"
  [donor]="Кровь помнит:"
  [horizon]="Лог системы:"
  [order]="Земля слышала:"
  [kochevye]="В крови помнят..."
  [venskaya_krov]="Кровь помнит:"
  [order_of_signs]="Карта говорит:"
  [tyulpan_i_pepel]="Зеркальный сон:"
  [panteon]="Синхронизация:"
)

# ── 1. Тире (универсально, блок) ──
dash=$(grep -nE "—|–" "$FILE" 2>/dev/null || true)
if [ -n "$dash" ]; then
  echo "❌ Эм/эн-тире (запрещено, только дефис '-'):"
  echo "$dash" | head -10 | sed 's/^/    /'
  ERRORS=$((ERRORS + 1))
fi

# ── 2. Мусорные/чужие символы (CJK/кана/хангыль/арабица/иврит, блок) ──
JUNK=$(python3 - "$FILE" << 'PYEOF' 2>/dev/null
import sys, re
try:
    t = open(sys.argv[1], encoding='utf-8').read()
    bad = re.findall(r'[぀-ヿ㐀-䶿一-鿿가-힯؀-ۿ֐-׿]', t)
    print(''.join(sorted(set(bad))))
except Exception:
    pass
PYEOF
)
if [ -n "$JUNK" ]; then
  echo "❌ Мусорные/чужие символы (вероятно опечатка-вставка): $JUNK"
  ERRORS=$((ERRORS + 1))
fi

# ── 3. Чужие сигнатуры (анти-протечка голоса, блок) ──
for w in "${!SIGS[@]}"; do
  [ "$w" = "$WORK" ] && continue
  sig="${SIGS[$w]}"
  if grep -Fq "$sig" "$FILE" 2>/dev/null; then
    echo "❌ ЧУЖАЯ СИГНАТУРА «${sig}» (слой работы ${w}) в посте ${WORK}. Свой слой у каждой работы (ARCANA=«магия через чувства», ZODIAC=«Карта часа:», TOWER=дневник)."
    ERRORS=$((ERRORS + 1))
  fi
done

# ── 4. Универсальные слова-заполнители (предупреждение) ──
found=$(grep -ioE "(^|[^а-яё])(${UNIVERSAL_FORBIDDEN})([^а-яё]|\$)" "$FILE" 2>/dev/null | grep -ioE "(${UNIVERSAL_FORBIDDEN})" | sort -u || true)
if [ -n "$found" ]; then
  echo "⚠️  Слова-заполнители (эмоция через точность, не через штамп):"
  echo "$found" | sed 's/^/    - /'
  WARNINGS=$((WARNINGS + 1))
fi

# ── 5. Длина ПО ФОРМАТУ ──
WORDS=$(wc -w < "$FILE")
IS_PROMO=0
IS_LORE=0
IS_PROLOGUE=0

if [[ "${FILE,,}" =~ (promo|anons|анонс) ]] || grep -qE "ПРОТОКОЛЫ:.*(FLASH|PROMO)|Grade:[[:space:]]*[FSQB]" "$FILE" 2>/dev/null; then
  IS_PROMO=1
elif [[ "$FILE" =~ (prolog|пролог) ]]; then
  IS_PROLOGUE=1
elif [[ "$FILE" =~ (lore|лор|soundtrack|архив|archive) ]]; then
  IS_LORE=1
fi

if [ "$FORMAT" = "long" ]; then
  if [ $IS_PROMO -eq 1 ]; then
    # Определяем этап промо
    if [[ "$FILE" =~ (_02_|_02|PROMO_02|досье|dossier) ]]; then
      # ЭТАП 2: DOSSIER (450-550 слов)
      if [ "$WORDS" -lt 450 ] || [ "$WORDS" -gt 550 ]; then
        echo "⚠️  Промо-досье (Этап 2) должно быть 450-550 слов (сейчас $WORDS слов)"
        WARNINGS=$((WARNINGS + 1))
      fi
    else
      # ЭТАПЫ 1, 3, 4: HOOK, INTERACTIVE, COUNTDOWN (300-400 слов)
      if [ "$WORDS" -lt 300 ] || [ "$WORDS" -gt 400 ]; then
        echo "⚠️  Промо-пост (Этап 1, 3, 4) должен быть 300-400 слов (сейчас $WORDS слов)"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  elif [ $IS_PROLOGUE -eq 1 ]; then
    if [ "$WORDS" -lt 600 ] || [ "$WORDS" -gt 700 ]; then
      echo "⚠️  Завязка/пролог должен быть 600-700 слов (сейчас $WORDS слов)"
      WARNINGS=$((WARNINGS + 1))
    fi
  elif [ $IS_LORE -eq 1 ]; then
    if [ "$WORDS" -lt 500 ] || [ "$WORDS" -gt 600 ]; then
      echo "⚠️  Лор/реакция/второстепенный пост должен быть 500-600 слов (сейчас $WORDS слов)"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    # Основная глава
    if [ "$WORDS" -lt 800 ] || [ "$WORDS" -gt 900 ]; then
      echo "⚠️  Основная глава должна быть 800-900 слов (сейчас $WORDS слов)"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi
else
  # Дневниковый (short) формат
  if [ "$WORDS" -gt 400 ]; then
    echo "⚠️  Запись дневника раздута: $WORDS слов (TOWER/PARALLAX держат ~2-3 мин чтения)"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ── Итог ──
if [ "$ERRORS" -gt 0 ]; then
  echo; echo "❌ voice-lint ($WORK): $ERRORS ошибок, $WARNINGS предупреждений"; exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo; echo "⚠️  voice-lint ($WORK): $WARNINGS предупреждений"; exit 2
else
  exit 0
fi
