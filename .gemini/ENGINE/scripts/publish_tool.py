import sys
import os
import re

# YOURVISION 2.0 TIER-1 LIMITS
LIMITS = {
    'Q': (100, 300),    # QUOTE
    'S': (301, 500),    # SNAP
    'F': (501, 1000),   # FLASH / NEWS WIRE (Expanded)
    'B': (701, 1300),   # BRIEF (Expanded)
    'N': (1001, 1500),  # NOTE / VISUAL EXP
    'C': (1301, 2000),  # COLUMN / DATA & CHARTS
    'A': (1801, 3500),  # ANALYTICS / DEEP DIVE (Expanded for Longreads)
    'R': (2401, 4000),  # REPORT / INVESTIGATION
    'E': (3001, 5000),  # ESSAY
    'M': (4001, 8000)   # MONOGRAPH
}

def publish(file_path):
    if not os.path.exists(file_path): return "ERROR: File not found."
    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()

    # 1. Санитайзинг (Типографика)
    content = content.replace("—", "-").replace("–", "-")
    
    # 2. Метаданные из поста
    time_match = re.search(r"Время:?\s*(\d{2}:\d{2})", content)
    date_match = re.search(r"Дата:?\s*(\d{2}\.\d{2}\.\d{4})", content)
    channel_match = re.search(r"Канал:?\s*(AC|NB|SW|YV)", content)
    grade_match = re.search(r"Grade:?\s*([QSFBNCAREM]{1,2})", content)
    
    if not all([time_match, date_match, channel_match, grade_match]):
        # Fallback для старых форматов
        return f"ERROR: Missing Metadata. Time={bool(time_match)}, Date={bool(date_match)}, Channel={bool(channel_match)}, Grade={bool(grade_match)}"

    post_time = time_match.group(1)
    post_date_full = date_match.group(1)
    post_date_short = post_date_full[:5] # DD.MM
    channel = channel_match.group(1)
    grade = grade_match.group(1)

    # 3. Объем (Умный подсчет)
    # Считаем только текст между заголовком и промптом/системной инфой
    try:
        # Ищем начало текста (после статуса или заголовка)
        start_marker = "СТАТУС: ГОТОВ"
        end_marker_1 = "**PROMPT:**"
        end_marker_2 = "---"
        
        if start_marker in content:
            body = content.split(start_marker)[1]
        else:
            body = content # Fallback

        # Обрезаем хвосты
        if end_marker_1 in body:
            body = body.split(end_marker_1)[0]
        elif end_marker_2 in body: # Если промпта нет, ищем разделитель
             body = body.split(end_marker_2)[0]
        
        count = len(body.strip())
    except Exception as e:
        return f"ERROR: Content parsing failed. {str(e)}"

    low, high = LIMITS.get(grade, (0, 9999))
    
    # Soft Validation (Предупреждение вместо блока для пограничных значений)
    validation_msg = ""
    if count < low:
        # Allow 10% deviation downwards
        if count >= low * 0.9:
            validation_msg = f"WARNING: Grade {grade} low ({count}/{low}). Allowed."
        else:
            return f"REJECTED: Grade {grade} underflow ({count} chars). Min: {low}"
    elif count > high:
        # Allow 10% deviation upwards
        if count <= high * 1.1:
             validation_msg = f"WARNING: Grade {grade} high ({count}/{high}). Allowed."
        else:
            return f"REJECTED: Grade {grade} overflow ({count} chars). Max: {high}"

    # 4. Сохранение (Перезапись с исправленной типографикой)
    with open(file_path, 'w', encoding='utf-8') as f: f.write(content)

    # 5. СИНХРОНИЗАЦИЯ ПЛАНОВ (Recursive Global Sync)
    sync_report = []
    timeline_dir = ".gemini/TIMELINE"
    
    # Стратегия: Ищем совпадение Time + Channel в любом файле плана
    # Игнорируем дату, если это мастер-план (там даты в заголовках)
    
    for root, dirs, files in os.walk(timeline_dir):
        for file in files:
            if file.endswith(".md"):
                p = os.path.join(root, file)
                with open(p, 'r', encoding='utf-8') as f: lines = f.readlines()
                
                new_lines = []
                modified = False
                current_section_date = None
                
                for l in lines:
                    # Попытка определить дату секции в мастер-плане
                    section_match = re.search(r"### (\d{2}\.\d{2})", l)
                    if section_match:
                        current_section_date = section_match.group(1)

                    # Логика совпадения
                    if post_time in l and f"**{channel}**" in l:
                        is_target = False
                        
                        # 1. Это дневной план и дата в имени файла совпадает
                        if f"daily_plan_{post_date_short}.md" in file:
                            is_target = True
                        
                        # 2. Это мастер-план и мы внутри правильной секции
                        elif "master_plans" in p and current_section_date == post_date_short:
                            is_target = True
                            
                        # 3. Это Recovery Plan (без даты) - берем всё
                        elif "recovery" in file:
                            is_target = True

                        if is_target and any(x in l for x in ["⬜", "🔴"]):
                            l = re.sub(r"[- ]*[🔴⬜]\s*\[(ДОЛГ|ОЖИДАНИЕ|FLEX SLOT.*)\]", " - ✅ [ГОТОВО]", l)
                            modified = True
                            
                    new_lines.append(l)
                
                if modified:
                    with open(p, 'w', encoding='utf-8') as f: f.writelines(new_lines)
                    sync_report.append(os.path.basename(p))

    return f"SUCCESS: Published. Sync: {', '.join(sync_report)} | {count} chars (Net). {validation_msg}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(publish(sys.argv[1]))