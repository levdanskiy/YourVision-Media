#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime

BASE_DIR = "/home/levdanskiy/.gemini"
PLAN_DIR = os.path.join(BASE_DIR, "TIMELINE/daily_workflow")
MASTER_DIR = os.path.join(BASE_DIR, "TIMELINE/master_plans")

# Обновленные шаблоны YV V2.2
YV_STRUCTURE = {
    0: "### 📺 YOURVISION (Broadcaster)\n* 18:00 | **YV** | 🖋️ **#REVIEW:** [НАЗВАНИЕ ТРЕКА] (РЕЦЕНЗИЯ). - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)", # Mon
    1: "### 📺 YOURVISION (Broadcaster)\n* 19:15 | **YV** | 📊 **#CHART_RESULTS:** [ТЕКУЩИЙ ЧАРТ] (ИТОГИ). - ⬜ [ОЖИДАНИЕ]\n* 20:30 | **YV** | 📈 **#CHART_ANNOUNCE:** [НОВЫЙ ЧАРТ] (АНОНС). - ⬜ [ОЖИДАНИЕ]", # Tue
    2: "### 📺 YOURVISION (Broadcaster)\n* 18:00 | **YV** | 🖋️ **#REVIEW:** [НАЗВАНИЕ ТРЕКА] (РЕЦЕНЗИЯ). - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)", # Wed
    3: "### 📺 YOURVISION (Broadcaster)\n* 18:00 | **YV** | 🗳️ **#CHART_UPDATE:** НАПОМИНАНИЕ (MID-WEEK). - ⬜ [ОЖИДАНИЕ]\n* 20:00 | **YV** | 🖋️ **#REVIEW:** [НАЗВАНИЕ ТРЕКА] (РЕЦЕНЗИЯ). - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)", # Thu
    4: "### 📺 YOURVISION (Broadcaster)\n* 16:00 | **YV** | 🗳️ **#HYPEMETER_POLL:** ОПРОС ПЕРЕД ВЫХОДНЫМИ. - ⬜ [ОЖИДАНИЕ]", # Fri
    5: "### 📺 YOURVISION (Broadcaster)\n* 16:00 | **YV** | 🖋️ **#REVIEW:** ОБЗОР ОТБОРОВ. - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)", # Sat
    6: "### 📺 YOURVISION (Broadcaster)\n* 16:00 | **YV** | 🗣️ **#EXPERT_OPINION:** МНЕНИЯ ЭКСПЕРТОВ. - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)\n* 19:00 | **YV** | 📊 **#CHART_UPDATE:** ФИНАЛЬНЫЙ ОТСЧЕТ (FINAL CALL). - ⬜ [ОЖИДАНИЕ]" # Sun
}

def get_master_content(date_str, channel):
    """Ищет контент для конкретной даты и канала в мастер-планах."""
    # Определяем месяц для выбора папки (02, 03)
    month = date_str.split('.')[1]
    master_path = os.path.join(MASTER_DIR, month, f"{channel}_Plan_{month}.md")
    
    if not os.path.exists(master_path): return []
    
    content = []
    with open(master_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    capture = False
    for line in lines:
        if f"### {date_str[:5]}" in line:
            capture = True
            continue
        if capture and line.startswith("### "):
            break
        if capture and line.strip().startswith("*"):
            content.append(line.strip())
            
    return content

def generate_plan(date_str):
    try:
        dt = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        dt = datetime.strptime(date_str + ".2026", "%d.%m.%Y")
        
    day_short = date_str[:5]
    weekday = dt.weekday() # 0 = Mon, 6 = Sun
    
    plan = f"# 💎 СВОДНЫЙ ЭФИРНЫЙ ПЛАН: {date_str} ({dt.strftime('%A')})\n"
    plan += "**// СИНХРОНИЗАЦИЯ: MASTER PLAN + STRATEGY V2.2 //**\n\n"
    
    plan += f"## 🚨 КРИТИЧЕСКИЕ ДОЛГИ (ПЕРЕНОС)\n* (Нет критических долгов)\n\n"
    plan += f"## 🎯 СЕГОДНЯ: {date_str}\n\n"
    
    # 1. AC (Architect)
    plan += "### 🏛️ ALMANAC MAIN (Architect)\n"
    ac_content = get_master_content(date_str, "AC")
    if ac_content:
        plan += "\n".join(ac_content) + "\n"
    else:
        plan += "* 08:00 | **AC** | 📡 **#TIME_WHEEL:** [Тема]. - ⬜ [ОЖИДАНИЕ]\n"
        
    plan += "\n### 🌍 ALMANAC NEIGHBORS (Traveler)\n"
    nb_content = get_master_content(date_str, "NB")
    if nb_content:
        plan += "\n".join(nb_content) + "\n"
        
    plan += "\n### 🍰 ALMANAC SWEET (Hedonist)\n"
    sw_content = get_master_content(date_str, "SW")
    if sw_content:
        plan += "\n".join(sw_content) + "\n"
        
    # 4. YV (YourVision) - Гибридная логика
    # Сначала берем из мастер-плана (там чарты)
    yv_content = get_master_content(date_str, "YV")
    
    # Если в мастер-плане пусто, берем шаблон по дню недели
    if not yv_content:
        plan += "\n" + YV_STRUCTURE[weekday] + "\n"
    else:
        plan += "\n### 📺 YOURVISION (Broadcaster)\n"
        plan += "\n".join(yv_content) + "\n"
        # Добавляем опциональные слоты, если их нет в мастере
        if weekday == 3 and "REVIEW" not in "".join(yv_content): # Thu
             plan += "* 20:00 | **YV** | 🖋️ **#REVIEW:** [ТРЕК] (ОПЦИЯ). - ⬜ [ОЖИДАНИЕ]\n"
        if weekday == 4 and "POLL" not in "".join(yv_content): # Fri
             plan += "* 16:00 | **YV** | 🗳️ **#HYPEMETER_POLL:** ОПРОС. - ⬜ [ОЖИДАНИЕ]\n"

    file_path = os.path.join(PLAN_DIR, f"daily_plan_{day_short}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(plan)
        
    return f"✅ Plan generated for {date_str}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_plan(sys.argv[1]))
    else:
        print("Usage: python3 plan_generator.py DD.MM.YYYY")