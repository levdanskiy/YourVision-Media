#!/usr/bin/env python3
import os
import re
import sys

def check_style(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 1. Проверка Telegram-разделителей
    if "━━━━━━━━━━━━" not in content and "---" not in content and "~ ~ ~" not in content:
        issues.append("STYLE: Отсутствуют канонические разделители.")
    
    # 2. Проверка моноширинных акцентов
    if not re.search(r'`.*?`', content):
        issues.append("STYLE: Мало моноширинных акцентов (бэктиков).")
    
    # 3. Проверка физики в промпте
    prompt_match = re.search(r'PROMPT:(.*)', content, re.DOTALL | re.IGNORECASE)
    if prompt_match:
        p = prompt_match.group(1).lower()
        quality_tokens = ["refraction", "diffraction", "volumetric", "chromatic", "subsurface", "texture"]
        found_tokens = [t for t in quality_tokens if t in p]
        if len(found_tokens) < 2:
            issues.append(f"PROMPT: Слишком простой промпт. Добавьте физики (найдено: {found_tokens}).")

    if issues:
        for iss in issues: print(f"⚠️ {iss}")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    if check_style(sys.argv[1]):
        print("✅ STYLE CHECK PASSED")
        sys.exit(0)
    else:
        sys.exit(1)
