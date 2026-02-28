#!/usr/bin/env python3
import sys
import os
import re

def update_lore(post_content):
    lore_path = ".gemini/system/YV_Season_2026.md"
    # Ищем ключевые факты (победители, даты)
    winner = re.search(r'(Победитель|Переможець|Winner): \*\*([^*]+)\*\*', post_content)
    
    if winner:
        fact = f"- **Fact:** {winner.group(2)} зафиксирован в Лоре."
        with open(lore_path, 'a') as f:
            f.write(f"\n{fact}")
        return True, "Lore updated automatically."
    
    return False, "No key facts found."

if __name__ == "__main__":
    content = sys.stdin.read()
    update_lore(content)

