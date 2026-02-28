#!/usr/bin/env python3
import os
import re
import sys

def check_ux(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fn = os.path.basename(file_path).upper()
    errors = []

    # 1. Запрет на декоративные символы (V9.2)
    forbidden_decor = ["⋆", "⋅", "☆", "✧", "✨", "〰️", "═", "─", "▬", "• • •"]
    for char in forbidden_decor:
        if char in content.replace("---", ""):
            errors.append(f"UX ERROR: Запрещен декоративный символ '{char}'.")

    # 2. YourVision: Контекстная аналитика (V10.1)
    if "YV-" in fn:
        is_deep = any(tag in content for tag in ["#ANALYSIS", "#STAGE_DIVING"])
        is_news = any(tag in content for tag in ["#NEWS", "#LIVE_NEWS", "#ESC_RELEASES"])
        
        if is_deep and not re.search(r'\[[■□]+\]', content):
            errors.append("UX ERROR (YV): В аналитике ОБЯЗАТЕЛЕН статус-бар.")
        
        if is_news and re.search(r'\[[■□]+\]', content):
            errors.append("UX ERROR (YV): В новостях ЗАПРЕЩЕН статус-бар (используйте чистый текст).")

    # 3. Общие проверки (AC/NB)
    if "AC-" in fn and "||" not in content:
        errors.append("UX (AC): Нет спойлера.")
    if "NB-" in fn and "📍" not in content:
        errors.append("UX (NB): Нет гео-тега.")

    if errors:
        for err in errors: print(f"❌ {err}")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    if check_ux(sys.argv[1]):
        print("✅ ALMANAC UX GUARD: PASSED (V10.1 Contextual)")
        sys.exit(0)
    else:
        sys.exit(1)
