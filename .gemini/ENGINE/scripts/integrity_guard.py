#!/usr/bin/env python3
import sys
import os

def check_structural_integrity(file_path, new_content):
    # Если это сводный план (daily_plan), проверяем наличие долгов
    if "daily_plan_" in file_path:
        critical_blocks = [
            "ДОЛГИ", 
            "Recovery Queue", 
            "ALMANAC (Main)", 
            "ALMANAC: NEIGHBORS", 
            "ALMANAC: SWEET", 
            "YOURVISION"
        ]
        
        for block in critical_blocks:
            if block not in new_content:
                return False, f"КРИТИЧЕСКИЙ СБОЙ: В новом плане отсутствует обязательный блок '{block}'!"

    return True, "Структурная целостность подтверждена."

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    f_path = sys.argv[1]
    content = sys.stdin.read()
    
    ok, msg = check_structural_integrity(f_path, content)
    if not ok:
        print(f"❌ {msg}")
        sys.exit(1)
    else:
        sys.exit(0)
