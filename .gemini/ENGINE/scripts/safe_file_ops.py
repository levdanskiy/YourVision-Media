import json
import os
import sys

REGISTRY_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/THEME_REGISTRY.json"

def verify_content_integrity(channel, new_content):
    if not os.path.exists(REGISTRY_PATH):
        return True # Если реестра нет, доверяем (первый запуск)
        
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    if channel not in registry:
        return True
        
    # Проверяем, что КАЖДАЯ тема из реестра присутствует в новом контенте
    missing_themes = []
    for entry in registry[channel]:
        if entry["topic"] not in new_content:
            missing_themes.append(f"{entry['time']} - {entry['topic']}")
            
    if missing_themes:
        print(f"❌ CRITICAL ERROR: Data loss detected for channel {channel}!")
        print(f"Missing themes: {', '.join(missing_themes[:3])}...")
        return False
        
    return True

def safe_save_plan(file_path, content):
    channel = os.path.basename(file_path).split("_")[0]
    
    if verify_content_integrity(channel, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ SAFE SAVE SUCCESSFUL: {file_path}")
        return True
    else:
        print(f"🛑 SAVE BLOCKED to prevent data loss in {file_path}")
        return False

if __name__ == "__main__":
    # Логика для системных вызовов
    pass