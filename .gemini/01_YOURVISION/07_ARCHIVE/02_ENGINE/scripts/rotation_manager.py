import sqlite3
import random
import re
import os

DB_PATH = '/home/levdanskiy/.gemini/TIMELINE/database/content_plan.db'
PROTOCOL_PATH = '/home/levdanskiy/.gemini/KNOWLEDGE/Visual_Protocol.md'

def get_last_post(channel):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rubric, gender, file_path FROM posts WHERE channel=? ORDER BY id DESC LIMIT 1", (channel,))
    res = cursor.fetchone()
    conn.close()
    return res

def get_ar_list(channel):
    with open(PROTOCOL_PATH, 'r') as f:
        content = f.read()
    # Извлекаем список AR для конкретного канала
    section = re.search(f"## {channel}.*?\n(.*?)\n##", content + "\n##", re.DOTALL)
    if not section: return ["1:1"]
    ar_list = re.findall(r"--ar (\d+:?\d*\.?\d*)", section.group(1))
    return ar_list

def suggest_next(channel):
    last = get_last_post(channel)
    ar_options = get_ar_list(channel)
    
    # 1. Чередование пола (для AC/NB)
    next_gender = "MALE"
    if last and last[1] == "MALE":
        next_gender = "FEMALE"
    
    # 2. Выбор уникального AR
    # В будущем можно добавить чтение AR из файлов, сейчас просто исключаем 16:9 для теста
    next_ar = random.choice(ar_options[:5]) # Берем из топ-5 трендовых
    
    print(f"--- ROTATION SPEC FOR {channel} ---")
    print(f"NEXT GENDER: {next_gender}")
    print(f"NEXT AR: --ar {next_ar}")
    print(f"FORBIDDEN RUBRIC (Recent): {last[0] if last else 'None'}")
    print(f"VIBE: Imperfect by Design / Organic Realism")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        suggest_next(sys.argv[1])
