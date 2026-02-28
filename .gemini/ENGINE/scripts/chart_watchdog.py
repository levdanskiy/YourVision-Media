#!/usr/bin/env python3
import sys
import datetime
import os

def check_chart_slots(target_date_str=None):
    if target_date_str:
        dt = datetime.datetime.strptime(target_date_str, "%d.%m.%Y")
    else:
        dt = datetime.datetime.now()
    
    weekday = dt.weekday() # 0=Mon, 1=Tue, ..., 6=Sun
    date_formatted = dt.strftime("%d.%m")
    
    requirements = {
        1: [("19:20", "#CHART_RESULTS"), ("20:30", "#CHART_ANNOUNCE")], # Tuesday
        2: [("15:00", "#CHART_REMINDER")], # Wednesday
        4: [("19:00", "#CHART_REMINDER")], # Friday
        6: [("15:00", "#CHART_REMINDER")]  # Sunday (Moved to 15:00 to free up 12:00 for ESC_RELEASES)
    }
    
    if weekday not in requirements:
        return True, f"No chart slots required for {date_formatted}."
    
    req_slots = requirements[weekday]
    plan_path = f".gemini/system/workflow/daily_plan_{date_formatted}.md"
    
    if not os.path.exists(plan_path):
        return False, f"CRITICAL: Plan file {plan_path} not found to check chart slots!"
    
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan_content = f.read()
    
    missing = []
    for time, tag in req_slots:
        if time not in plan_content or tag not in plan_content:
            missing.append(f"{time} {tag}")
            
    if missing:
        return False, f"MISSING CHART SLOTS for {date_formatted}: {', '.join(missing)}"
    
    return True, f"All chart slots for {date_formatted} are present in the daily plan."

if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    ok, msg = check_chart_slots(date_arg)
    if ok:
        print(f"✅ {msg}")
        sys.exit(0)
    else:
        print(f"❌ {msg}")
        sys.exit(1)