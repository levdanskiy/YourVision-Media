#!/usr/bin/env python3
import os
import sys
import glob

# Конфигурация
BASE_DIR = "/home/levdanskiy/.gemini"
POSTS_DIR = os.path.join(BASE_DIR, "posts")

def check_slot(date_str, time_str):
    # date_str: 24.01.2026
    # time_str: 10:00
    
    try:
        day, month, year = date_str.split('.')
    except ValueError:
        print(f"❌ ERROR: Неверный формат даты. Используйте DD.MM.YYYY")
        sys.exit(1)

    # Формируем путь: posts/2026/01/24/
    path = os.path.join(POSTS_DIR, year, month, day)
    
    if not os.path.exists(path):
        print(f"✅ SLOT CLEAN: Папка {path} еще не создана. Можно генерировать.")
        sys.exit(0)

    # Ищем файл с указанным временем
    # Формат файла: CODE-DD.MM-HH-MM-Title.md
    time_clean = time_str.replace(':', '-')
    pattern = f"*-{day}.{month}-{time_clean}-*.md"
    search_path = os.path.join(path, pattern)
    
    files = glob.glob(search_path)
    
    if files:
        print(f"⚠️ WARNING: Файл уже существует!")
        for f in files:
            print(f"   📄 {os.path.basename(f)}")
        print("\n⛔ STOP. Не генерируйте пост без прямого приказа 'ПЕРЕПИСАТЬ'.")
        sys.exit(1)
    else:
        print(f"✅ SLOT CLEAN: Файлов на {time_str} нет. Жду промпт.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 check_slot.py [DD.MM.YYYY] [HH:MM]")
        sys.exit(1)
    
    check_slot(sys.argv[1], sys.argv[2])
