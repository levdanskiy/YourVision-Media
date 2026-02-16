#!/usr/bin/env python3
import json
import os
import random

ATLAS_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/rubric_atlas.json"
HISTORY_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/rubric_history.json"

def get_next_rubric(channel):
    channel = channel.upper()
    if not os.path.exists(ATLAS_PATH):
        return "#GENERAL"
    
    with open(ATLAS_PATH, 'r') as f:
        atlas = json.load(f)
    
    if channel not in atlas:
        return "#GENERAL"
    
    available_rubrics = atlas[channel]
    
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as f:
            history = json.load(f)
    else:
        history = {c: {} for c in atlas.keys()}

    channel_history = history.get(channel, {})
    
    # Считаем количество использований для каждой рубрики
    usage_counts = {r: channel_history.get(r, 0) for r in available_rubrics}
    
    # Находим минимальное количество использований
    min_usage = min(usage_counts.values())
    
    # Отбираем рубрики с минимальным использованием
    candidates = [r for r, count in usage_counts.items() if count == min_usage]
    
    # Выбираем случайную из кандидатов
    selected = random.choice(candidates)
    
    # Обновляем историю
    channel_history[selected] = channel_history.get(selected, 0) + 1
    history[channel] = channel_history
    
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=4)
    
    return selected

if __name__ == "__main__":
    import sys
    ch = sys.argv[1] if len(sys.argv) > 1 else "AC"
    print(get_next_rubric(ch))