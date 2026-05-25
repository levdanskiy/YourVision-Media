#!/usr/bin/env python3
import sys
import os
import re

def sync_lore(file_path):
    if not os.path.exists(file_path): return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем заголовок даты и Озарение
    date_match = re.search(r'Date: (\d{2}\.\d{2})', content)
    insight_match = re.search(r'\*\*ОЗАРЕННЯ\*\*\n(.*?)\n', content, re.DOTALL | re.IGNORECASE)
    
    if date_match and insight_match:
        date = date_match.group(1)
        insight = insight_match.group(1).strip().replace("||", "") # Убираем спойлеры для лора
        
        lore_path = ".gemini/system/config/ALMANAC_LORE.md"
        with open(lore_path, 'a', encoding='utf-8') as f:
            f.write(f"\n- **{date}:** {insight}")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    sync_lore(sys.argv[1])
