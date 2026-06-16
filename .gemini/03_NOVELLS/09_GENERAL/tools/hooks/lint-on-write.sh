#!/usr/bin/env bash
# Claude-хук PostToolUse (Write|Edit): линт Novells-поста сразу при записи.
# Если файл - пост в 04_CONTENT и voice-lint дал ошибки/предупреждения, отдаёт их обратно в контекст.
# Тихо выходит для любых других файлов.
ROOT=/home/levdanskiy/.gemini/03_NOVELLS
f=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
case "$f" in
  */03_NOVELLS/*/04_CONTENT/*.md) ;;
  *) exit 0 ;;
esac
o=$(bash "$ROOT/09_GENERAL/tools/voice-lint.sh" --auto "$f" 2>&1)
[ $? -eq 0 ] && exit 0
jq -n --arg t "$o" --arg f "$f" \
  '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:("⚠ voice-lint "+$f+":\n"+$t)}}'
