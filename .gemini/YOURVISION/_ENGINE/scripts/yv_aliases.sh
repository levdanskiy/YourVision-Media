#!/bin/bash

# --- YOURVISION MEDIA SHORTCUTS (V2.5) ---

# 1. CORE PUBLISHING ENGINE
alias yv_plan='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py plan'
alias yv_guide='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py guide'
alias yv_week='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py week'
alias yv_history='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py history'
alias yv_pub='python3 ~/.gemini/ENGINE/scripts/yv_aliases.py pub'

# 2. VALIDATION & SYNC
alias yv_validate='python3 ~/.gemini/ENGINE/scripts/publish_tool.py'
alias yv_sync='python3 ~/.gemini/ENGINE/scripts/triple_sync.py'

# 3. MAINTENANCE
alias yv_clean='rm ~/.gemini/tmp/*'
alias yv_help='cat ~/.gemini/KNOWLEDGE/CHEATSHEET.md'

echo "🎛️ YourVision 2.5 Shortcuts Activated!"alias yv_tg='python3 ~/.gemini/ENGINE/scripts/telegram_bot.py'
