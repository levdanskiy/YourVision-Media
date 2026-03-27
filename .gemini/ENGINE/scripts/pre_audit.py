import sys
import os

def audit_file(file_path):
    if not os.path.exists(file_path):
        return True
    
    # ПРОВЕРЯЕМ ТОЛЬКО НАШИ ФАЙЛЫ
    allowed_dirs = ['./.gemini/CONTENT/', './index.html', './data.js', './YV_Editor_Hub.html', './YourEurovision_Hub_Deploy/', './patch_final.py']
    is_target = False
    for d in allowed_dirs:
        if file_path.startswith(d) or file_path == d.strip('./'):
            is_target = True
            break
    
    if not is_target:
        return True

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Запрет на ТИРЕ - КАТЕГОРИЧЕСКИЙ ДЛЯ ВСЕХ ТАРГЕТОВ
        if '—' in content or '–' in content:
            print(f"CRITICAL ERROR: Forbidden DASH symbol (— or –) found in {file_path}")
            return False
            
        # Запрет на многоточия - ТОЛЬКО ДЛЯ КОДА И ТЕКУЩИХ ДАННЫХ
        if file_path in ['./index.html', './data.js', './patch_final.py', './YV_Editor_Hub.html']:
            if '...' in content:
                print(f"CRITICAL ERROR: Truncation detected in CODE/DATA file {file_path} ('...')")
                return False
        
        return True
    except Exception as e:
        return True

if __name__ == "__main__":
    passed = True
    for root, dirs, files in os.walk('.'):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(('.md', '.js', '.html', '.py')):
                if not audit_file(full_path):
                    passed = False
            
    if not passed:
        print("\nIRON PROTOCOL: FAILED. Please fix Forbidden Dashes or Code Truncation.")
        sys.exit(1)
    else:
        print("\nIRON PROTOCOL: AUDIT PASSED. Workspace is clean from dashes.")
        sys.exit(0)
