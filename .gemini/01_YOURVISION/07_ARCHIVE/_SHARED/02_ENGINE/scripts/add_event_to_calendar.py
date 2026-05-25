import os
import sys
import re
from datetime import datetime

# Конфигурация
BASE_DIR = "/home/levdanskiy/.gemini"
CALENDAR_FILE = os.path.join(BASE_DIR, "system/calendars/YV_ESC_Live_Calendar.md")

MONTHS_RU = {
    1: "ЯНВАРЬ", 2: "ФЕВРАЛЬ", 3: "МАРТ", 4: "АПРЕЛЬ", 5: "МАЙ", 6: "ИЮНЬ",
    7: "ИЮЛЬ", 8: "АВГУСТ", 9: "СЕНТЯБРЬ", 10: "ОКТЯБРЬ", 11: "НОЯБРЬ", 12: "ДЕКАБРЬ"
}

def add_event(date_str, country, event, link=None):
    """Добавляет событие в календарь."""
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use DD.MM.YYYY")
        return

    day_str = date_obj.strftime("%d.%m")
    month_name = MONTHS_RU[date_obj.month]
    year = date_obj.year
    
    # Формируем строку события
    event_line = f"    *   {country}: {event}"
    if link:
        # Пытаемся сделать ссылку Markdown, если link похож на якорь или URL
        if link.startswith("#") or link.startswith("http"):
             event_line = f"    *   {country}: [{event}]({link})"
        else:
             event_line = f"    *   {country}: {event} ({link})" # Fallback

    with open(CALENDAR_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    month_found = False
    date_found = False
    inserted = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Ищем заголовок месяца
        # ### **ДЕКАБРЬ 2025 / ГРУДЕНЬ 2025**
        if f"### **{month_name} {year}" in line:
            month_found = True
            new_lines.append(line)
            i += 1
            continue
            
        if month_found and not inserted:
            # Если нашли следующий месяц или конец файла, вставляем дату и событие
            if line.startswith("###") or i == len(lines) - 1:
                if not date_found:
                     new_lines.append(f"*   〰️ **{day_str}:**\n")
                     new_lines.append(f"{event_line}\n")
                inserted = True
                month_found = False # Выходим из режима вставки в текущий месяц
            
            # Ищем дату внутри месяца
            # *   ✅ **17.12:**
            elif re.match(r"\*   .{1,2} \*\*" + re.escape(day_str) + r":\*\*", line):
                date_found = True
                new_lines.append(line)
                new_lines.append(f"{event_line}\n")
                inserted = True
                i += 1
                continue
                
            # Сортировка дат (упрощенная) - если текущая строка дата больше нашей
            elif line.startswith("*   "):
                 match = re.search(r"\*\*(\d{2})\.(\d{2}):\*\*", line)
                 if match:
                     curr_day = int(match.group(1))
                     if curr_day > date_obj.day:
                         if not date_found:
                             new_lines.append(f"*   〰️ **{day_str}:**\n")
                             new_lines.append(f"{event_line}\n")
                             inserted = True
        
        new_lines.append(line)
        i += 1

    if not month_found and not inserted:
        # Если месяц не найден вообще, нужно добавить его (сложно, пока пропустим)
        print(f"Warning: Month section for {month_name} {year} not found. Please add manually.")
    
    with open(CALENDAR_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Event added to {day_str} in {CALENDAR_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 add_event_to_calendar.py <DD.MM.YYYY> <Country_Icon+Name> <Event_Description> [Link]")
        sys.exit(1)
        
    date_arg = sys.argv[1]
    country_arg = sys.argv[2]
    event_arg = sys.argv[3]
    link_arg = sys.argv[4] if len(sys.argv) > 4 else None
    
    add_event(date_arg, country_arg, event_arg, link_arg)
