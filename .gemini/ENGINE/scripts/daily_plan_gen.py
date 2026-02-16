import sys
import os
import re
from datetime import datetime, timedelta

def get_day_plan(date_str, channel):
    path = f".gemini/TIMELINE/master_plans/02/{channel}_Plan_02.md"
    if not os.path.exists(path): return []
    with open(path, 'r') as f: content = f.read()
    day_short = date_str[:5] 
    pattern = rf"### {day_short}.*?\n(.*?)(?=\n###|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = match.group(1).strip().split('\n')
        return [l for l in lines if l.strip()]
    return []

def get_debts(current_date_str):
    # Вычисляем вчерашнюю дату
    try:
        curr_date = datetime.strptime(current_date_str, "%d.%m.%Y")
        prev_date = curr_date - timedelta(days=1)
        prev_str = prev_date.strftime("%d.%m") # формат 15.02
        
        # Ищем файл вчерашнего плана
        wf_dir = ".gemini/TIMELINE/daily_workflow"
        prev_file = None
        for f in os.listdir(wf_dir):
            if f.startswith(f"daily_plan_{prev_str}"):
                prev_file = os.path.join(wf_dir, f)
                break
        
        if not prev_file or not os.path.exists(prev_file):
            return []

        with open(prev_file, 'r') as f:
            lines = f.readlines()
        
        debts = []
        for line in lines:
            # Если в строке есть ⬜ [ОЖИДАНИЕ] или 🔴 [ДОЛГ], значит задача не выполнена
            if "⬜" in line or "🔴" in line:
                # Очищаем строку от старых статусов, чтобы не дублировать
                clean_line = line.strip().replace("⬜ [ОЖИДАНИЕ]", "").replace("🔴 [ДОЛГ]", "").strip()
                if clean_line.startswith("*") or re.match(r"^\d+\.", clean_line):
                    # Убираем лишние тире в конце перед добавлением нового статуса
                    clean_line = re.sub(r"\s*-\s*$", "", clean_line)
                    debts.append(clean_line + " -  🔴 [ДОЛГ]")
        return debts

    except Exception as e:
        print(f"Debt calculation error: {e}")
        return []

def generate(date_str):
    header = f"# 📅 DAILY PLAN: {date_str}\n**// STATUS: GENERATED | AUTO-SYNC ENABLED //**\n\n"
    
    # 1. Сбор Долгов
    debts = get_debts(date_str)
    
    # 2. Сборка секций из Мастер-планов
    ac_lines = get_day_plan(date_str, "AC")
    nb_lines = get_day_plan(date_str, "NB")
    sw_lines = get_day_plan(date_str, "SW")
    yv_lines = get_day_plan(date_str, "YV")

    content = header
    
    if debts:
        content += "### 🔴 DEBTS / ДОЛГИ (С прошлого дня)\n" + "\n".join(debts) + "\n\n"
        content += "---\n\n"

    content += "### 🗝️ ARCHITECT (Main)\n" + "\n".join(ac_lines) + "\n\n"
    content += "### 🕊️ NEIGHBORS (Soul)\n" + "\n".join(nb_lines) + "\n\n"
    content += "### 🍒 SWEET (Taste)\n" + "\n".join(sw_lines) + "\n\n"
    content += "### 📺 YOURVISION (Broadcaster)\n" + "\n".join(yv_lines) + "\n"
    
    filename = f".gemini/TIMELINE/daily_workflow/daily_plan_{date_str[:5]}.md"
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Plan generated: {filename}")
    if debts:
        print(f"ALERT: {len(debts)} debts transferred!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 daily_plan_gen.py DD.MM.YYYY")
    else:
        generate(sys.argv[1])