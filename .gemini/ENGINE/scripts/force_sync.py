#!/usr/bin/env python3
import os
import re
import sys
import glob
from datetime import datetime

# Конфигурация
BASE_DIR = "/home/levdanskiy/.gemini"
POSTS_DIR = os.path.join(BASE_DIR, "posts")
WORKFLOW_DIR = os.path.join(BASE_DIR, "system/workflow")
CALENDARS_DIR = os.path.join(BASE_DIR, "system/calendars")

def get_posts_for_date(date_str):
    """Находит все посты за дату (DD.MM.YYYY)"""
    try:
        day, month, year = date_str.split('.')
    except:
        return []
        
    path = os.path.join(POSTS_DIR, year, month, day)
    
    if not os.path.exists(path):
        print(f"⚠️ Папка постов не найдена: {path}")
        return []

    posts = []
    for file in os.listdir(path):
        if file.endswith(".md"):
            # Format: CODE-DD.MM-HH-MM-Title.md
            parts = file.split('-')
            if len(parts) >= 4:
                channel = parts[0]
                time_str = f"{parts[2]}:{parts[3]}"
                posts.append({
                    'channel': channel,
                    'time': time_str,
                    'file': file,
                    'month': month
                })
    return posts

def update_daily_plan(date_str, posts):
    """Обновляет сводный план daily_plan_DD.MM.md"""
    day, month, year = date_str.split('.')
    short_date = f"{day}.{month}"
    plan_file = os.path.join(WORKFLOW_DIR, f"daily_plan_{short_date}.md")

    if not os.path.exists(plan_file):
        return

    print(f"🔧 Обработка дневного плана: {os.path.basename(plan_file)}")
    with open(plan_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section_channel = None
    section_map = {
        "### 🏛️ ALMANAC": "AC",
        "### 🌍 ALMANAC: NEIGHBORS": "NB",
        "### 🍰 ALMANAC: SWEET": "SW",
        "### 🎤 YOURVISION": "YV"
    }

    new_lines = []
    for line in lines:
        for section_title, channel_code in section_map.items():
            if section_title in line:
                current_section_channel = channel_code
                break

        updated_line = line
        for post in posts:
            if f"`{post['time']}`" in line and "⬜" in line:
                if current_section_channel == post['channel']:
                    updated_line = line.replace("⬜", "✅")
                    print(f"  ✅ [PLAN] {post['channel']} @ {post['time']} DONE")
        new_lines.append(updated_line)

    with open(plan_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def update_channel_calendars(date_str, posts):
    """Обновляет глобальные календари каналов (AC_Plan_01.md и т.д.)"""
    day, month, year = date_str.split('.')
    short_date = f"{day}.{month}"

    # Собираем все доступные файлы планов рекурсивно
    all_calendars = []
    for root, _, files in os.walk(CALENDARS_DIR):
        for file in files:
            if "_Plan_" in file and file.endswith(".md"):
                all_calendars.append(os.path.join(root, file))

    for cal_path in all_calendars:
        cal_name = os.path.basename(cal_path)
        # Определяем, к какому каналу и месяцу относится этот календарь
        # Формат: CODE_Plan_MM.md
        cal_channel = cal_name.split('_')[0]
        cal_month = cal_name.split('_')[2].replace('.md', '')

        with open(cal_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        current_date_context = None
        updated_any = False

        for line in lines:
            if short_date in line:
                current_date_context = short_date
            
            updated_line = line
            if current_date_context == short_date:
                for post in posts:
                    # Совпадение канала, месяца и времени
                    if post['channel'] == cal_channel and post['month'] == cal_month:
                        time_marker = f"`{post['time']}`"
                        if time_marker in line and "⬜" in line:
                            updated_line = line.replace("⬜", "✅")
                            if "[ГОТОВО]" not in updated_line and "*" in updated_line:
                                updated_line = updated_line.strip() + " - ✅ [ГОТОВО]\n"
                            print(f"  ✅ [CALENDAR] {cal_name}: {post['time']} DONE")
                            updated_any = True
            new_lines.append(updated_line)

        if updated_any:
            with open(cal_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

def main():
    target_date = datetime.now().strftime("%d.%m.%Y")
    if len(sys.argv) > 1:
        target_date = sys.argv[1]

    print(f"🚀 ЗАПУСК FORCE SYNC: {target_date}")
    posts = get_posts_for_date(target_date)
    
    if not posts:
        print("Посты не найдены.")
        return

    update_daily_plan(target_date, posts)
    update_channel_calendars(target_date, posts)
    print("🏁 Синхронизация завершена.")

if __name__ == "__main__":
    main()