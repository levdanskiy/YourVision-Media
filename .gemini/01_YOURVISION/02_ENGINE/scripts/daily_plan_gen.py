import sys
import os
import re
import json
from datetime import datetime, timedelta

# YOURVISION 2.0 ADVANCED PLANNER (ULTIMATE)

def get_day_plan(date_str, channel):
    # Mapping for master plans folder structure
    month = date_str[3:5]
    path = f".gemini/TIMELINE/master_plans/{month}/{channel}_Plan_{month}.md"
    if not os.path.exists(path): return []
    with open(path, 'r') as f: content = f.read()
    day_short = date_str[:5] 
    pattern = rf"### {day_short}.*?\n(.*?)(?=\n###|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = match.group(1).strip().split('\n')
        return [l for l in lines if l.strip()]
    return []

def get_live_events_from_json(date_str):
    """Сбор событий из Базы Данных JSON"""
    db_path = ".gemini/TIMELINE/database/yv_season_2026.json"
    if not os.path.exists(db_path): return []
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    # Конвертируем дату DD.MM.YYYY -> YYYY-MM-DD
    target_date = datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    
    live_lines = []
    for event in db.get("events", []):
        if event["date"] == target_date:
            emoji = "🔴"
            if event["type"] == "ANNOUNCEMENT": emoji = "📻"
            if event["type"] == "RELEASE": emoji = "🎵"
            
            line = f"* {event['time']} | **YV** | {emoji} **#{event['type']}:** {event['country']}. {event['event']}."
            live_lines.append(line)
    
    return live_lines

def get_calendar_events(date_str):
    """Сбор событий из текстового Live Calendar (MD)"""
    cal_path = ".gemini/KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md"
    if not os.path.exists(cal_path): return []
    
    with open(cal_path, 'r') as f: lines = f.readlines()
    
    target_short = date_str[:5] # DD.MM
    cal_lines = []
    
    for line in lines:
        if line.startswith(target_short):
            # Парсим строку календаря
            clean_text = line.strip().replace(target_short, "").strip()
            # Пытаемся найти время в скобках (20:00)
            time_match = re.search(r"\((\d{2}:\d{2})\)", clean_text)
            time = time_match.group(1) if time_match else "TBA"
            
            # Формируем строку плана
            cal_lines.append(f"* {time} | **YV** | 🗓 **#EVENT:** {clean_text}")
            
    return cal_lines

def get_debts(current_date_str):
    try:
        curr_date = datetime.strptime(current_date_str, "%d.%m.%Y")
        prev_date = curr_date - timedelta(days=1)
        prev_str = prev_date.strftime("%d.%m")
        
        wf_dir = ".gemini/TIMELINE/daily_workflow"
        prev_file = None
        for f in os.listdir(wf_dir):
            if f.startswith(f"daily_plan_{prev_str}"):
                prev_file = os.path.join(wf_dir, f)
                break
        
        if not prev_file or not os.path.exists(prev_file):
            return []

        with open(prev_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        debts = []
        for line in lines:
            if "⬜" in line or "🔴" in line:
                clean_line = line.strip().replace("⬜ [ОЖИДАНИЕ]", "").replace("🔴 [ДОЛГ]", "").strip()
                if clean_line.startswith("*") or re.match(r"^\d+\.", clean_line):
                    clean_line = re.sub(r"\s*-\s*$", "", clean_line)
                    debts.append(clean_line + " -  🔴 [ДОЛГ]")
        return debts
    except:
        return []

def generate(date_str):
    header = f"# 📅 DAILY PLAN: {date_str} (YourVision 2.0)\n**// STATUS: GENERATED | AUTO-SYNC ENABLED //**\n\n"
    
    # 1. Сбор данных
    debts = get_debts(date_str)
    json_events = get_live_events_from_json(date_str)
    cal_events = get_calendar_events(date_str)
    
    # Объединяем события из JSON и MD, убирая дубликаты (похожие названия)
    # Приоритет у JSON (там точнее структура)
    unique_events = json_events.copy()
    json_texts = [e.split(":", 1)[1] for e in json_events if ":" in e]
    
    for c_e in cal_events:
        is_dup = False
        for j_t in json_texts:
            # Омичаем дубликат, если текст календаря содержится в JSON или наоборот
            # (очень упрощенно, но работает для основных названий)
            c_text = c_e.split(":", 1)[1]
            if c_text[:10] in j_t or j_t[:10] in c_text:
                is_dup = True
                break
        if not is_dup:
            unique_events.append(c_e)

    # 2. Мастер-планы
    yv_master = get_day_plan(date_str, "YV")
    
    # 3. ОБЯЗАТЕЛЬНЫЕ РУБРИКИ (Если их нет в Мастере)
    mandatory = [
        "* 09:00 | **YV** | 🗓 **#EVENTS:** Гид по событиям дня.",
        "* 13:00 | **YV** | 🎞 **#EUROFLASHBACK:** История дня."
    ]
    
    # 4. Объединение YV
    yv_all = unique_events + yv_master + mandatory
    
    # Сортировка по времени
    def get_time_sort(line):
        time_part = line.split('|')[0].strip().replace('*', '').strip()
        if not re.match(r"\d{2}:\d{2}", time_part): return "99:99" # TBA в конец
        return time_part

    yv_sorted = sorted(yv_all, key=get_time_sort)

    content = header
    
    if debts:
        content += "### 🚨 CRITICAL DEBTS\n" + "\n".join(debts) + "\n\n"
        content += "---\n\n"

    content += "### 📺 YOURVISION (Broadcaster)\n"
    for line in yv_sorted:
        if "✅" not in line and "🔴" not in line and "⬜" not in line:
            line = line.split(" - ")[0].strip()
            content += f"{line} - ⬜ [ОЖИДАНИЕ]\n"
        else:
            content += f"{line}\n"
    
    content += "\n---\n### 🧊 ARCHIVE CHANNELS (ON PAUSE)\n"
    content += "*(AC, NB, SW content will be added here only if requested)*\n"
    
    filename = f".gemini/TIMELINE/daily_workflow/daily_plan_{date_str[:5]}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Plan YourVision 2.0 generated: {filename}")
    if unique_events: print(f"LIVE: {len(unique_events)} events added from DB/Calendar.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 daily_plan_gen.py DD.MM.YYYY")
    else:
        generate(sys.argv[1])