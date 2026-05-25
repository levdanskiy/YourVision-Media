#!/usr/bin/env python3
import os
import re
from datetime import datetime

BASE_DIR = "/home/levdanskiy/.gemini"
MOON_FILE = os.path.join(BASE_DIR, "system/calendars/AC_Moon_Phases.md")

def get_moon_phase():
    today_str = datetime.now().strftime("%d.%m.%Y")
    
    if not os.path.exists(MOON_FILE):
        return "Unknown", "Moon calendar not found."

    with open(MOON_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ищем сегодняшнюю фазу
    match = re.search(fr'\| {today_str} \| (.*?) \| (.*?) \|', content)
    if match:
        phase = match.group(1).strip()
        advice = match.group(2).strip()
        return phase, advice
    return "Unknown", "No data for today."

if __name__ == "__main__":
    phase, advice = get_moon_phase()
    print(f"🌙 ФАЗА ЛУНЫ: {phase}")
    print(f"🔮 СОВЕТ: {advice}")
