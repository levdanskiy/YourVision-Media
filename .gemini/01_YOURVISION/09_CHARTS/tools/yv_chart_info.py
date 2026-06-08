#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YourVision Chart Info Fetcher
Parses the schedule to report what chart actions are active on a given date.
"""

import sys
import os
import re
import datetime

SCHEDULE_PATH = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/09_CHARTS/YV_Charts_Schedule.md"

def get_chart_for_date(target_date_str):
    # Normalize input date format
    if len(target_date_str) > 5:
        # e.g., "07.06.2026" -> "07.06"
        target_date_str = target_date_str[:5]
        
    if not os.path.exists(SCHEDULE_PATH):
        return f"Error: Schedule file {SCHEDULE_PATH} not found."

    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    row_pattern = re.compile(r"^\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", re.MULTILINE)
    
    events_found = []
    
    for match in row_pattern.finditer(content):
        cols = [c.strip() for c in match.groups()]
        if cols[0].lower() == "серия" or "announce" in cols[2].lower():
            continue
            
        series = cols[0]
        theme = re.sub(r"\*\*|\*", "", cols[1])
        announce_field = cols[2]
        results_field = cols[3]
        status = cols[4]
        
        # Check announce
        announce_match = re.search(r"(\d{2}\.\d{2})\s+(\d{2}:\d{2})", announce_field)
        if announce_match:
            date_part, time_part = announce_match.groups()
            if date_part == target_date_str:
                events_found.append(f"🆕 **ANNOUNCE ({time_part}):** {series}: {theme} (Status: {status})")
                
        # Check results
        results_match = re.search(r"(\d{2}\.\d{2})\s+(\d{2}:\d{2})", results_field)
        if results_match:
            date_part, time_part = results_match.groups()
            if date_part == target_date_str:
                events_found.append(f"🏆 **RESULTS ({time_part}):** {series}: {theme} (Status: {status})")
                
            # Check reminder (T-1 day / T+6, at 17:50)
            try:
                res_date = datetime.datetime.strptime(f"{date_part}.2026", "%d.%m.%Y")
                rem_date = res_date - datetime.timedelta(days=1)
                rem_date_str = rem_date.strftime("%d.%m")
                if rem_date_str == target_date_str:
                    events_found.append(f"📢 **REMINDER (17:50):** {series}: {theme} (Voting closes tomorrow at {time_part})")
            except Exception:
                pass
                
    if events_found:
        header = f"📅 **SCHEDULED FOR {target_date_str}:**\n"
        return header + "\n".join(events_found)
    else:
        return f"📅 **DATE:** {target_date_str}\nNo chart events scheduled for this date."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        target_date = datetime.datetime.now().strftime("%d.%m")
    else:
        target_date = sys.argv[1]
        
    print(get_chart_for_date(target_date))
