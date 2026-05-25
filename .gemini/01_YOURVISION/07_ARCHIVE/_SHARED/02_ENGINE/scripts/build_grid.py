#!/usr/bin/env python3
import os
import re
import sys
import arrow
import json

BASE_DIR = "/home/levdanskiy/.gemini/"
TIMELINE_DIR = BASE_DIR + "TIMELINE/"
KNOWLEDGE_DIR = BASE_DIR + "KNOWLEDGE/"
FEEDS_DIR = BASE_DIR + "ENGINE/feeds/"

def get_context(date_str):
    context = []
    h_file = FEEDS_DIR + "global_holidays.json"
    if os.path.exists(h_file):
        with open(h_file, 'r') as f:
            h = json.load(f)
            target_iso = f"2026-{date_str.split('.')[1]}-{date_str.split('.')[0]}"
            today_h = [x for x in h if x['date'] == target_iso]
            for x in today_h[:3]: context.append(f"🚩 {x['countryCode']}: {x['name']}")
    
    g_cal = KNOWLEDGE_DIR + "Live_Calendars/GLOBAL_Events_2026.md"
    if os.path.exists(g_cal):
        with open(g_cal, 'r') as f:
            content = f.read()
            if date_str in content:
                for line in content.split('\n'):
                    if date_str in line and "-" in line:
                        context.append(f"🌍 {line.strip('- ').strip()}")
    return context

def build_grid(target_date):
    now = arrow.now()
    real_today = now.format('DD.MM')
    day_target, mon_target = target_date.split('.')
    month_folder = mon_target.zfill(2)
    
    out_path = os.path.join(TIMELINE_DIR, "daily_workflow", f"daily_plan_{target_date}.md")
    
    # 1. ЗАХВАТ ИСТОРИИ И ЗАМЕТОК ИЗ ТЕКУЩЕГО ФАЙЛА
    history_done_raw = []
    manual_notes = ""
    if os.path.exists(out_path):
        with open(out_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Сохраняем готовые посты
            for line in content.split('\n'):
                if "✅" in line:
                    history_done_raw.append(line.strip())
            
            # Сохраняем раздел заметок
            notes_match = re.search(r"### 📝 ЗАМЕТКИ(.*?)(?=---|\Z)", content, re.DOTALL)
            if notes_match:
                manual_notes = notes_match.group(1).strip()

    # ... (rest of the script logic) ...
    # 4. Сборка финального текста (в конце функции)
    # ...
    md += "### 🔗 SYNERGY MAP\n* **AC + YV:** Аналитика мудрости и ML.\n* **NB + SW:** Артефакты вкуса.\n\n"
    
    if manual_notes:
        md += f"### 📝 ЗАМЕТКИ\n{manual_notes}\n\n"
    else:
        md += "### 📝 ЗАМЕТКИ\n*(Место для ваших ручных правок и уточнений)*\n\n"

    md += f"---\n**📊 GRID DENSITY:** {sum(len(v) for v in events_by_channel.values())} постов"

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"✅ План {target_date} пересобран. Все данные и заметки сохранены.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "24.01"
    build_grid(target)