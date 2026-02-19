#!/bin/bash

# --- YOURVISION MEDIA SHORTCUTS ---

# 1. PUBLISHING
alias yv_pub='python3 .gemini/ENGINE/scripts/publish_tool.py'
alias yv_plan='python3 .gemini/ENGINE/scripts/daily_plan_gen.py'
alias yv_status='python3 .gemini/ENGINE/scripts/update_state.py && cat .gemini/CORE/STATE.md'

# 2. INTELLIGENCE
alias yv_time='python3 .gemini/ENGINE/scripts/true_time.py'
alias yv_odds='python3 .gemini/ENGINE/scripts/intel_hub.py "Odds"'
alias yv_charts='python3 .gemini/ENGINE/scripts/intel_hub.py "Charts"'

# 3. GIT & SYNC
alias yv_sync='git add . && git commit -m "Auto-sync: Content Update" && git push'
alias yv_save='git add . && git commit -m'

# 4. MAINTENANCE
alias yv_clean='rm .gemini/tmp/*'
alias yv_recover='python3 .gemini/ENGINE/scripts/recover_session.py'
alias yv_help='cat .gemini/COMMAND_REFERENCE.md'

echo "✅ YourVision Shortcuts Activated!"
echo "Try: yv_pub, yv_plan, yv_sync, yv_time"
alias yv_week='python3 .gemini/ENGINE/scripts/calendar_gen.py week'
alias yv_guide='python3 .gemini/ENGINE/scripts/calendar_gen.py guide'
alias yv_history='python3 .gemini/ENGINE/scripts/history_engine.py'
