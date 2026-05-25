import os
import re
from datetime import datetime

# Конфигурация
BASE_DIR = "/home/levdanskiy/.gemini"
CALENDAR_FILE = os.path.join(BASE_DIR, "system/calendars/YV_ESC_Live_Calendar.md")
WORKFLOW_DIR = os.path.join(BASE_DIR, "system/workflow")
STATE_FILE = os.path.join(BASE_DIR, "STATE.md")

def get_current_date():
    """Получает текущую системную дату."""
    return datetime.now()

def parse_calendar(file_path, target_date):
    """Ищет события на указанную дату в календаре."""
    events = []
    target_str = target_date.strftime("%d.%m")
    
    if not os.path.exists(file_path):
        print(f"Calendar file {file_path} not found.")
        return events
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        # Ищем форматы **28.12:** или **28.12**
        if f"**{target_str}:**" in line or f"**{target_str}**" in line:
            clean_line = line.strip().replace('*', '').replace('`', '')
            # Извлекаем текст после даты
            if ":" in clean_line:
                event_text = clean_line.split(":", 1)[1].strip()
            else:
                event_text = clean_line.strip()
            
            if event_text:
                events.append(event_text)
            
    return events

def update_daily_plan(date, events):
    """Добавляет события в ежедневный план."""
    plan_file = os.path.join(WORKFLOW_DIR, f"daily_plan_{date.strftime('%d.%m')}.md")
    
    if not os.path.exists(plan_file):
        print(f"Plan file {plan_file} not found. Skipping.")
        return

    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_tasks = []
    for event in events:
        # Проверяем, нет ли уже такого события в плане (по ключевым словам)
        if event[:20] not in content:
            # Формируем задачу
            task = f"*   ⚠️ `09:00` - 🔴 **#LIVE_TODAY:** {event} - ⬜ `[ОЖИДАНИЕ]`\n"
            new_tasks.append(task)
            
    if new_tasks:
        # Ищем место для вставки (после заголовка задач)
        # Обычно это после "### Workflow" или аналогичного
        header_match = re.search(r"### .+|#### .+", content)
        if header_match:
            insert_pos = header_match.end()
            new_content = content[:insert_pos] + "\n" + "".join(new_tasks) + content[insert_pos:]
            
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added {len(new_tasks)} live events to {plan_file}")
        else:
            # Если заголовка нет, просто в конец
            with open(plan_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "".join(new_tasks))
            print(f"Added {len(new_tasks)} live events to the end of {plan_file}")
    else:
        print("No new live events to add or plan already up to date.")

def main():
    today = get_current_date()
    print(f"Checking Live Calendar for {today.strftime('%d.%m.%Y')}")
    
    events = parse_calendar(CALENDAR_FILE, today)
    
    if events:
        print(f"Found events: {events}")
        update_daily_plan(today, events)
    else:
        print("No events found for today.")

if __name__ == "__main__":
    main()