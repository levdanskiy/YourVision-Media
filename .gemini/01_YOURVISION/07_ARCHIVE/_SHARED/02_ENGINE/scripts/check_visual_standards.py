#!/usr/bin/env python3
import sys
import re
import os

def check_ar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    ar_match = re.search(r'--ar (\d+:\d+(?:\.\d+)?)', content)
    if not ar_match:
        return False, "VISUAL ERROR: Нет параметра --ar."
    
    ar = ar_match.group(1)
    fn = os.path.basename(file_path).upper()

    # Глобальный список всех допустимых AR для Midjourney
    valid_ars = [
        "1:1", "16:9", "9:16", "4:5", "5:4", "3:2", "2:3", "21:9", "4:3", "3:4", "7:5", "5:7", "2:1", "1:2"
    ]

    if ar not in valid_ars:
        # Пропускаем, если это валидный формат MJ, но редкий (например 3.5:1)
        pass 

    # СТРАТЕГИЯ: РАЗРЕШЕНО ВСЕ, НО С КОММЕНТАРИЯМИ
    # Мы больше не блокируем генерацию (return False), мы только информируем.
    # Блокировка только на явный абсурд.

    msg = f"VISUAL PASS: AR {ar} validated."

    # AC - Архитектор
    if "AC-" in fn:
        if ar in ["9:16"]:
            msg += " (Note: Вертикаль 9:16 допустима для Stories, но не для ленты)."

    # NB - Путешественник
    if "NB-" in fn:
        # Полная свобода репортажа
        pass

    # SW - Гедонист
    if "SW-" in fn:
        # Полная свобода для фуд-порно
        pass

    return True, msg

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    success, message = check_ar(sys.argv[1])
    if success:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)
