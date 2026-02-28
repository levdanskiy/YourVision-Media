#!/usr/bin/env python3
import sys
import os
import re
import datetime

CORE_PATH = "/home/levdanskiy/.gemini/"
PLAN_DIR = os.path.join(CORE_PATH, "TIMELINE/daily_workflow/")

def run_slot(time_target):
    today = datetime.datetime.now().strftime("%d.%m")
    plan_path = os.path.join(PLAN_DIR, f"daily_plan_{today}.md")
    
    if not os.path.exists(plan_path):
        return f"❌ No plan for {today} found."

    with open(plan_path, 'r') as f:
        lines = f.readlines()

    # Find the line with the target time
    target_line = ""
    for line in lines:
        if time_target in line and ("⬜" in line or "✅" in line):
            target_line = line
            break
    
    if not target_line:
        return f"❌ Slot for {time_target} not found in {today} plan."

    # Parse channel and topic
    # Example: * 08:30 | **AC** | 🌀 #ALCHEMY_OF_SYNC: Topic. - ⬜ [ОЖИДАНИЕ]
    match = re.search(r"\*\s*(\d{2}:\d{2})\s*\|\s*\*\*(\w{2})\*\*\s*\|\s*(.*?) -", target_line)
    if not match:
        return f"❌ Could not parse slot data: {target_line}"

    time, channel, topic = match.groups()
    
    # --- 1. FETCH SYNERGY CONTEXT ---
    synergy_script = "/home/levdanskiy/.gemini/ENGINE/agents/mnemosyne_nexus.py"
    synergy_context = os.popen(f"python3 {synergy_script} get_context").read()

    # --- 2. EXECUTE POWER PACK ---
    output = os.popen(f"python3 {CORE_PATH}ENGINE/scripts/context_router.py {channel} {topic}").read()
    
    # Inject synergy into output for the model to see
    output += synergy_context

    # ... (After post is written successfully) ...
    # --- 3. RECORD EVENT FOR FUTURE SYNERGY ---
    os.popen(f"python3 {synergy_script} record {channel} '{topic}'").read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: @do HH:MM")
        sys.exit(1)
    print(run_slot(sys.argv[1]))
