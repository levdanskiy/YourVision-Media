import os
import re

BASE_DIR = "/home/levdanskiy/.gemini/TIMELINE/daily_workflow"

# New YV Structure Templates
YV_TUESDAY = """### 📺 YOURVISION (Broadcaster)
* 19:15 | **YV** | 📊 **#CHART_RESULTS:** [ТЕКУЩИЙ ЧАРТ] (ИТОГИ). - ⬜ [ОЖИДАНИЕ]
* 20:30 | **YV** | 📈 **#CHART_ANNOUNCE:** [НОВЫЙ ЧАРТ] (АНОНС). - ⬜ [ОЖИДАНИЕ]"""

YV_THURSDAY = """### 📺 YOURVISION (Broadcaster)
* 18:00 | **YV** | 🗳️ **#CHART_UPDATE:** НАПОМИНАНИЕ (MID-WEEK). - ⬜ [ОЖИДАНИЕ]
* 20:00 | **YV** | 🖋️ **#REVIEW:** [НАЗВАНИЕ ТРЕКА] (РЕЦЕНЗИЯ). - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)"""

YV_FRIDAY = """### 📺 YOURVISION (Broadcaster)
* 16:00 | **YV** | 🗳️ **#HYPEMETER_POLL:** ОПРОС ПЕРЕД ВЫХОДНЫМИ. - ⬜ [ОЖИДАНИЕ]
* 20:00 | **YV** | 🗣️ **#EXPERT_OPINION:** МНЕНИЯ ЭКСПЕРТОВ. - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)"""

YV_SUNDAY = """### 📺 YOURVISION (Broadcaster)
* 19:00 | **YV** | 📊 **#CHART_UPDATE:** ФИНАЛЬНЫЙ ОТСЧЕТ (FINAL CALL). - ⬜ [ОЖИДАНИЕ]"""

YV_DEFAULT = """### 📺 YOURVISION (Broadcaster)
* 18:00 | **YV** | 🖋️ **#REVIEW:** [НАЗВАНИЕ ТРЕКА] (РЕЦЕНЗИЯ). - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)
* 20:00 | **YV** | 🗣️ **#EXPERT_OPINION:** МНЕНИЯ ЭКСПЕРТОВ. - ⬜ [ОЖИДАНИЕ] (ОПЦИЯ)"""

def clean_plan(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath): return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by Almanac sections to preserve them
    parts = re.split(r"(### 📺 YOURVISION.*)", content, flags=re.DOTALL)
    
    if len(parts) < 2: return # No YV section found

    almanac_part = parts[0]
    
    # Determine day of week/date logic
    if "04.02" in filename: yv_block = YV_DEFAULT # Wed
    elif "05.02" in filename: yv_block = YV_THURSDAY # Thu
    elif "06.02" in filename: yv_block = YV_FRIDAY # Fri
    elif "07.02" in filename: yv_block = YV_DEFAULT # Sat
    elif "08.02" in filename: yv_block = YV_SUNDAY # Sun
    elif "09.02" in filename: yv_block = YV_DEFAULT # Mon
    else: return

    new_content = almanac_part + yv_block
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filename}")

files_to_clean = [
    "daily_plan_04.02.md", "daily_plan_05.02.md", "daily_plan_06.02.md",
    "daily_plan_07.02.md", "daily_plan_08.02.md", "daily_plan_09.02.md"
]

for f in files_to_clean:
    clean_plan(f)
