import os
import re
from datetime import datetime, timedelta

# Конфигурация путей
BASE_DIR = "/home/levdanskiy/.gemini"
LIVE_CALENDAR_FILE = os.path.join(BASE_DIR, "system/calendars/YV_ESC_Live_Calendar.md")
WORKFLOW_DIR = os.path.join(BASE_DIR, "system/workflow")

def get_current_date():
    """Получает текущую дату (симуляционную) для формирования имени файла плана."""
    return datetime(2025, 12, 24) # Для симуляции, так как сегодня 24.12

def generate_pulse_content(start_date, days=7):
    """Генерирует контент для поста 'Пульс Недели'."""
    end_date = start_date + timedelta(days=days)
    
    content_ru = f"📅 **#ПУЛЬС_НЕДЕЛИ:** ГЛАВНЫЕ СОБЫТИЯ НА YOURVISION (с {start_date.strftime('%d.%m')} по {end_date.strftime('%d.%m')})!\n\n"
    content_ua = f"📅 **#ПУЛЬС_ТИЖНЯ:** ГОЛОВНІ ПОДІЇ НА YOURVISION (з {start_date.strftime('%d.%m')} по {end_date.strftime('%d.%m')})!\n\n"
    
    events_ru = []
    events_ua = []
    
    with open(LIVE_CALENDAR_FILE, 'r', encoding='utf-8') as f:
        calendar_content = f.read()
        
    # Парсим календарь построчно
    # TODO: Улучшить парсинг для более точного извлечения дат и событий
    current_month_ru = ""
    current_month_ua = ""
    
    # Регулярное выражение для поиска дат и событий в каждой строке
    # Пример: 〰️ **17.12:** 🇦🇱 **Албания:** Festivali i Këngës #64 (Полуфинал 1). / **Festivali i Këngës 64 (Півфінал 1).**
    event_pattern = re.compile(r"〰️ \*\*(\d{2}\.\d{2})\*\*:\s*(.+?)\s*\/\s*(.+)")
    month_pattern = re.compile(r"### \*\*(.+)\s(\d{4})\s\/\s(.+)\s(\d{4})\*\*") # ### **DECEMBER 2025 / ГРУДЕНЬ 2025**
    
    for line in calendar_content.splitlines():
        month_match = month_pattern.match(line)
        if month_match:
            current_month_ru = month_match.group(1).split(' ')[0]
            current_month_ua = month_match.group(3).split(' ')[0]
            continue
            
        event_match = event_pattern.match(line)
        if event_match:
            event_date_str = event_match.group(1)
            event_ru = event_match.group(2).strip()
            event_ua = event_match.group(3).strip()
            
            try:
                # Assuming all events are in 2025/2026 as per calendar
                event_date = datetime.strptime(f"{event_date_str}.2025", "%d.%m.%Y").date()
                if event_date >= start_date.date() and event_date <= end_date.date():
                    events_ru.append(f"■ {event_date_str}: {event_ru}")
                    events_ua.append(f"■ {event_date_str}: {event_ua}")
            except ValueError:
                # If year is 2026 (e.g. Jan 2026 events)
                try:
                    event_date = datetime.strptime(f"{event_date_str}.2026", "%d.%m.%Y").date()
                    if event_date >= start_date.date() and event_date <= end_date.date():
                        events_ru.append(f"■ {event_date_str}: {event_ru}")
                        events_ua.append(f"■ {event_date_str}: {event_ua}")
                except ValueError:
                    pass
                    
    content_ru += "\n".join(events_ru) + "\n\n"
    content_ua += "\n".join(events_ua) + "\n\n"

    # Добавляем стандартные хэштеги
    hashtags_ru = "#YourVision #ПульсНедели #Евровидение2026 #ESC2026"
    hashtags_ua = "#YourVisionUA #ПульсТижня #Євробачення2026 #ESC2026"
    
    final_content = f"{content_ru}{hashtags_ru}\n\n***\n\n{content_ua}{hashtags_ua}"
    
    return final_content

def main():
    today = get_current_date()
    # Для Пульса Недели обычно берут понедельник.
    # Если запускаем сегодня (среда 24.12), то берем ближайший понедельник
    # Или просто генерируем Пульс Недели от текущей даты.
    # Давайте сделаем Пульс на 7 дней вперед от текущей даты.
    
    pulse_content = generate_pulse_content(today)
    
    # Создаем пост в папке контента
    post_filename = f"YV-{today.strftime('%d.%m')}-PULSE_NEDELI.md"
    post_path = os.path.join(WORKFLOW_DIR, post_filename) # Создаем в workflow, чтобы потом перенести в content
    
    # Добавляем запись в daily_plan (тут нужно найти соответствующий понедельник)
    # Пока что, для тестирования, просто выведем контент
    print(pulse_content)

if __name__ == "__main__":
    main()
