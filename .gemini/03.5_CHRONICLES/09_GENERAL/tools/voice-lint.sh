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
    *01_ARCANA/*)    WORK="arcana" ;;
    *02_ZODIAC/*)    WORK="zodiac" ;;
    *01_TOWER/*)     WORK="tower" ;;
    *02_PARALLAX/*)  WORK="parallax" ;;
    *03_SOMNIUM/*)   WORK="somnium" ;;
    *) echo "❌ Не удалось определить работу по пути: $FILE"; exit 1 ;;
  esac
else
  WORK="$MODE"; FILE="${2:-}"
fi
[ -z "$WORK" ] || [ -z "$FILE" ] && { echo "Usage: $0 --auto <file> | $0 <work> <file>"; exit 1; }
[ -f "$FILE" ] || { echo "❌ Файл не найден: $FILE"; exit 1; }

# Формат работы: long (роман) | short (дневник)
case "$WORK" in
  arcana|zodiac)          FORMAT="long" ;;
  tower|parallax|somnium) FORMAT="short" ;;
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
CHARS=$(wc -m < "$FILE")
WORDS=$(wc -w < "$FILE")
if [ "$FORMAT" = "long" ]; then
  # роман: пост целится в 3500-4000 символов (стандарт серии); коротко = сигнал
  if [ "$CHARS" -lt 1500 ]; then
    echo "⚠️  Пост короткий для длинной формы: $CHARS символов (стандарт ARCANA/ZODIAC ~3500-4000; анонс/лор могут быть короче)"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  # дневник: короткие плотные записи; раздувание = сигнал
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
