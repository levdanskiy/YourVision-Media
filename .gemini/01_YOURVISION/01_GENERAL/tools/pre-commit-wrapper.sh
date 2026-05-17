#!/usr/bin/env bash
# Pre-commit wrapper - chains all per-project pre-commit checks.
# Install: ln -sf "$(pwd)/.gemini/01_YOURVISION/01_GENERAL/tools/pre-commit-wrapper.sh" .git/hooks/pre-commit

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
EXIT=0

# Novells checks
NOVELLS_HOOK="$REPO_ROOT/.gemini/03_NOVELLS/09_GENERAL/tools/pre-commit-novells.sh"
if [ -x "$NOVELLS_HOOK" ]; then
  "$NOVELLS_HOOK" || EXIT=$?
fi

# YV checks
YV_HOOK="$REPO_ROOT/.gemini/01_YOURVISION/01_GENERAL/tools/pre-commit-yv.sh"
if [ -x "$YV_HOOK" ]; then
  "$YV_HOOK" || EXIT=$?
fi

exit $EXIT
