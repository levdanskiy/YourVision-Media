import sys
import os
import re

LIMITS = {
    'Q': (100, 300),   # QUOTE
    'S': (301, 500),   # SNAP
    'F': (501, 700),   # FLASH
    'B': (701, 1000),  # BRIEF
    'N': (1001, 1300), # NOTE
    'C': (1301, 1800), # COLUMN
    'A': (1801, 2400), # ARTICLE
    'R': (2401, 3000), # REPORT
    'E': (3001, 4000), # ESSAY
    'M': (4001, 6000)  # MONOGRAPH
}

def publish(file_path):
    if not os.path.exists(file_path): return "ERROR: File not found."
    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()

    # 1. Санитайзинг
    content = content.replace("—", "-").replace("–", "-")
    
    # 2. Метаданные из поста (УЛЬТРА-ГИБКИЙ ПОИСК)
    time_match = re.search(r"Время:?\s*(\d{2}:\d{2})", content)
    date_match = re.search(r"Дата:?\s*(\d{2}\.\d{2}\.\d{4})", content)
    channel_match = re.search(r"Канал:?\s*(AC|NB|SW|YV)", content)
    grade_match = re.search(r"Grade:?\s*([QSFBNCAREM]{1,2})", content)
    
    if not all([time_match, date_match, channel_match, grade_match]):
        return f"ERROR: Missing Metadata. Time={bool(time_match)}, Date={bool(date_match)}, Channel={bool(channel_match)}, Grade={bool(grade_match)}"

    post_time = time_match.group(1)
    post_date_full = date_match.group(1)
    post_date_short = post_date_full[:5] # DD.MM
    channel = channel_match.group(1)
    grade = grade_match.group(1)

    # 3. Объем
    try:
        parts = content.split('СТАТУС: ГОТОВ')
        useful_content = parts[1].split('PROMPT:')[0]
        count = len(useful_content.strip())
    except:
        count = len(content.split('PROMPT:')[0].strip())

    low, high = LIMITS.get(grade, (0, 9999))
    if count < low or count > high:
        return f"REJECTED: Grade {grade} violation ({count} chars). Range: {low}-{high}"

    # 4. Сохранение
    with open(file_path, 'w', encoding='utf-8') as f: f.write(content)

    # 5. СИНХРОНИЗАЦИЯ ПЛАНОВ
    sync_report = []
    timeline_dir = ".gemini/TIMELINE"
    
    for root, dirs, files in os.walk(timeline_dir):
        for file in files:
            if file.endswith(".md"):
                p = os.path.join(root, file)
                with open(p, 'r', encoding='utf-8') as f: lines = f.readlines()
                
                new_lines = []
                modified = False
                for l in lines:
                    if post_time in l and channel in l:
                        line_date_match = re.search(r"(\d{2}\.\d{2})", l)
                        date_ok = True
                        if line_date_match:
                            if line_date_match.group(1) != post_date_short:
                                date_ok = False
                        
                        if "master_plans" in p and f"### {post_date_short}" not in "".join(lines):
                            date_ok = False

                        if date_ok and any(x in l for x in ["⬜", "🔴"]):
                            l = re.sub(r"[- ]*[🔴⬜]\s*\[(ДОЛГ|ОЖИДАНИЕ)\]", " - ✅ [ГОТОВО]", l)
                            modified = True
                    new_lines.append(l)
                
                if modified:
                    with open(p, 'w', encoding='utf-8') as f: f.writelines(new_lines)
                    sync_report.append(os.path.basename(p))

    return f"SUCCESS: Published. Sync: {', '.join(sync_report)} | {count} chars (Net)."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(publish(sys.argv[1]))
