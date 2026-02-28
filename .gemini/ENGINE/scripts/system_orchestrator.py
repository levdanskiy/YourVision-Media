#!/usr/bin/env python3
import subprocess
import os

SCRIPTS_DIR = "/home/levdanskiy/.gemini/ENGINE/scripts"

def run_sync():
    print("🚀 Running Global Data Sync...")
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "market_pulse.py")])
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "nasa_rss.py")])
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "esc_crawler.py")])
    print("✅ Sync Complete.\n")

def update_state():
    print("📊 Updating System State...")
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "knowledge_hub.py")])
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "sync_status.py")])
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "update_state.py")])
    print("✅ State Updated.\n")

def fix_all_punctuation():
    print("✍️ Enforcing Punctuation Rules...")
    # Запускаем bash скрипт для всей папки CONTENT и TIMELINE
    subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "fix_punctuation.sh"), "/home/levdanskiy/.gemini/CONTENT"])
    subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "fix_punctuation.sh"), "/home/levdanskiy/.gemini/TIMELINE"])
    print("✅ Punctuation Enforced.\n")

if __name__ == "__main__":
    run_sync()
    update_state()
    fix_all_punctuation()
    print("--- 🛠️ SYSTEM MAINTENANCE COMPLETE ---")
