#!/usr/bin/env python3
import sys
import os
import re

def fix_content(file_path):
    if not os.path.exists(file_path):
        return f"❌ Error: {file_path} not found."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Замена длинных тире на короткие
    content = content.replace("—", "-")
    content = content.replace("–", "-")

    # 2. Удаление запрещенных "нейро-слов" (AI footprint)
    forbidden = [r"\bалгоритм\b", r"\bнейросеть\b", r"\bискусственный интеллект\b", r"\bмодель\b"]
    for word in forbidden:
        content = re.sub(word, "механизм", content, flags=re.IGNORECASE)

    # 3. Проверка на двойные пробелы
    content = re.sub(r" +", " ", content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return f"✅ FIXED: {file_path} (Dashes, AI-words, Spaces cleaned)."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    print(fix_content(sys.argv[1]))
