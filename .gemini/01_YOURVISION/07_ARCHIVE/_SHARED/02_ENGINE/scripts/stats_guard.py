import sys
import re

def check_stats(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Извлечение Grade
    grade_match = re.search(r"Grade ([BASS]{1,2})", content)
    if not grade_match:
        return "ERROR: Grade metadata not found!"
    
    grade = grade_match.group(1)
    
    # Очистка текста от системной инфы для честного подсчета
    text_body = content.split('🍰')[-1].split('***')[0]
    char_count = len(text_body.replace(" ", "").replace("\n", ""))
    
    limits = {
        'B': (300, 800),
        'A': (801, 1500),
        'S': (1501, 2500),
        'SS': (2501, 4500)
    }
    
    low, high = limits.get(grade, (0, 9999))
    
    if char_count < low:
        return f"CRITICAL FAILURE: Text too short for Grade {grade} ({char_count} chars, min {low})"
    if char_count > high:
        return f"CRITICAL FAILURE: Text too long for Grade {grade} ({char_count} chars, max {high})"
    
    return f"PASS: Grade {grade} verified ({char_count} chars)"

if __name__ == "__main__":
    print(check_stats(sys.argv[1]))
