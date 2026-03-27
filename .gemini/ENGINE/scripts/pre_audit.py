import sys
import os

def audit_file(file_path):
    if not os.path.exists(file_path):
        return True
    
    # Игнорируем бинарные файлы и скрытые папки
    if '.git' in file_path or '.cache' in file_path:
        return True

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Проверка 1: Запрет на многоточия в коде (вне кавычек новостей)
    # Но для надежности пока запрещаем везде
    if '...' in content:
        print(f"CRITICAL ERROR: Truncation detected in {file_path} ('...')")
        return False
    
    # Проверка 2: КАТЕГОРИЧЕСКИЙ ЗАПРЕТ НА ТИРЕ (— и –)
    if '—' in content or '–' in content:
        print(f"CRITICAL ERROR: Forbidden DASH symbol (— or –) found in {file_path}")
        return False
    
    # Проверка 3: Проверка наличия обязательных блоков дизайна
    if 'index.html' in file_path:
        required_blocks = ['hero-view', 'layout', 'column', 'card', 'syncRadio', 'team-song']
        for block in required_blocks:
            if block not in content:
                print(f"CRITICAL ERROR: Design block '{block}' missing in index.html")
                return False
                
    return True

if __name__ == "__main__":
    files_to_check = ['index.html', 'data.js', 'YV_Editor_Hub.html', 'patch_final.py']
    all_passed = True
    for f in files_to_check:
        if not audit_file(f):
            all_passed = False
            
    if not all_passed:
        print("IRON PROTOCOL: FAILED. Fix symbols before proceeding.")
        sys.exit(1)
    else:
        print("IRON PROTOCOL: AUDIT PASSED. Integrity verified (ZERO dashes, ZERO truncation).")
        sys.exit(0)
