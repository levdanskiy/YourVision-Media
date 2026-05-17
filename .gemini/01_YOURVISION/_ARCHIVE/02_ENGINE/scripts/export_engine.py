#!/usr/bin/env python3
import sys
import os
import re

def clean_for_telegram(file_path):
    if not os.path.exists(file_path):
        return f"❌ ERROR: File {file_path} not found."
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    clean_text = []
    capture = False
    
    for line in lines:
        # Игнорируем системные комментарии // и метаданные в конце
        if line.startswith("//"): continue
        if line.startswith("---"): break # Конец тела поста
        if "PROMPT:" in line: break # Конец тела поста
        
        clean_text.append(line)
        
    return "".join(clean_text).strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 export_engine.py <file_path>")
    else:
        print(clean_for_telegram(sys.argv[1]))
