#!/usr/bin/env bash
# Claude-хук SessionStart: вкидывает в контекст аудит-бриф АКТИВНОГО Novells-проекта
# (по самой свежей публикации). Тихо выходит, если Novells-контента нет.
ROOT=/home/levdanskiy/.gemini/03_NOVELLS
latest=$(find "$ROOT"/*/04_CONTENT -name '*.md' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | awk '{print $2}')
[ -z "$latest" ] && exit 0
proj=$(echo "$latest" | sed -E 's#.*/03_NOVELLS/([0-9]+_[A-Z_]+)/.*#\1#')
case "$proj" in
  05_ORCHID) k=orchid ;;
  02_KINGMAKER) k=km ;;
  01_ELEYIA) k=eleyia ;;
  10_VIENNA_SPECIAL) k=vs ;;
  11_WHITE_LADY) k=white_lady ;;
  12_SNEGUROCHKA_SPECIAL) k=snegurochka ;;
  *) exit 0 ;;
esac
o=$(bash "$ROOT/09_GENERAL/tools/audit.sh" "$k" 2>/dev/null | sed -n '1,30p')
[ -z "$o" ] && exit 0
jq -n --arg t "$o" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:("🗂 Активный Novells-проект - бриф:\n"+$t)}}'
