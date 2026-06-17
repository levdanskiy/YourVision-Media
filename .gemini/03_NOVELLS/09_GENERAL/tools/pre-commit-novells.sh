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
# CHECK 1: Em-dashes (AUTO-FIX)
# ============================================
# Auto-replaces em-dashes with hyphens (python, NOT sed - sed once truncated a file).
# Allowed exceptions kept intact: demonstration lines citing the rule itself
# ("Эм-тире (—)", "никогда —" in NOVELLS_OS / VOICE_LOCK).
for file in $STAGED; do
  if [ ! -f "$file" ]; then continue; fi

  bad_lines=$(grep -n "—" "$file" 2>/dev/null \
    | grep -v "Эм-тире (—)" \
    | grep -v "никогда —" \
    || true)

  if [ -n "$bad_lines" ]; then
    if command -v python3 >/dev/null 2>&1; then
      python3 - "$file" <<'PYEOF'
import sys
p = sys.argv[1]
with open(p, encoding="utf-8") as f:
    lines = f.readlines()
out, n = [], 0
for line in lines:
    if "Эм-тире (—)" in line or "никогда —" in line:
        out.append(line)
    else:
        n += line.count("—")
        out.append(line.replace("—", "-"))
with open(p, "w", encoding="utf-8") as f:
    f.writelines(out)
print(f"   🔧 авто-фикс: {n} эм-тире -> дефис")
PYEOF
      git add "$file"
      echo "🔧 ЭМ-ТИРЕ исправлены автоматически: $file"
    else
      echo ""
      echo "❌ ЭМ-ТИРЕ в файле (python3 недоступен, авто-фикс невозможен): $file"
      echo "$bad_lines" | head -10
      ERROR=1
    fi
  fi
done

# ============================================
# CHECK 2: Character names in image prompts (WARNING)
# ============================================
KNOWN_NAMES="Alex|Theodora|Erik|Marco|KORYNNYA|Korynnya|Julien|Klara|Linus|Klavis|Adrian|Leon|Damien|Beatrice|Isabella|Khloe|Chloe|Nora|Max|Lukas|Berg|Vossen|Johansson|V-DYNAMO|Weiss|Stil|Vitri|Clerc|Helena|Stefan|Victoria|Maximilian|Laurent|Nikolya|Sophie|Camille|Valentina|Bruno|Marcel|Adelina|Hugo|Lindt|Andre|Jan|Mikas|Dorian|Felix|Oeron|Elias|Reinis|Marta|Elara|Alaric|Simas|Vika|Ula|Anya|Strazds|Kalejs|Greta|Foss|Theo|Renata|Alexander|Elza|Liga|Ansis|Ozols|Zanis|Ilze|Berzins|Kaspars|Maija|Anete|Gustavs|Karlis|Snegurochka|Lel|Mizgir|Moroz|Vesna|Siegfried"
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
# CHECK 3: Voice-lint (per-project rules)
# ============================================
# Resolve actual script directory via symlink (hook is symlinked from .git/hooks/pre-commit)
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
VOICE_LINT="$SCRIPT_DIR/voice-lint.sh"

if [ -x "$VOICE_LINT" ]; then
  for file in $STAGED; do
    if [ ! -f "$file" ]; then continue; fi
    # Только content-файлы (не system-файлы вроде STATE.md, POLL_LOG.md, VOICE_LOCK.md)
    if ! echo "$file" | grep -q "04_CONTENT"; then continue; fi

    output=$("$VOICE_LINT" --auto "$file" 2>&1) || true
    exit_code=$?
    if [ $exit_code -eq 1 ]; then
      # Блокирующие ошибки
      echo ""
      echo "❌ voice-lint ошибки в: $file"
      echo "$output" | sed 's/^/   /'
      ERROR=1
    elif [ $exit_code -eq 2 ]; then
      # Только предупреждения - показать, не блокировать
      echo ""
      echo "⚠️  voice-lint предупреждения в: $file"
      echo "$output" | sed 's/^/   /'
      WARN=1
    fi
  done
fi

# ============================================
# RESULT
# ============================================
if [ "$ERROR" -ne 0 ]; then
  echo ""
  echo "✋ Коммит заблокирован."
  echo "   Эм-тире (—): замени на дефис: sed -i 's/—/-/g' [file]"
  echo "   Voice-lint: проверь VOICE_LOCK проекта"
  exit 1
fi

if [ "$WARN" -ne 0 ]; then
  echo ""
  echo "⚠️  Предупреждения не блокируют коммит, но желательно исправить."
fi

echo "✅ NOVELLS checks passed."
exit 0
