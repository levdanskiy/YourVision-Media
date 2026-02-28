#!/usr/bin/env python3
import os
import re
from datetime import datetime, timedelta

BASE_DIR = "/home/levdanskiy/.gemini"
WORK_DIR = os.path.join(BASE_DIR, "TIMELINE/master_plans")

def check_holidays():
    today = datetime.now()
    lookahead = 7
    
    current_month_code = today.strftime("%m") # '01', '02', etc.
    month_path = os.path.join(WORK_DIR, current_month_code)
    
    if not os.path.exists(month_path):
        print(f"⚠️ Папка плана на месяц {current_month_code} не найдена.")
        return

    print(f"📅 АНАЛИЗ ГРЯДУЩИХ СОБЫТИЙ (на {lookahead} дней):")
    
    # Собираем контент изо всех планов в этой папке
    full_content = ""
    for f_name in os.listdir(month_path):
        if f_name.endswith(".md"):
            with open(os.path.join(month_path, f_name), 'r', encoding='utf-8') as f:
                full_content += f.read() + "\n"
        
    # Ищем даты в формате DD.MM
    found_any = False
    for i in range(lookahead + 1):
        target_date = today + timedelta(days=i)
        date_str = target_date.strftime("%d.%m")
        
        # Ищем строки с этой датой. Ищем во всем контенте.
        # Формат обычно: **DD.MM (День недели)**
        matches = re.findall(fr'\*\*({date_str}.*?)\*\*', full_content)
        for m in set(matches): # Используем set для уникальности
            found_any = True
            days_left = i
            status = "СЕГОДНЯ" if i == 0 else f"через {i} дн."
            priority = "🔥 [МАЯК]" if "[МАЯК]" in m else "📌 [КОНСТАНТА]" if "[КОНСТАНТА]" in m else "☁️ [ДОПОЛНЕНИЕ]"
            print(f"  {status} | {priority} | {m}")
    
    if not found_any:
        print("  Событий в мастер-планах на ближайшую неделю не обнаружено.")

if __name__ == "__main__":
    check_holidays()
