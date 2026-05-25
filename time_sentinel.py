#!/usr/bin/env python3
import sys
import re

# YourVision Time-Sentinel V1.0
# Guarding Europe/Riga timezone constraints and zero-hallucination dates

def check_time_standards(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\033[1;36m⏰ TIME SENTINEL: {file_path}\033[0m")
    errors = 0

    # 1. Broadcaster CET/CEST ban check in post text
    if "cet" in content.lower() or "cest" in content.lower():
        # Exclude Midjourney prompt lines just in case
        lines_with_cet = []
        for line in content.split("\n"):
            if not line.startswith("Prompt:") and not line.startswith("**Prompt:"):
                if "cet" in line.lower() or "cest" in line.lower():
                    lines_with_cet.append(line.strip())
        if lines_with_cet:
            print("\033[1;31m❌ ERROR: Prohibited timezone (CET/CEST) found in text. Convert all times to Riga EET/EEST.\033[0m")
            for l in lines_with_cet:
                print(f"  -> {l}")
            errors += 1

    # 2. Header publishing date check
    pub_match = re.search(r"//\s*ДАТА ПУБЛИКАЦИИ:\s*(.+)", content)
    if pub_match:
        pub_val = pub_match.group(1).strip()
        # Expecting format like: 25.05.2026, 12:00 (Europe/Riga)
        if "Europe/Riga" not in pub_val:
            print(f"\033[1;31m❌ ERROR: Timezone '(Europe/Riga)' not explicitly defined in ДАТА ПУБЛИКАЦИИ: {pub_val}\033[0m")
            errors += 1
        
        # Verify format (DD.MM.YYYY, HH:MM (Europe/Riga))
        fmt_match = re.match(r"\d{2}\.\d{2}\.\d{4},\s+\d{2}:\d{2}\s+\(Europe/Riga\)", pub_val)
        if not fmt_match:
            print(f"\033[1;31m❌ ERROR: Invalid header publishing date format: '{pub_val}'. Expected format: 'DD.MM.YYYY, HH:MM (Europe/Riga)'\033[0m")
            errors += 1
    else:
        print("\033[1;33m⚠️ WARNING: System header '// ДАТА ПУБЛИКАЦИИ' not found in file. Skipping header timezone validation.\033[0m")

    if errors == 0:
        print("\033[1;32m✅ TIME VALIDATED: Europe/Riga timezone constraints fully respected.\033[0m")
        return True
    else:
        print(f"\033[1;36m--- Time Sentinel: {errors} issues found ---\033[0m")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        success = check_time_standards(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        print("Usage: python3 time_sentinel.py [file_path]")
        sys.exit(1)
