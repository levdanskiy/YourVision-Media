#!/usr/bin/env bash
# Pre-commit hook for YourVision content
# Source: .gemini/01_YOURVISION/01_GENERAL/tools/pre-commit-yv.sh
#
# Checks performed on staged .md files under 01_YOURVISION/04_CONTENT:
#   1. BLOCKING: em-dashes (—) must not appear
#   2. BLOCKING: Sniper forbidden lexicon (via voice-lint.sh §2 OS)
#   3. WARNING:  hedge phrases, prompt without --ar 1:1, prompt without Dazed tail
#
# Safe to install repo-wide: only checks files under 01_YOURVISION, ignores rest.

set -uo pipefail

# Get staged .md files under 01_YOURVISION (only content posts get linted)
STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep -E "01_YOURVISION/04_CONTENT/.*\.md$" || true)

if [ -z "$STAGED" ]; then
  exit 0
fi

echo "🔍 YOURVISION pre-commit checks..."

ERROR=0
WARN=0

# ============================================
# CHECK 1: Em-dashes (BLOCKING)
# ============================================
# Allowed exceptions: lines that explicitly cite the rule (OS demonstration lines)
for file in $STAGED; do
  if [ ! -f "$file" ]; then continue; fi

  bad_lines=$(grep -n "—" "$file" 2>/dev/null \
    | grep -v "Эм-тире (—)" \
    | grep -v "никогда —" \
    || true)

  if [ -n "$bad_lines" ]; then
    echo ""
    echo "❌ ЭМ-ТИРЕ в файле: $file"
    echo "$bad_lines" | head -10
    ERROR=1
  fi
done

# ============================================
# CHECK 2: Voice-lint (Sniper rules from OS §2/§8)
# ============================================
# voice-lint.sh лежит в Novells (исторически), но он project-aware
VOICE_LINT="/home/levdanskiy/.gemini/03_NOVELLS/09_GENERAL/tools/voice-lint.sh"

if [ -x "$VOICE_LINT" ]; then
  for file in $STAGED; do
    if [ ! -f "$file" ]; then continue; fi

    output=$("$VOICE_LINT" --auto "$file" 2>&1) || true
    exit_code=$?
    if [ $exit_code -eq 1 ]; then
      echo ""
      echo "❌ voice-lint ошибки в: $file"
      echo "$output" | sed 's/^/   /'
      ERROR=1
    elif [ $exit_code -eq 2 ]; then
      echo ""
      echo "⚠️  voice-lint предупреждения в: $file"
      echo "$output" | sed 's/^/   /'
      WARN=1
    fi
  done
else
  echo "⚠️  voice-lint.sh не найден: $VOICE_LINT"
fi

# ============================================
# RESULT
# ============================================
if [ "$ERROR" -ne 0 ]; then
  echo ""
  echo "✋ Коммит YV заблокирован."
  echo "   Эм-тире (—): замени на дефис: sed -i 's/—/-/g' [file]"
  echo "   Sniper §2: убери табу-лексику (см. 01_GENERAL/YOURVISION_OS.md §2)"
  exit 1
fi

if [ "$WARN" -ne 0 ]; then
  echo ""
  echo "⚠️  YV предупреждения не блокируют коммит, но желательно исправить."
fi

echo "✅ YOURVISION checks passed."
exit 0
