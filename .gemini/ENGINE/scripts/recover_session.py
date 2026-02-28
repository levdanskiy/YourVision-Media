#!/usr/bin/env python3
import os
import sys
import datetime

CORE_PATH = "/home/levdanskiy/.gemini/"
STATE_FILE = os.path.join(CORE_PATH, "CORE/STATE.md")
COMMAND_REF = os.path.join(CORE_PATH, "COMMAND_REFERENCE.md")

def recover():
    print("\n\u23f3 SYSTEM RECOVERY INITIATED...")
    
    # 1. Read State
    state_info = "UNKNOWN"
    active_plan = "UNKNOWN"
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            for line in f:
                if "Real Date" in line: state_info = line.strip()
                if "Active Plan" in line: active_plan = line.split("`")[1]
    
    print(f"\ud83d\udcc5 Last Known State: {state_info}")
    print(f"\ud83d\udcb0 Active Plan: {active_plan}")

    # 2. Check Plan Status
    if active_plan != "UNKNOWN":
        plan_path = os.path.join(CORE_PATH, "TIMELINE/daily_workflow", active_plan)
        if os.path.exists(plan_path):
            print("\n\u26a0 PENDING TASKS (NEXT ACTIONS):")
            with open(plan_path, 'r') as f:
                for line in f:
                    if "⬜" in line:
                        print(f"   {line.strip()}")
                        break # Show only the first pending task
        else:
            print(f"\u274c Error: Plan file {active_plan} not found!")

    # 3. Memory Reinforcement
    print("\n\ud83e\udd7a MEMORY REFRESH:")
    print("   - Mandate: NO WRITE without explicit command.")
    print("   - Format AC: Ultimate List (5 categories).")
    print("   - Format YV: Insider Tone + 3D Branding.")
    
    print("\n\u2705 SYSTEM RESTORED. READY FOR COMMAND.")

if __name__ == "__main__":
    recover()
