#!/usr/bin/env bash
# Pre-commit hook for Novells content
# Source: .gemini/03_NOVELLS/09_GENERAL/tools/pre-commit-novells.sh
# Install: ln -sf "$(pwd)/.gemini/03_NOVELLS/09_GENERAL/tools/pre-commit-novells.sh" .git/hooks/pre-commit
#
# Checks performed on staged .md files under 03_NOVELLS:
#   1. BLOCKING: em-dashes (—) must not appear in Novells files
#   2. WARNING:  image prompts must include a character name (not just generic descriptor)
#
# Safe to install repo-wide: only checks files under 03_NOVELLS, ignores everything else.

set -uo pipefail

# Get staged .md files under 03_NOVELLS
STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep -E "03_NOVELLS.*\.md$" || true)

if [ -z "$STAGED" ]; then
  exit 0
fi

echo "🔍 NOVELLS pre-commit checks..."

ERROR=0
WARN=0

# ============================================
# CHECK 1: Em-dashes (BLOCKING)
# ============================================
# Allowed exceptions: lines that explicitly cite the rule itself
# (NOVELLS_OS, VOICE_LOCK files have demonstration lines like "Эм-тире (—) нет нигде?")
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
# CHECK 2: Character names in image prompts (WARNING)
# ============================================
KNOWN_NAMES="Alex|Theodora|Erik|Marco|KORYNNYA|Korynnya|Julien|Klara|Linus|Klavis|Adrian|Leon|Damien|Beatrice|Isabella|Khloe|Chloe|Nora|Max|Lukas|Berg|Vossen|Johansson|V-DYNAMO|Vossen|Weiss|Stil|Vitri|Clerc"
GENERIC_DESCRIPTORS="young woman|young man|professional woman|tall woman|tall man|petite woman|young professional|woman in her|man in his|middle-aged woman|middle-aged man"

for file in $STAGED; do
  if [ ! -f "$file" ]; then continue; fi

  # Skip files that aren't in 04_CONTENT (system files don't have prompts to artists)
  if ! echo "$file" | grep -q "04_CONTENT"; then continue; fi

  # Extract prompt section
  prompt_lines=$(awk '/^\*\*Prompt:\*\*/{flag=1} flag' "$file" 2>/dev/null || true)

  if [ -z "$prompt_lines" ]; then continue; fi

  has_generic=$(echo "$prompt_lines" | grep -E -i "$GENERIC_DESCRIPTORS" || true)
  has_name=$(echo "$prompt_lines" | grep -E "$KNOWN_NAMES" || true)

  if [ -n "$has_generic" ] && [ -z "$has_name" ]; then
    echo ""
    echo "⚠️  В $file - промпт с обобщённым описанием без имени персонажа."
    echo "   Правило: в Novells всегда писать имя (Alex / Theodora / etc.)"
    WARN=1
  fi
done

# ============================================
# RESULT
# ============================================
if [ "$ERROR" -ne 0 ]; then
  echo ""
  echo "✋ Коммит заблокирован: эм-тире (—) запрещены в Novells."
  echo "   Замени на дефис: sed -i 's/—/-/g' [file]"
  exit 1
fi

if [ "$WARN" -ne 0 ]; then
  echo ""
  echo "⚠️  Предупреждения не блокируют коммит, но желательно исправить."
fi

echo "✅ NOVELLS checks passed."
exit 0
