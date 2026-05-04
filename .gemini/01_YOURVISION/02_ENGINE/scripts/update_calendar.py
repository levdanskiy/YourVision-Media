#!/usr/bin/env python3
import sys
import os
import re

def update_status(file_path, date_str, time_str, new_status):
    if not os.path.exists(file_path): return False
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем строку с временем и датой (или просто временем в сводном плане)
    # Используем более широкий поиск
    pattern = rf"(`{time_str}.*?`\s*.*?-\s*)⬜"
    if new_status == "✅":
        replacement = r"\1✅"
        new_content = re.sub(pattern, replacement, content)
        
        # Также ищем формат [ОЖИДАНИЕ]
        new_content = new_content.replace("[ОЖИДАНИЕ]", "[ГОТОВО]")
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 5: sys.exit(1)
    # Аргументы: путь, дата, время, статус
    res = update_status(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print(f"{'✅' if res else '❌'} Статус обновлен.")