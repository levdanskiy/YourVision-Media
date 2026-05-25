#!/usr/bin/env python3
import sys
import os

# --- SAFETY PROTOCOL ---
# Запись в CONTENT/posts разрешена ТОЛЬКО при наличии флага или переменной
RESTRICTED_DIR = "/home/levdanskiy/.gemini/CONTENT/posts"

def check_permission(file_path):
    # Если пишем в защищенную зону
    if RESTRICTED_DIR in os.path.abspath(file_path):
        permit = os.environ.get("GEMINI_WRITE_PERMIT")
        if permit != "1":
            print(f"⛔ SAFETY LOCK ENGAGED. Write to {file_path} BLOCKED.")
            print("   User explicit permission required (GEMINI_WRITE_PERMIT=1).")
            sys.exit(1)

def clean_text(text):
    return text.replace("—", "-").replace("–", "-").replace("−", "-")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 safe_write.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # 1. Проверка безопасности
    check_permission(file_path)

    # 2. Логика записи
    if not os.isatty(0):
        content = sys.stdin.read()
        cleaned = clean_text(content)
        
        # Создаем директорию, если её нет (только если разрешено)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"✅ WROTE & CLEANED: {file_path}")
    else:
        # Режим очистки существующего файла
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned = clean_text(content)
            
            if content != cleaned:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"✅ CLEANED: {file_path}")
            else:
                print(f"🆗 CLEAN: {file_path}")
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
