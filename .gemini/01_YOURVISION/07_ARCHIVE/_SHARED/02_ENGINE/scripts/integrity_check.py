#!/usr/bin/env python3
import os
import re

POSTS_DIR = "/home/levdanskiy/.gemini/CONTENT/posts/"
PLAN_DIR = "/home/levdanskiy/.gemini/TIMELINE/daily_workflow/"

def sync_plan_with_files(plan_file):
    if not os.path.exists(plan_file): return
    
    # Извлекаем дату из имени файла daily_plan_DD.MM.md
    date_match = re.search(r'daily_plan_(\d{2})\.(\d{2})\.md', plan_file)
    if not date_match: return
    day, month = date_match.groups()
    year = "2026"
    
    # Путь к папке с постами именно на эту дату
    target_date_dir = os.path.join(POSTS_DIR, year, month, day)
    
    with open(plan_file, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        match = re.search(r'(\d{2}:\d{2}) \| \*\*(\w+)\*\* \|.*?#(\w+)', line)
        if match:
            time_str, channel, rubric = match.groups()
            time_tag = time_str.replace(':', '-')
            
            # Проверяем наличие файла ТОЛЬКО в папке этой даты
            found = False
            if os.path.exists(target_date_dir):
                for f_name in os.listdir(target_date_dir):
                    if channel.upper() in f_name and time_tag in f_name:
                        found = True
                        break
            
            if found:
                line = line.replace("⬜ [ОЖИДАНИЕ]", "✅ [ГОТОВО]")
            else:
                line = line.replace("✅ [ГОТОВО]", "⬜ [ОЖИДАНИЕ]")
        
        new_lines.append(line)
    
    with open(plan_file, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sync_plan_with_files(sys.argv[1])
    else:
        for p in os.listdir(PLAN_DIR):
            if p.startswith("daily_plan_") and p.endswith(".md"):
                sync_plan_with_files(os.path.join(PLAN_DIR, p))
    print("💎 INTEGRITY CHECK V2: Date-aware synchronization complete.")