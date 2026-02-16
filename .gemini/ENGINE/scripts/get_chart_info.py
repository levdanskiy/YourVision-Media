#!/usr/bin/env python3
import sys
import re
import datetime

def get_chart_for_date(target_date_str):
    schedule_path = ".gemini/system/calendars/YV_Charts_Schedule.md"
    
    try:
        with open(schedule_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return "Error: Schedule file not found."

    # Ищем блок с датой
    # Формат в файле: #### 📅 27.01.2026 (Вторник)
    pattern = re.compile(r'#### 📅 ' + re.escape(target_date_str) + r'.*?(?=#### 📅|$)', re.DOTALL)
    match = pattern.search(content)
    
    if match:
        block = match.group(0)
        
        # Парсим Финал
        final_match = re.search(r'🏆 \*\*ФИНАЛ \(19:20\):\*\* (.*)', block)
        final_chart = final_match.group(1).strip() if final_match else "None"
        
        # Парсим Старт
        start_match = re.search(r'🆕 \*\*СТАРТ \(20:30\):\*\* (.*)', block)
        start_chart = start_match.group(1).strip() if start_match else "None"
        
        return f"📅 **DATE:** {target_date_str}\n🏆 **RESULTS (19:20):** {final_chart}\n🆕 **ANNOUNCE (20:30):** {start_chart}"
    else:
        return "No chart scheduled for this specific date."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Если дата не передана, берем сегодня
        target_date = datetime.datetime.now().strftime("%d.%m.%Y")
    else:
        target_date = sys.argv[1]
        
    print(get_chart_for_date(target_date))