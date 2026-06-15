#!/usr/bin/env bash
# audit.sh - Novells сессионный аудит
# Запускать в начале каждой сессии работы над любым Novells-проектом.
#
# Использование:
#   ./audit.sh kingmaker         # или km
#   ./audit.sh vienna_special    # или vs
#   ./audit.sh orchid
#   ...
#
# Что делает:
#   1. Показывает последние 7 дней публикаций
#   2. Достаёт ключевое из STATE.md
#   3. Парсит последние опросы из POLL_LOG.md
#   4. Если есть STATS.json - таблица котировок и affinity
#   5. Напоминает правила работы

set -uo pipefail

PROJECT="${1:-}"
NOVELLS_ROOT="/home/levdanskiy/.gemini/03_NOVELLS"
TODAY="$(date +%Y-%m-%d)"

project_dir() {
  case "$1" in
    kingmaker|km) echo "$NOVELLS_ROOT/02_KINGMAKER" ;;
    vienna_special|vs) echo "$NOVELLS_ROOT/10_VIENNA_SPECIAL" ;;
    orchid) echo "$NOVELLS_ROOT/05_ORCHID" ;;
    donor) echo "$NOVELLS_ROOT/03_DONOR" ;;
    order) echo "$NOVELLS_ROOT/06_ORDER" ;;
    horizon) echo "$NOVELLS_ROOT/04_HORIZON" ;;
    code) echo "$NOVELLS_ROOT/07_CODE" ;;
    anthropos) echo "$NOVELLS_ROOT/08_ANTHROPOS" ;;
    eleyia) echo "$NOVELLS_ROOT/01_ELEYIA" ;;
    white_lady|wl) echo "$NOVELLS_ROOT/11_WHITE_LADY" ;;
    snegurochka|sneg) echo "$NOVELLS_ROOT/12_SNEGUROCHKA_SPECIAL" ;;
    *) echo "" ;;
  esac
}

if [ -z "$PROJECT" ]; then
  echo ""
  echo "Использование: $0 <project>"
  echo ""
  echo "Проекты:"
  echo "  kingmaker (km), vienna_special (vs), orchid, donor,"
  echo "  order, horizon, code, anthropos, eleyia"
  echo ""
  exit 1
fi

DIR=$(project_dir "$PROJECT")
if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "❌ Проект не найден: $PROJECT"
  exit 1
fi

PROJECT_NAME=$(basename "$DIR")

# Заголовок
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📋 NOVELLS AUDIT"
echo "  Проект: $PROJECT_NAME"
echo "  Дата: $TODAY"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ============================================
# 0. КРАТКО - сессионный бриф (из шапки STATE)
# ============================================
if [ -f "$DIR/02_SYSTEM/STATE.md" ]; then
  echo "🧭 КРАТКО (шапка STATE - где мы / что дальше)"
  echo "───────────────────────────────────────────────────────────────"
  grep -m1 "Последнее обновление" "$DIR/02_SYSTEM/STATE.md" 2>/dev/null \
    | sed 's/\*\*//g; s/^/  /' | fold -s -w 75 | sed '2,$s/^/    /'
  echo ""
fi

# ============================================
# 1. Последние публикации (месяце-независимо - чинит баг хардкода 2026/05)
# ============================================
echo "📅 ПУБЛИКАЦИИ (последние 7 пуб.дней)"
echo "───────────────────────────────────────────────────────────────"
# Собираем все папки-дни YYYY/MM/DD под 04_CONTENT, сортируем по дате, берём 7 последних
recent_days=$(find "$DIR/04_CONTENT" -mindepth 3 -maxdepth 3 -type d 2>/dev/null \
  | sed -E 's#^(.*)/([0-9]{4})/([0-9]{2})/([0-9]{2})$#\2-\3-\4|\1/\2/\3/\4#' \
  | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}\|' | sort -r | head -7)
if [ -z "$recent_days" ]; then
  echo "  (контент не найден)"
