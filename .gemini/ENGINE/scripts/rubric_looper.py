#!/usr/bin/env python3
import os
import re
import json
import random

CORE_PATH = "/home/levdanskiy/.gemini/"
MASTER_DIR = os.path.join(CORE_PATH, "TIMELINE/master_plans/02/")
POSTS_DIR = os.path.join(CORE_PATH, "CONTENT/posts/")

def get_rubrics_from_master(channel):
    file_map = {"AC": "AC_Plan_02.md", "NB": "NB_Plan_02.md", "SW": "SW_Plan_02.md", "YV": "YV_Plan_02.md"}
    path = os.path.join(MASTER_DIR, file_map.get(channel, ""))
    if not os.path.exists(path): return []
    
    with open(path, 'r') as f:
        text = f.read()
    
    # Извлекаем все рубрики (начинаются с #)
    rubrics = re.findall(r'#([A-Z_]+)', text)
    return list(set(rubrics))

def get_actual_usage(channel):
    usage = {}
    for root, dirs, files in os.walk(POSTS_DIR):
        for f in files:
            if f.startswith(channel):
                # Извлекаем рубрику из имени файла (упрощенно)
                # Или читаем содержимое файла на предмет #RUBRIC
                with open(os.path.join(root, f), 'r') as content:
                    match = re.search(r'#([A-Z_]+)', content.read())
                    if match:
                        r = match.group(1)
                        usage[r] = usage.get(r, 0) + 1
    return usage

def get_balanced_rubric(channel):
    master_rubrics = get_rubrics_from_master(channel)
    actual_usage = get_actual_usage(channel)
    
    # Считаем "вес" каждой рубрики (сколько раз она была пропущена)
    candidates = []
    min_uses = min([actual_usage.get(r, 0) for r in master_rubrics]) if master_rubrics else 0
    
    for r in master_rubrics:
        if actual_usage.get(r, 0) == min_uses:
            candidates.append(r)
            
    return random.choice(candidates) if candidates else "GENERAL"

if __name__ == "__main__":
    import sys
    ch = sys.argv[1] if len(sys.argv) > 1 else "AC"
    print(get_balanced_rubric(ch))
