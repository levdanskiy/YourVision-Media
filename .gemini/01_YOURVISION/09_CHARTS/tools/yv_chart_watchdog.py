#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YourVision Charts Watchdog
Checks master plans and daily plans for required chart posting slots based on YV_Charts_Schedule.md.
"""

import sys
import os
import re
import datetime

SCHEDULE_PATH = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/09_CHARTS/YV_Charts_Schedule.md"
MASTER_PLANS_DIR = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/06_TIMELINE/master_plans"
DAILY_PLAN_DIR = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/06_TIMELINE/daily_workflow"

def get_scheduled_slots(target_date_str):
    # target_date_str: "DD.MM"
    if not os.path.exists(SCHEDULE_PATH):
        print(f"ERROR: Schedule file {SCHEDULE_PATH} not found.")
        sys.exit(1)
        
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    expected_slots = []
    
    # Simple regex to parse markdown table rows
    # Example: | WorldSound | Theme | 07.06 20:30 | 14.06 19:20 | ⬜ PLAN |
    row_pattern = re.compile(r"^\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", re.MULTILINE)
    
    for match in row_pattern.finditer(content):
        cols = [c.strip() for c in match.groups()]
        if cols[0].lower() == "серия" or "announce" in cols[2].lower():
            continue # Header row
            
        series = cols[0]
        theme = re.sub(r"\*\*|\*", "", cols[1])
        announce_field = cols[2] # e.g. "07.06 20:30"
        results_field = cols[3] # e.g. "14.06 19:20"
        
        # Check announce
        announce_match = re.search(r"(\d{2}\.\d{2})\s+(\d{2}:\d{2})", announce_field)
        if announce_match:
            date_part, time_part = announce_match.groups()
            if date_part == target_date_str:
                expected_slots.append({
                    "time": time_part,
                    "tag": "#CHART", # can also be #ANNOUNCEMENT or #CHART_ANNOUNCE
                    "description": f"Announce of {series} ({theme})"
                })
                
        # Check results
        results_match = re.search(r"(\d{2}\.\d{2})\s+(\d{2}:\d{2})", results_field)
        if results_match:
            date_part, time_part = results_match.groups()
            if date_part == target_date_str:
                expected_slots.append({
                    "time": time_part,
                    "tag": "#CHART_RESULTS", # or #RESULTS
                    "description": f"Results of {series} ({theme})"
                })
                
            # Check reminder (T-1 day / T+6, at 17:50)
            try:
                res_date = datetime.datetime.strptime(f"{date_part}.2026", "%d.%m.%Y")
                rem_date = res_date - datetime.timedelta(days=1)
                rem_date_str = rem_date.strftime("%d.%m")
                if rem_date_str == target_date_str:
                    expected_slots.append({
                        "time": "17:50",
                        "tag": "#CHART_REMINDER",
                        "description": f"Reminder for {series} ({theme})"
                    })
            except Exception as e:
                pass
                
    return expected_slots

def check_plans(target_date_str, expected_slots):
    # Parse month for master plans path: e.g. "07.06" -> month "06"
    month = target_date_str[3:5]
    master_plan_path = os.path.join(MASTER_PLANS_DIR, month, f"YV_Plan_{month}.md")
    
    # Check if master plan exists
    master_content = ""
    if os.path.exists(master_plan_path):
        with open(master_plan_path, "r", encoding="utf-8") as f:
            master_content = f.read()
            
    # Extract specific day section from master plan: e.g. "### 07.06"
    day_section = ""
    if master_content:
        day_pattern = re.compile(rf"### {re.escape(target_date_str)}.*?(?=###|\Z)", re.DOTALL)
        day_match = day_pattern.search(master_content)
        if day_match:
            day_section = day_match.group(0)
            
    # Check if daily workflow plan exists
    daily_plan_path = os.path.join(DAILY_PLAN_DIR, f"daily_plan_{target_date_str}.md")
    daily_content = ""
    if os.path.exists(daily_plan_path):
        with open(daily_plan_path, "r", encoding="utf-8") as f:
            daily_content = f.read()
            
    combined_content = day_section + "\n" + daily_content
    
    missing = []
    for slot in expected_slots:
        time = slot["time"]
        tag = slot["tag"]
        
        # Check alternative tags as well
        # e.g., #CHART can be represented as #ANNOUNCEMENT or #CHART_ANNOUNCE
        # e.g., #CHART_RESULTS can be represented as #RESULTS
        time_found = time in combined_content
        tag_found = False
        
        tags_to_check = [tag]
        if tag == "#CHART":
            tags_to_check.extend(["#ANNOUNCEMENT", "#CHART_ANNOUNCE"])
        elif tag == "#CHART_RESULTS":
            tags_to_check.extend(["#RESULTS"])
            
        for t in tags_to_check:
            if t in combined_content:
                tag_found = True
                break
                
        # Robust check: does a line contain both the time and one of the tags?
        match_line = False
        for line in combined_content.split("\n"):
            if time in line:
                for t in tags_to_check:
                    if t in line:
                        match_line = True
                        break
                        
        if not (time_found and tag_found) and not match_line:
            missing.append(slot)
            
    return missing

def main():
    if len(sys.argv) < 2:
        # Default to today
        target_date_str = datetime.datetime.now().strftime("%d.%m")
    else:
        # Date argument can be DD.MM or DD.MM.YYYY
        arg = sys.argv[1]
        target_date_str = arg[:5]
        
    print(f"Checking scheduled chart slots for {target_date_str}...")
    expected = get_scheduled_slots(target_date_str)
    
    if not expected:
        print(f"✅ No chart events scheduled in YV_Charts_Schedule.md for {target_date_str}.")
        sys.exit(0)
        
    print(f"Scheduled slots found:")
    for slot in expected:
        print(f"  - {slot['time']} | {slot['tag']} ({slot['description']})")
        
    missing = check_plans(target_date_str, expected)
    
    if missing:
        print(f"\n❌ CRITICAL: Missing required chart slots in plans for {target_date_str}:")
        for slot in missing:
            print(f"  - Expected {slot['time']} with tag {slot['tag']} ({slot['description']})")
        sys.exit(1)
    else:
        print(f"\n✅ All scheduled chart slots for {target_date_str} are verified in plans.")
        sys.exit(0)

if __name__ == "__main__":
    main()
