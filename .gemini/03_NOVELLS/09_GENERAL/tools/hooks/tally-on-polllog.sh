#!/usr/bin/env bash
# Claude-хук PostToolUse (Bash): если команда тронула POLL_LOG, прогоняет affinity-tally
# для проекта со свежайшим POLL_LOG и вкидывает сверку чисел в контекст (анти-ручная-математика).
ROOT=/home/levdanskiy/.gemini/03_NOVELLS
cmd=$(jq -r '.tool_input.command // empty' 2>/dev/null)
echo "$cmd" | grep -q "POLL_LOG" || exit 0
latest=$(find "$ROOT"/*/02_SYSTEM/POLL_LOG.json -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | awk '{print $2}')
[ -z "$latest" ] && exit 0
proj=$(echo "$latest" | sed -E 's#.*/03_NOVELLS/([0-9]+_[A-Z_]+)/.*#\1#')
case "$proj" in
  05_ORCHID) k=orchid ;;
  02_KINGMAKER) k=km ;;
  01_ELEYIA) k=eleyia ;;
  10_VIENNA_SPECIAL) k=vs ;;
  *) exit 0 ;;
esac
o=$(python3 "$ROOT/09_GENERAL/tools/affinity-tally.py" "$k" 2>&1)
[ -z "$o" ] && exit 0
jq -n --arg t "$o" \
  '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:("📊 "+$t)}}'
