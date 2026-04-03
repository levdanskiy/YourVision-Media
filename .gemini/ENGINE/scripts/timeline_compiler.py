#!/usr/bin/env python3
import re
import os
import arrow

def compile_today():
    today = "24.01" # В будущем будем брать динамически из pulse.py
    plans_dir = ".gemini/system/workflow/"
    daily_plan_path = f"{plans_dir}daily_plan_{today}.md"
    
    if not os.path.exists(daily_plan_path):
        print(f"❌ План на {today} не найден.")
        return

    with open(daily_plan_path, 'r') as f:
        content = f.read()

    # Ищем строки вида: * `HH:mm` | CHANNEL | #TAG: Topic - ⬜
    events = re.findall(r"\* `(\d{2}:\d{2})` \| (\w+) \| (.*?) - (✅|⬜)", content)
    
    print(f"--- 📅 TIMELINE ДЛЯ {today} ---")
    for time, channel, topic, status in sorted(events):
        print(f"{time} | {channel:2} | {status} | {topic[:40]}...")
    print("-------------------------------")

if __name__ == "__main__":
    compile_today()
