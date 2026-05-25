#!/usr/bin/env bash
# ==============================================================================
# yv_publish.sh - Unified YourVision 2.6 Post Publisher & Automator
# Usage: ./yv_publish.sh <path_to_post.md>
# ==============================================================================

set -e

FILE="$1"

if [ -z "$FILE" ]; then
    echo -e "\033[1;31m❌ ERROR: Please specify a post file path.\033[0m"
    echo "Usage: ./yv_publish.sh <04_CONTENT/.../YV-post.md>"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo -e "\033[1;31m❌ ERROR: File '$FILE' does not exist.\033[0m"
    exit 1
fi

echo -e "\033[1;34m⚡ Starting YourVision 2.6 Unified Publication Pipeline...\033[0m"
echo "--------------------------------------------------------"

# 1. Run Style Audit
python3 /home/levdanskiy/yv_audit.py "$FILE"
echo ""

# 2. Run Time Sentinel Validation
python3 /home/levdanskiy/time_sentinel.py "$FILE"
echo ""



# 4. Extract Post metadata for Git Commit Message
POST_ID=$(grep -E "^//\s*ИД-ПОСТА:" "$FILE" | head -n1 | cut -d':' -f2- | xargs)
TOPIC=$(grep -E "^//\s*ТЕМА:" "$FILE" | head -n1 | cut -d':' -f2- | xargs)

if [ -z "$POST_ID" ]; then
    POST_ID=$(basename "$FILE" .md)
fi

if [ -z "$TOPIC" ]; then
    TOPIC="Content Update"
fi

echo -e "\033[1;34m📦 Preparing Git Commit for publication...\033[0m"
# Stage only the specific post file and synchronized project files
git add "$FILE"
git add .gemini/01_YOURVISION/02_KNOWLEDGE/YV_Season_2026.md 2>/dev/null || true
git add .gemini/01_YOURVISION/02_KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md 2>/dev/null || true
git add .gemini/01_YOURVISION/08_HUB/data.js 2>/dev/null || true
git add YourEurovision_Hub_Deploy/data.js 2>/dev/null || true

# Commit and Push
COMMIT_MSG="feat: publish $POST_ID - $TOPIC"
echo "Commit message: '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG"

echo -e "\033[1;34m🚀 Pushing updates to GitHub...\033[0m"
git push origin main

echo "--------------------------------------------------------"
echo -e "\033[1;32m✅ SUCCESS: Post successfully audited, synced with Hub, and pushed to Git main!\033[0m"
echo -e "\033[1;36m🏆 Antigravity CLI Operations Sentinel V1.0 compliant.\033[0m"
