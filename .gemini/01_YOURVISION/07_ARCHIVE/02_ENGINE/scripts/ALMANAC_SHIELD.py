#!/usr/bin/env python3
import sys
import re
import os
import json

def validate_post(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError: return False, "File not found."

    fn = os.path.basename(file_path).upper()
    channel_id = fn[:2].lower()
    
    # 1. Проверка Ротации AR (Глубина 5) - V11.3
    with open(".gemini/system/config/SYSTEM_STATE.json", 'r') as f:
        state = json.load(f)
    
    ar_match = re.search(r'--ar (\d+\.?\d*:\d+\.?\d*)', content)
    current_ar = ar_match.group(1) if ar_match else "None"
    history = state["channels"].get(channel_id, {}).get("ar_history", [])
    
    if current_ar in history and "YV" not in fn:
        return False, f"AR REPEAT ERROR: Формат {current_ar} уже был в последних 5 постах. История: {', '.join(history)}"

    # 2. Проверка Persona Check
    if channel_id != "sw" and "YV" not in fn:
        if not any(t in content.upper() for t in ["MODEL", "MAN", "WOMAN", "PERSON"]):
            return False, "PROMPT ERROR: Нет модели."

    return True, f"SUCCESS: AR ({current_ar}) Unique in sequence."

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    ok, msg = validate_post(sys.argv[1])
    print(f"✅ {msg}" if ok else f"❌ {msg}")
    sys.exit(0 if ok else 1)