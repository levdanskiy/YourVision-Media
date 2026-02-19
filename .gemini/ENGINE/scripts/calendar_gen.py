import sys
import os
import re
from datetime import datetime, timedelta

# CONFIG
CALENDAR_FILE = ".gemini/KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md"
OUTPUT_DIR = ".gemini/CONTENT/posts/2026"

def parse_calendar():
    if not os.path.exists(CALENDAR_FILE): return []
    with open(CALENDAR_FILE, 'r') as f: lines = f.readlines()
    
    events = []
    current_year = "2026"
    
    for line in lines:
        # Regex для строк типа: "28.02 🇫🇮 Финляндия: Финал UMK (21:00)"
        # Или "16-21.02 ..."
        match = re.search(r"(\d{2}\.\d{2}|\d{2}-\d{2}\.\d{2})\s+(.*)", line)
        if match:
            date_str = match.group(1)
            desc = match.group(2).strip()
            
            # Обработка диапазонов 16-21.02 -> берем дату старта 16.02
            if "-" in date_str:
                start_date = date_str.split("-")[0] + date_str.split("-")[1][-3:]
                clean_date = start_date
            else:
                clean_date = date_str
                
            events.append({
                "date": clean_date, # DD.MM
                "desc": desc,
                "full_line": line.strip()
            })
    return events

def generate_weekly():
    events = parse_calendar()
    today = datetime.now()
    end_date = today + timedelta(days=7)
    
    # Фильтр на неделю
    weekly_events = []
    for e in events:
        try:
            d = datetime.strptime(e['date'] + ".2026", "%d.%m.%Y")
            if today <= d <= end_date:
                weekly_events.append(e)
        except: continue

    if not weekly_events: return "Нет событий на эту неделю."

    # Формирование поста
    date_range = f"{today.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"
    post = f"// ИД: YV-WEEKLY-{today.strftime('%d%m')}\n"
    post += f"// ТИП: #WEEKLY_ROADMAP\n\n"
    post += f"📅 **YV: ROADMAP: ГЛАВНОЕ НА НЕДЕЛЕ ({date_range})**\n\n"
    post += "Сохраняйте расписание, чтобы не пропустить финалы и премьеры.\n\n"
    
    for e in weekly_events:
        post += f"**{e['date']}**\n{e['desc']}\n\n"
        
    post += "#YourVision #Eurovision2026 #Roadmap"
    return post

def generate_daily_guide():
    events = parse_calendar()
    today_str = datetime.now().strftime("%d.%m")
    
    daily_events = [e for e in events if e['date'] == today_str]
    
    if not daily_events: return "Сегодня эфиров нет."

    post = f"// ИД: YV-GUIDE-{datetime.now().strftime('%d%m')}\n"
    post += f"// ТИП: #LIVE_GUIDE\n\n"
    post += f"📺 **YV: LIVE GUIDE: ГДЕ СМОТРЕТЬ СЕГОДНЯ ({today_str})**\n\n"
    post += "Все ссылки на прямые трансляции в одном месте.\n\n"
    
    for e in daily_events:
        post += f"🔹 **{e['desc']}**\n"
        post += "🔗 Ссылка: [Ожидается]\n\n"
        
    post += "Обсуждаем эфиры в комментариях! 👇\n"
    post += "#YourVision #Live #Eurovision2026"
    return post

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "help" 
    
    if mode == "week":
        print(generate_weekly())
    elif mode == "guide":
        print(generate_daily_guide())
    else:
        print("Usage: python3 calendar_gen.py [week|guide]")