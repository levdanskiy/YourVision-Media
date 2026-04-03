import os
import re

BASE_DIR = "/home/levdanskiy/.gemini/TIMELINE/master_plans/02"
STATUS_PENDING = "⬜ [ОЖИДАНИЕ]"
STATUS_DONE = "✅ [ГОТОВО]"

# Current date for reference
CURRENT_DAY = 4
CURRENT_MONTH = 2

def reset_master_plan(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath): return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    current_date_in_file = None
    
    for line in lines:
        # Detect date header ### DD.MM
        date_match = re.search(r"### (\d{2})\.(\d{2})", line)
        if date_match:
            d = int(date_match.group(1))
            m = int(date_match.group(2))
            current_date_in_file = (d, m)
        
        # If the date in the file is >= CURRENT_DAY (and same month), reset to WAITING
        if STATUS_DONE in line and current_date_in_file:
            if current_date_in_file[1] > CURRENT_MONTH or (current_date_in_file[1] == CURRENT_MONTH and current_date_in_file[0] >= CURRENT_DAY):
                line = line.replace(STATUS_DONE, STATUS_PENDING)
        
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Reset {filename} for dates >= {CURRENT_DAY}.{CURRENT_MONTH}")

for f in os.listdir(BASE_DIR):
    if f.endswith(".md"):
        reset_master_plan(f)
