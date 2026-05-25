#!/usr/bin/env python3
import json
import random
import sys

def get_daily_mood(date_str):
    path = "/home/levdanskiy/.gemini/CORE/knowledge/mood_palettes.json"
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Логика: привязка палитры к дате (чтобы в течение дня она была одна)
    # Используем сумму чисел даты как сид
    random.seed(sum(map(int, date_str.split('.'))))
    palette_key = random.choice(list(data['palettes'].keys()))
    return data['palettes'][palette_key]

if __name__ == "__main__":
    date_val = sys.argv[1] if len(sys.argv) > 1 else "30.01.2026"
    print(get_daily_mood(date_val))
