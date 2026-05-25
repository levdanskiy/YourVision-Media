#!/usr/bin/env python3
import os
import sys
import glob
import re
from datetime import datetime, timedelta

# Конфигурация
BASE_DIR = "/home/levdanskiy/.gemini"
POSTS_DIR = os.path.join(BASE_DIR, "posts")

def get_post_language(file_path):
    """Определяет язык поста по содержимому."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Удаляем метаданные и промпты
            clean_content = re.sub(r'^//.*', '', content, flags=re.MULTILINE)
            clean_content = clean_content.split('**PROMPT:**')[0]
            
            if re.search(r'[ыэъ]', clean_content, re.IGNORECASE):
                return "RU"
            elif re.search(r'[іїєґ]', clean_content, re.IGNORECASE):
                return "UA"
            else:
                # Если явных маркеров нет, ищем кириллицу
                if re.search(r'[а-яА-Я]', clean_content):
                    # Эвристика: если нет специфических букв, считаем RU (дефолт) или пробуем найти 'и' (есть в обоих, но в UA чаще 'і')
                    # Для простоты: если нет UA-маркеров, но есть кириллица -> RU
                    return "RU"
                return "UNKNOWN"
    except Exception as e:
        return "UNKNOWN"

def find_last_post(channel_code, target_date_obj):
    """Находит последний пост канала до указанной даты."""
    # Идем назад по дням (максимум 30 дней)
    current_date = target_date_obj
    
    for _ in range(30):
        current_date -= timedelta(days=1)
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")
        
        path = os.path.join(POSTS_DIR, year, month, day)
        if not os.path.exists(path):
            continue
            
        # Ищем файлы канала
        pattern = os.path.join(path, f"{channel_code}-*.md")
        files = glob.glob(pattern)
        
        if files:
            # Сортируем по времени (имя файла содержит HH-MM)
            files.sort()
            return files[-1] # Возвращаем самый последний файл дня
            
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 predict_language.py [CHANNEL_CODE] [DD.MM.YYYY]")
        sys.exit(1)
        
    channel = sys.argv[1]
    date_str = sys.argv[2]
    
    try:
        target_date = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print("❌ Invalid date format.")
        sys.exit(1)
        
    last_post = find_last_post(channel, target_date)
    
    if last_post:
        lang = get_post_language(last_post)
        print(f"🔍 Last post found: {os.path.basename(last_post)}")
        print(f"🌍 Last language: {lang}")
        
        if lang == "RU":
            print(f"🚀 RECOMMENDED: UA")
        elif lang == "UA":
            print(f"🚀 RECOMMENDED: RU")
        else:
            print(f"⚠️ Unknown last language. Defaulting to RU.")
    else:
        print("⚠️ No previous posts found. Defaulting to RU.")

if __name__ == "__main__":
    main()