else
  while IFS='|' read -r date_key day_path; do
    [ -z "$day_path" ] && continue
    dd="${date_key:8:2}"; mm="${date_key:5:2}"
    post_count=$(ls -1 "$day_path"/*.md 2>/dev/null | wc -l)
    echo ""
    echo "  $dd.$mm  ($post_count постов):"
    ls -1 "$day_path"/*.md 2>/dev/null | while read f; do
      echo "    • $(basename "$f" .md)"
    done
  done <<< "$recent_days"
fi
echo ""

# ============================================
# 2. STATE - ключевое
# ============================================
if [ -f "$DIR/02_SYSTEM/STATE.md" ]; then
  echo "📊 STATE - КЛЮЧЕВОЕ"
  echo "───────────────────────────────────────────────────────────────"
  echo ""

  # Текущая фаза
  awk '/^## 📅 ТЕКУЩАЯ ФАЗА/,/^---$/' "$DIR/02_SYSTEM/STATE.md" 2>/dev/null \
    | grep -v "^---$" | grep -v "^## 📅" | sed 's/^/  /'
  echo ""

  # Статус конфликтов (последние)
  if grep -q "СТАТУС КОНФЛИКТОВ" "$DIR/02_SYSTEM/STATE.md"; then
    echo "  Конфликты (из STATE):"
    awk '/^## 🎭 СТАТУС КОНФЛИКТОВ/,/^---$/' "$DIR/02_SYSTEM/STATE.md" 2>/dev/null \
      | grep "^|" | grep -v "^|---" | head -10 | sed 's/^/    /'
    echo ""
  fi
fi

# ============================================
# 3. POLL_LOG - последние опросы
# ============================================
if [ -f "$DIR/02_SYSTEM/POLL_LOG.json" ]; then
  echo "🗳 ПОСЛЕДНИЕ ОПРОСЫ (из POLL_LOG.json)"
  echo "───────────────────────────────────────────────────────────────"
  python3 << PYEOF 2>/dev/null
import json
try:
    with open("$DIR/02_SYSTEM/POLL_LOG.json") as f:
        data = json.load(f)

    polls = data.get('polls', [])
    if not polls:
        print("  (нет опросов)")
    else:
        # Last 5 polls
        for p in polls[-5:]:
            day = p.get('narrative_day', '?')
            pub = p.get('pub_date', '?')
            q = p.get('question', '')[:60]
            winner = p.get('winner')
            wt = p.get('winner_type', '')
            print(f"  День {day} / {pub} [{p.get('id')}]")
            print(f"    Q: {q}")
            if winner is None:
                print(f"    ⏳ ОТКРЫТ (ждёт результатов)")
            else:
                print(f"    → {winner} ({wt})")
                if p.get('tie_resolution'):
                    tr = p['tie_resolution'][:80]
                    print(f"    ⚖️  Резолюция: {tr}")
                deltas = p.get('stats_deltas', [])
                if deltas:
                    delta_str = ', '.join([f"{d['character']}.{d['param']}{'+' if d['delta']>=0 else ''}{d['delta']}" for d in deltas])
                    print(f"    Δ {delta_str}")
            print()

    # Open polls (those without total_votes set)
    open_polls = [p for p in polls if p.get('total_votes') is None]
    if open_polls:
        print(f"  📍 ОТКРЫТЫХ ОПРОСОВ: {len(open_polls)}")
        for p in open_polls:
            print(f"    [{p.get('id')}] {p.get('question', '')[:60]}")
        print()
except Exception as e:
    print(f"  (ошибка парсинга: {e})")
PYEOF
elif [ -f "$DIR/02_SYSTEM/POLL_LOG.md" ]; then
  echo "🗳 ПОСЛЕДНИЕ ОПРОСЫ (из POLL_LOG.md - JSON ещё не мигрирован)"
  echo "───────────────────────────────────────────────────────────────"
  echo ""
  tail -n 80 "$DIR/02_SYSTEM/POLL_LOG.md" \
    | grep -E "^(###|\*\*Конфликт|\*\*Победитель|\*\*Варианты)" \
    | tail -20 \
    | sed 's/^/  /'
  echo ""
fi

# ============================================
# 4. STATS.json - котировки и affinity
# ============================================
if [ -f "$DIR/02_SYSTEM/STATS.json" ]; then
  echo "📈 STATS (из STATS.json)"
  echo "───────────────────────────────────────────────────────────────"
  python3 << PYEOF 2>/dev/null
import json
try:
    with open("$DIR/02_SYSTEM/STATS.json") as f:
        data = json.load(f)

    print(f"  Phase: {data.get('current_phase', '?')}")
    print(f"  Pub day: {data.get('current_pub_day', '?')}")
    print(f"  Narrative day: {data.get('current_narrative_day', '?')}")
    print(f"  Last updated: {data.get('last_updated', '?')}")
    print()
    print(f"  {'Персонаж':<14} {'Котировка':<10} {'Тренд':<6} {'Affinity':<10} {'Unlocks'}")
    print(f"  {'-'*14} {'-'*10} {'-'*6} {'-'*10} {'-'*15}")

    for cid, c in data.get('characters', {}).items():
        rep = c.get('reputation', {})
        aff = c.get('affinity', {})
        unlocks = aff.get('unlocks', {})
        triggered = sum(1 for u in unlocks.values() if u.get('triggered'))
        print(f"  {c.get('name', cid):<14} {rep.get('current', '?'):<10} {rep.get('trend', '?'):<6} {aff.get('current', 0):<10} {triggered}/4")

    if data.get('polls'):
        print(f"\n  Polls в логе: {len(data['polls'])}")
    if data.get('black_velvet_leaks'):
        print(f"  Black Velvet leaks: {len(data['black_velvet_leaks'])}")
except Exception as e:
    print(f"  (ошибка парсинга: {e})")
PYEOF
  echo ""
fi

# ============================================
# 5. Roadmap - где мы в сезоне
# ============================================
if [ -f "$DIR/SEASON_1_ROADMAP.md" ]; then
  echo "🗺  СЕЗОННЫЙ ROADMAP - ВРЕМЕННАЯ ШКАЛА"
  echo "───────────────────────────────────────────────────────────────"
  awk '/## ⏳ ВРЕМЕННАЯ ШКАЛА/,/^---$/' "$DIR/SEASON_1_ROADMAP.md" 2>/dev/null \
    | grep -v "^---$" | grep -v "^## ⏳" | sed 's/^/  /' | head -15
  echo ""
fi

# ============================================
# 6. Напоминания
# ============================================
echo "💡 ПЕРЕД НАПИСАНИЕМ"
echo "───────────────────────────────────────────────────────────────"
echo ""
echo "  ✓ Получи результаты вчерашних опросов от пользователя"
echo "  ✓ Сверь время в проекте (нарративное ≠ публикационное)"
echo "  ✓ Проверь VOICE_LOCK проекта"
echo "  ✓ Правило: STORY-пост только для уже опрошенных персонажей"
echo "  ✓ Pre-commit хук активен (эм-тире блокируются)"
echo ""

# ============================================
# 7. Ссылки
# ============================================
echo "🔗 ФАЙЛЫ"
echo "───────────────────────────────────────────────────────────────"
[ -f "$DIR/02_SYSTEM/STATE.md" ]      && echo "  STATE:       $DIR/02_SYSTEM/STATE.md"
[ -f "$DIR/02_SYSTEM/POLL_LOG.md" ]   && echo "  POLL_LOG:    $DIR/02_SYSTEM/POLL_LOG.md"
[ -f "$DIR/02_SYSTEM/STATS.json" ]    && echo "  STATS:       $DIR/02_SYSTEM/STATS.json"
[ -f "$DIR/02_SYSTEM/STATS_RULES.md" ] && echo "  STATS_RULES: $DIR/02_SYSTEM/STATS_RULES.md"
[ -f "$DIR/02_SYSTEM/AFFINITY_UNLOCKS.md" ] && echo "  AFFINITY:    $DIR/02_SYSTEM/AFFINITY_UNLOCKS.md"
[ -f "$DIR/02_SYSTEM/LORE.json" ] && echo "  LORE:        $DIR/02_SYSTEM/LORE.json"
[ -f "$DIR/02_SYSTEM/VOICE_LOCK.md" ] && echo "  VOICE_LOCK:  $DIR/02_SYSTEM/VOICE_LOCK.md"
[ -f "$DIR/SEASON_1_ROADMAP.md" ]     && echo "  ROADMAP:     $DIR/SEASON_1_ROADMAP.md"
echo ""
echo "  NOVELLS_OS:  $NOVELLS_ROOT/09_GENERAL/NOVELLS_OS.md"
echo "  Templates:   $NOVELLS_ROOT/09_GENERAL/templates/"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
