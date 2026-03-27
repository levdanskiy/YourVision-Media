import sys
import os

def audit_file(file_path):
    if not os.path.exists(file_path):
        return True
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Проверка 1: Запрет на многоточия в коде
    if '...' in content:
        print(f"CRITICAL ERROR: Truncation detected in {file_path} ('...')")
        return False
    
    # Проверка 2: Проверка наличия обязательных блоков дизайна
    if 'index.html' in file_path:
        required_blocks = ['hero-view', 'layout', 'column', 'card', 'syncRadio']
        for block in required_blocks:
            if block not in content:
                print(f"CRITICAL ERROR: Design block '{block}' missing in index.html")
                return False
                
    return True

if __name__ == "__main__":
    files_to_check = ['index.html', 'data.js', 'YV_Editor_Hub.html']
    all_passed = True
    for f in files_to_check:
        if not audit_file(f):
            all_passed = False
            
    if not all_passed:
        sys.exit(1)
    else:
        print("AUDIT PASSED: Integrity verified.")
        sys.exit(0)
