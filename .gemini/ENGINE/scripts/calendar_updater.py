#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime

CALENDAR_PATH = "/home/levdanskiy/.gemini/KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md"

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d.%m")
    except ValueError:
        return None

def update_calendar(date, country, event, time=None):
    if not os.path.exists(CALENDAR_PATH):
        print(f"❌ Error: Calendar file not found at {CALENDAR_PATH}")
        return

    with open(CALENDAR_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Formating the new entry line
    flag_map = {
        "Ukraine": "🇺🇦", "Sweden": "🇸🇪", "Italy": "🇮🇹", "Spain": "🇪🇸", 
        "Norway": "🇳🇴", "Finland": "🇫🇮", "Lithuania": "🇱🇹", "Latvia": "🇱🇻",
        "Estonia": "🇪🇪", "Denmark": "🇩🇰", "Germany": "🇩🇪", "France": "🇫🇷",
        "UK": "🇬🇧", "San Marino": "🇸🇲", "Serbia": "🇷🇸", "Croatia": "🇭🇷",
        "Greece": "🇬🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴", "Luxembourg": "🇱🇺",
        "Austria": "🇦🇹", "Portugal": "🇵🇹", "Switzerland": "🇨🇭"
    }
    
    # Try to find flag if country is English name, otherwise assume country holds the flag or name
    flag = flag_map.get(country, "") 
    if not flag and any(x in country for x in flag_map.values()):
        flag = "" # Country string likely already contains flag
    
    time_str = f" ({time} CET)" if time else ""
    new_line = f"〰️ {date}: {flag} {country} - {event}{time_str}.\n"
    
    print(f"🔍 Processing: {new_line.strip()}")

    # Logic to insert in chronological order
    # This is a simplified insertion logic. A robust one would parse sections (Months).
    # For now, we append to the file for manual sorting or simple appending if specific month section logic is too complex for a single regex.
    # BETTER APPROACH: Read all lines, identify dates, insert in correct position.
    
    # 1. Identify the Month Section
    month_map = {
        "01": "Январь 2026", "02": "Февраль 2026", "03": "Март 2026", 
        "04": "Апрель 2026", "05": "Май 2026", "06": "Июнь 2026"
    }
    target_month_num = date.split('.')[1]
    target_month_header = month_map.get(target_month_num)
    
    if not target_month_header:
        print("⚠️ Warning: Unknown month. Appending to end.")
        with open(CALENDAR_PATH, 'a', encoding='utf-8') as f:
            f.write(new_line)
        return

    # 2. Find range of lines for that month
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if target_month_header in line:
            start_idx = i
        elif start_idx != -1 and line.strip() == "" and i > start_idx + 1: # Empty line usually ends a block
             # Check if next line is another month header
             if i + 1 < len(lines) and any(m in lines[i+1] for m in month_map.values()):
                 end_idx = i
                 break
    
    if end_idx == -1: end_idx = len(lines) # End of file if no next month found

    # 3. Insert chronologically within the range
    if start_idx != -1:
        month_lines = lines[start_idx+1 : end_idx]
        insertion_idx = end_idx # Default: append to end of month section
        
        target_dt = parse_date(date)
        
        for i, m_line in enumerate(month_lines):
            match = re.search(r'〰️ (\d{2}\.\d{2}):', m_line)
            if match:
                curr_date_str = match.group(1)
                curr_dt = parse_date(curr_date_str)
                if curr_dt and curr_dt > target_dt:
                    insertion_idx = start_idx + 1 + i
                    break
        
        # Check for duplicates before inserting
        if any(event in l for l in lines):
             print("⚠️ Event likely already exists. Skipping to avoid duplicates.")
             return

        lines.insert(insertion_idx, new_line)
        
        with open(CALENDAR_PATH, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ Successfully added to {target_month_header}.")
    else:
        # Month header not found, append to end
        print(f"⚠️ Month header '{target_month_header}' not found. Appending.")
        with open(CALENDAR_PATH, 'a', encoding='utf-8') as f:
            f.write(f"\n{target_month_header}\n{new_line}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 calendar_updater.py <DD.MM> <Country> <Event> [Time]")
        sys.exit(1)
    
    d = sys.argv[1]
    c = sys.argv[2]
    e = sys.argv[3]
    t = sys.argv[4] if len(sys.argv) > 4 else None
    
    update_calendar(d, c, e, t)
