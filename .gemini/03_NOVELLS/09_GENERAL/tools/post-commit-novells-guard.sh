#!/bin/sh
# NOVELLS safety guard (post-commit hook).
# Purpose: protect Novells commits from being orphaned when a parallel
# YourVision stream does `git reset` on `main`.
#
# Behaviour: whenever a commit touches 03_NOVELLS/, fast-forward the local
# branch `novells` to the new HEAD. NEVER moves `novells` backward.
# If `novells` has diverged from HEAD (i.e. main was reset and lost Novells
# work), it does NOT move the ref and prints a recovery hint instead.
#
# Installed as a symlink: .git/hooks/post-commit -> this file.
# Recovery after a main reset:  git merge novells   (or: git cherry-pick <range>)

set -e

# Did this commit touch Novells?
if ! git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null | grep -q '03_NOVELLS/'; then
  exit 0
fi

head=$(git rev-parse HEAD)

if git rev-parse --verify -q refs/heads/novells >/dev/null 2>&1; then
  nov=$(git rev-parse refs/heads/novells)
  base=$(git merge-base "$nov" "$head" 2>/dev/null || echo "")
  if [ "$nov" = "$head" ]; then
    exit 0                      # already in sync (e.g. committed while on novells)
  elif [ "$base" = "$nov" ]; then
    git update-ref refs/heads/novells "$head"   # safe fast-forward
    echo "[novells-guard] advanced 'novells' -> $(git rev-parse --short "$head")"
  else
    echo "[novells-guard] WARNING: 'novells' diverged from HEAD - main may have been reset." 1>&2
    echo "[novells-guard] Novells work is preserved on branch 'novells'. Recover with: git merge novells" 1>&2
  fi
else
  git update-ref refs/heads/novells "$head"
  echo "[novells-guard] created 'novells' -> $(git rev-parse --short "$head")"
fi
