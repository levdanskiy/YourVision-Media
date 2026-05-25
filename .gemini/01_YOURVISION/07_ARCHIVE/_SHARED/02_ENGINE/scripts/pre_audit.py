import os
import sys
import re

def audit_post(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    errors = []
    # 1. Проверка тире
    if '—' in content or '–' in content: errors.append('ЗАПРЕЩЕННОЕ ТИРЕ')
    
    # 2. Проверка объема (Grade A требует глубины)
    if len(content) < 1200: errors.append('СЛИШКОМ КОРОТКИЙ ТЕКСТ (PLACEHOLDER)')
    
    # 3. Проверка временного окна (10:00 - 20:00)
    time_match = re.search(r'ДАТА ПУБЛИКАЦИИ: .*, (\d{2}):(\d{2})', content)
    if time_match:
        hour = int(time_match.group(1))
        if hour < 10 or hour > 20: errors.append(f'НАРУШЕНИЕ ОКНА ПУБЛИКАЦИИ ({hour}:00)')

    # 4. Проверка обязательных блоков
    if 'SOUNDSCAPE' not in content: errors.append('ОТСУТСТВУЕТ SOUNDSCAPE')
    if 'ALLIANCE NEWS WIRE' not in content: errors.append('ОТСУТСТВУЕТ NEWS WIRE')
    if 'Prompt:' not in content: errors.append('ОТСУТСТВУЕТ PROMPT')

    if errors:
        print(f'--- [CRITICAL AUDIT FAILURE] ---')
        for e in errors: print(f'🔴 {e}')
        return False
    
    print('--- [AUDIT SUCCESS] ВСЕ ПРАВИЛА СОБЛЮДЕНЫ ---')
    return True

if __name__ == '__main__':
    if not audit_post(sys.argv[1]): sys.exit(1)

