import sys
import re

def validate_style(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    body_started = False
    
    for line in lines:
        # Ignore system header and footer tags
        if line.startswith('//') or line.startswith('`⏱') or line.startswith('***') or line.startswith('**Grade:') or line.startswith('**Prompt:'):
            continue
            
        # Check for forbidden dashes
        if '—' in line or '–' in line:
            errors.append(f"ERROR: Forbidden dash in line: {line.strip()}")
            
        # Check for ANY line starting with # (Markdown headers)
        if line.strip().startswith('#'):
            errors.append(f"ERROR: Forbidden hashtag/header at line start: {line.strip()}")
    
    if errors:
        for err in errors:
            print(err)
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if not validate_style(sys.argv[1]):
            sys.exit(1)
