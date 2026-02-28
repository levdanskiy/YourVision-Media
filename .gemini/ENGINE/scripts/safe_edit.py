#!/usr/bin/env python3
import sys
import os
import shutil

def safe_replace(file_path, old_string, new_string):
    if not os.path.exists(file_path):
        return False, "File not found"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_string not in content:
        return False, "Old string not found in file"

    # Создаем бэкап
    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)

    new_content = content.replace(old_string, new_string, 1) # Replace only first occurrence usually, or add count

    # SAFETY CHECK 1: Length
    if len(new_content) < len(content) * 0.8: # Если файл сократился более чем на 20%
        shutil.copy2(backup_path, file_path) # Restore
        return False, "SAFETY TRIGGER: New content is significantly shorter. Potential data loss."

    # SAFETY CHECK 2: Structure markers (Optional, for specific files)
    # if "Plan" in file_path and "---" not in new_content: ...

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        shutil.copy2(backup_path, file_path)
        return False, f"Write error: {str(e)}"

    os.remove(backup_path)
    return True, "Success"

if __name__ == "__main__":
    # Usage: python3 safe_edit.py <file> <old_string> <new_string>
    # Note: This simple cli arg handling is risky for multiline strings. 
    # Better to use it as a library or pass arguments carefully.
    pass 
