#!/usr/bin/env python3
import sys
import re
import os

def check_sync():
    master_path = ".gemini/system/calendars/YV_ESC_Live_Calendar.md"
    plan_path = ".gemini/system/calendars/2026/01/YV_Plan_01.md"
    
    if not os.path.exists(master_path) or not os.path.exists(plan_path):
        return
        
    with open(master_path, 'r', encoding='utf-8') as f:
        master_content = f.read()
        
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan_content = f.read()
        
    # Ищем все даты в мастере (формат 24.01)
    dates = re.findall(r'\*\*(\d{2}\.01)\*\*', master_content)
    
    print("🔍 Проверка синхронизации планов с ТГ-календарем...")
    for d in dates:
        if d not in plan_content:
            print(f"⚠️ MISSING: Дата {d} есть в ТГ-календаре, но отсутствует в YV_Plan_01.md!")
        else:
            print(f"✅ {d} synced.")

if __name__ == "__main__":
    check_sync()
