#!/usr/bin/env python3
import sys
import subprocess
import os

def get_full_digest(date_str):
    # 1. Берем наши внутренние планы
    # (логика из старого скрипта...)
    
    # 2. Берем всемирные праздники
    res = subprocess.run([sys.executable, ".gemini/system/scripts/world_holidays.py", date_str], capture_output=True, text=True)
    global_holidays = res.stdout.strip()
    
    print("🌍 WORLD HOLIDAYS:")
    print(global_holidays)
    print("\n🏛️ OUR SCHEDULE:")
    # Тут будет вывод из календарей...

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    get_full_digest(sys.argv[1])