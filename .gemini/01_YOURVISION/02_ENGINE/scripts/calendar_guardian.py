#!/usr/bin/env python3
import sys
import re
import os
import datetime

# Пути к календарям
CALENDAR_PATH = ".gemini/system/calendars/2026/01"
CHANNELS = {
    "AC": "AC_Plan_01.md",
    "NB": "NB_Plan_01.md",
    "SW": "SW_Plan_01.md",
    "YV": "YV_Plan_01.md"
}

def parse_daily_plan(daily_path):
    """Извлекает выполненные задачи из плана на день."""
    if not os.path.exists(daily_path):
        return []

    with open(daily_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ищем строки: | 12:00 | RU | #TOPIC: Title | ✅ |
    # Regex: \| (\d{2}:\d{2}) \| \*\*([A-Z]{2}|BI)\*\* \| \*\*(#[_]+):?\*\*(.*?) \| (✅|⬜)
    tasks = []
    
    # Разбиваем по секциям каналов
    sections = re.split(r'### ', content)
    
    for section in sections:
        channel = None
        if "ALMANAC (Main)" in section: channel = "AC"
        elif "NEIGHBORS" in section: channel = "NB"
        elif "SWEET" in section: channel = "SW"
        elif "YOURVISION" in section: channel = "YV"
        
        if not channel: continue

        lines = section.strip().split('\n')
        for line in lines:
            if "|" in line and "✅" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 4:
                    time = parts[1].replace('`', '')
                    # topic_raw = parts[3] # #TAG: Title
                    tasks.append({
                        "channel": channel,
                        "time": time,
                        "status": "DONE"
                    })
    return tasks

def sync_calendars(daily_file):
    """Обновляет месячные календари на основе daily_plan."""
    
    # 1. Извлекаем дату из имени файла daily_plan_23.01.md
    match = re.search(r'daily_plan_(\d{2}\.\d{2})\.md', daily_file)
    if not match:
        print("❌ Ошибка: Неверный формат имени файла daily_plan.")
        return
    
    date_key = match.group(1) # "23.01"
    day_num = date_key.split('.')[0] # "23"
    
    done_tasks = parse_daily_plan(daily_file)
    if not done_tasks:
        print(f"ℹ️ В {daily_file} нет выполненных задач для синхронизации.")
        return

    print(f"🔄 Синхронизация для даты {date_key}...")

    # 2. Проходим по каждому каналу
    for code, filename in CHANNELS.items():
        channel_tasks = [t for t in done_tasks if t['channel'] == code]
        if not channel_tasks:
            continue
            
        cal_file = os.path.join(CALENDAR_PATH, filename)
        if not os.path.exists(cal_file):
            print(f"⚠️ Календарь {filename} не найден.")
            continue

        with open(cal_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        # Ищем секцию даты. Формат в календаре: "**23.01 (Пятница)..." или "**23.01..."
        in_date_block = False
        
        for line in lines:
            # Проверка начала блока даты
            if line.strip().startswith(f"**{date_key}"):
                in_date_block = True
                new_lines.append(line)
                continue
            
            # Если начался другой день (ищем жирный шрифт с цифрами)
            if in_date_block and re.match(r'\*\*\d{2}\.\d{2}', line.strip()):
                in_date_block = False
            
            if in_date_block:
                # Ищем задачи в этом дне и обновляем статус
                updated_line = line
                for task in channel_tasks:
                    # Ищем совпадение времени. Формат: * `12:00` ...
                    if f"`{task['time']}`" in line:
                        if "✅" not in line:
                            # Заменяем статус
                            updated_line = re.sub(r'⬜ \[.*?\]', '✅ [ГОТОВО]', line)
                            if line != updated_line:
                                print(f"   ✅ {code} {task['time']} -> Updated in Calendar.")
                new_lines.append(updated_line)
            else:
                new_lines.append(line)

        # Запись обратно
        with open(cal_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calendar_guardian.py <daily_plan_file>")
        sys.exit(1)
    
    sync_calendars(sys.argv[1])
