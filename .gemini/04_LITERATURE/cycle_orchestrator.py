#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMNIVERSE CYCLE ORCHESTRATOR (STRICT MODE)
Скрипт для жесткой валидации круга. Блокирует коммит, если правила нарушены.
ВВЕДЕНО ПРАВИЛО: "КАЖДЫЙ СЮЖЕТНЫЙ ПОСТ (001, 002, 003) = МИНИМУМ 9 МИНУТ ЧТЕНИЯ (9000 СИМВОЛОВ)".
СИНХРОННЫЙ ЗАПУСК: Все проекты (Arcana, Zodiac, Incubator) должны развиваться одновременно.
"""

import sys
import os
import glob
from pathlib import Path

MIN_CHAR_COUNT = 9000

def enforce_rules(filepath, text):
    errors = []
    # 1. Запрет на длинные и средние тире
    if "—" in text:
        errors.append("ОШИБКА: Обнаружено длинное тире (—)!")
    if "–" in text:
        errors.append("ОШИБКА: Обнаружено среднее тире (–)!")
    
    # 2. Проверка No-AI
    import re
    forbidden_words = ["серверная", "квантовый", "баг системы", r"\bии\b", "искусственный интеллект", "компьютер", "симуляция"]
    for word in forbidden_words:
        if word.startswith(r"\b"):
            if re.search(word, text, re.IGNORECASE):
                errors.append(f"ОШИБКА: Нарушение жанровой чистоты (Sci-Fi слово 'ИИ')")
        else:
            if word.lower() in text.lower():
                errors.append(f"ОШИБКА: Нарушение жанровой чистоты (Sci-Fi слово '{word}')")
            
    return errors

def validate_arcana_length(filepath, text):
    errors = []
    # Считаем только текст, исключая технический заголовок
    content_lines = [line for line in text.split('\n') if not line.startswith('//')]
    content = '\n'.join(content_lines)
    
    char_count = len(content.strip())
    if char_count < MIN_CHAR_COUNT:
        errors.append(f"КРИТИЧЕСКАЯ ОШИБКА: Пост слишком короткий! Всего {char_count} символов. Должно быть МИНИМУМ {MIN_CHAR_COUNT} символов (Правило 9 минут).")
    return errors

def validate_cycle(date_dir_path):
    print(f"=== ЗАПУСК ВАЛИДАЦИИ КРУГА: {date_dir_path} ===")
    
    target_dir = Path(date_dir_path)
    if not target_dir.exists():
        print(f"ОШИБКА: Директория {target_dir} не найдена.")
        sys.exit(1)
        
    posts = list(target_dir.glob("*.md"))
    if len(posts) < 5:
        print(f"ОШИБКА: Не хватает постов! Найдено {len(posts)}, нужно 5.")
        sys.exit(1)
        
    has_errors = False
    
    for post in sorted(posts):
        with open(post, 'r', encoding='utf-8') as f:
            text = f.read()
            
        print(f"\nПроверка файла: {post.name}")
        errors = enforce_rules(post, text)
        
        # Строгая проверка длины только для сюжетных постов 001, 002, 003
        if "001.md" in post.name or "002.md" in post.name or "003.md" in post.name:
            length_errors = validate_arcana_length(post, text)
            errors.extend(length_errors)
            
        if errors:
            for err in errors:
                print(err)
            has_errors = True
        else:
            print("OK.")
            
    if has_errors:
        print("\n[ВАЛИДАЦИЯ ПРОВАЛЕНА] Круг отменен. Исправьте ошибки.")
        sys.exit(1)
    else:
        print("\n[ВАЛИДАЦИЯ УСПЕШНА] Все правила соблюдены (Сюжетные посты > 9000 символов, без ИИ и тире).")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python cycle_orchestrator.py [путь_к_папке_дня]")
        print("Пример: python cycle_orchestrator.py /home/levdanskiy/GEMINI_PROJECT/04_LITERATURE/01_ARCANA/04_CONTENT/2026/07/01")
        sys.exit(1)
        
    validate_cycle(sys.argv[1])
