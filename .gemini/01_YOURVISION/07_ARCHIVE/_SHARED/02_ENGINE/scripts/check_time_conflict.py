import os
import re
from datetime import datetime, timedelta

PLAN_DIR = "/home/levdanskiy/.gemini/TIMELINE/daily_workflow"

def check_conflicts(date_str):
    plan_path = os.path.join(PLAN_DIR, f"daily_plan_{date_str}.md")
    if not os.path.exists(plan_path):
        return f"Plan for {date_str} not found."

    with open(plan_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    slots = []
    # Parse all slots
    for i, line in enumerate(lines):
        match = re.search(r"\*\s*(\d{2}:\d{2})\s*\|\s*\*\*(\w{2})\*\*", line)
        if match:
            time_str, channel = match.groups()
            dt = datetime.strptime(time_str, "%H:%M")
            slots.append({
                "time": dt,
                "time_str": time_str,
                "channel": channel,
                "line_idx": i,
                "original_line": line
            })

    # Sort by time
    slots.sort(key=lambda x: x["time"])

    conflicts = []
    
    # Check intervals
    for i in range(len(slots) - 1):
        current = slots[i]
        next_slot = slots[i+1]
        
        diff = (next_slot["time"] - current["time"])
        
        if diff.total_seconds() < 1800: # Conflict threshold: 30 mins
            conflicts.append((current, next_slot, diff.total_seconds() / 60))

    if not conflicts:
        return "✅ No time conflicts found."

    report = "⚠️ TIME CONFLICTS DETECTED:\n"
    for c1, c2, diff in conflicts:
        report += f"   - {c1['time_str']} ({c1['channel']}) vs {c2['time_str']} ({c2['channel']}) | Diff: {int(diff)} min\n"
    
    return report

if __name__ == "__main__":
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%d.%m.%Y")
    print(check_conflicts(d))