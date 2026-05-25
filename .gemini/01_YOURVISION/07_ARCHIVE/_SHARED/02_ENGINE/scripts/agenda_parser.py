#!/usr/bin/env python3
import re
import os
import arrow

def get_today_events():
    calendar_path = ".gemini/system/calendars/YV_ESC_Live_Calendar.md"
    if not os.path.exists(calendar_path):
        return []

    with open(calendar_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Берем текущую дату из системы
    today = arrow.now().format('DD.MM')
    
    # Ищем строки вида: 〰️ 24.01: 🇱🇺 Люксембург - ...
    pattern = rf"〰️ {today}: (.*)"
    matches = re.findall(pattern, content)
    
    return matches

if __name__ == "__main__":
    events = get_today_events()
    if events:
        print(f"--- 📅 AGENDA FOR TODAY ({arrow.now().format('DD.MM')}) ---")
        for e in events:
            print(f"🌟 {e}")
    else:
        print("📭 No major ESC events scheduled for today.")
