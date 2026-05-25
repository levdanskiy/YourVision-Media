#!/usr/bin/env python3
import sys
import os
import subprocess

# ПУТИ
BASE = "/home/levdanskiy/.gemini/"
SCRIPTS = BASE + "ENGINE/scripts/"

def run_script(name, *args):
    cmd = ["python3", SCRIPTS + name] + list(args)
    print(f"⚙️ EXEC: {name}...")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.stdout: print(res.stdout.strip())
        if res.stderr: print(f"⚠️ LOG: {res.stderr.strip()}")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

def execute_pipeline(channel, time_slot, topic):
    print(f"🚀 MISSION START: {channel} | {time_slot} | {topic}")

    # 1. СИНХРОНИЗАЦИЯ С РЕАЛЬНОСТЬЮ
    run_script("pulse.py")
    run_script("global_sync.py")
    
    # 2. СБОР СПЕЦИФИЧЕСКИХ ДАННЫХ
    if channel == "AC":
        run_script("moon_helper.py")
        run_script("market_pulse.py") # Золото для алхимии
        run_script("nasa_rss.py") # Космос для масштаба
    
    if channel == "YV":
        run_script("market_pulse.py") # Индикаторы рынка
        run_script("trend_scout.py", topic.split(":")[0]) # Хайп по теме
    
    # 3. ПОДГОТОВКА СТРУКТУРЫ
    # Здесь мы пока просто выводим данные, в будущем передадим в LLM
    print("\n✅ DATA COLLECTED. READY TO GENERATE.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 execute_task.py CHANNEL TIME TOPIC")
    else:
        execute_pipeline(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
