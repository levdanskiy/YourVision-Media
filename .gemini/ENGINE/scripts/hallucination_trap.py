#!/usr/bin/env python3
import sys
import os
import datetime
import re

class HallucinationTrap:
    def __init__(self, requested_slot):
        self.requested_slot = requested_slot
        self.plan_path = "/home/levdanskiy/.gemini/TIMELINE/daily_workflow/daily_plan_04.02.md" # Dynamic date in prod
        self.history_path = "/home/levdanskiy/.gemini/CORE/history/execution_log.txt"
        self.lock_file = "/home/levdanskiy/.gemini/tmp/SAFETY_LOCK_ACTIVE"

    def check_safety_lock(self):
        """Checks if the manual safety lock is active."""
        if os.path.exists(self.lock_file):
            print("❌ TRAP BLOCKED: Safety Lock is ENGAGED. Explicit permission required.")
            return False
        return True

    def check_plan_integrity(self):
        """Checks if the requested slot exists in the daily plan and is pending."""
        if not self.check_safety_lock():
            return False
        
        # Extract time and channel from request (e.g., "18:30 | NB")
        match = re.search(r"(\d{2}:\d{2})\s*\|\s*(\w{2})", self.requested_slot)
        if not match:
            print("❌ TRAP: Invalid slot format in request.")
            return False
        
        time, channel = match.groups()
        
        with open(self.plan_path, 'r') as f:
            plan_content = f.read()
            
        # Regex to find the specific slot line (Supports standard and Debt format)
        # Matches: "12:00 | **YV**" OR "[31.01] | 12:00 | **YV**"
        slot_regex = f"(\[.*?\]\s*\|\s*)?{time}\s*\|\s*\*\*{channel}\*\*.*?(✅|⬜)"
        found_slot = re.search(slot_regex, plan_content)
        
        if not found_slot:
            print(f"❌ TRAP: Slot {time} | {channel} NOT FOUND in daily plan.")
            return False
            
        status = found_slot.group(1)
        if status == "✅":
            print(f"❌ TRAP: Slot {time} | {channel} is ALREADY DONE.")
            return False
            
        print(f"✅ TRAP: Slot {time} | {channel} is VALID and PENDING.")
        return True

    def log_execution(self):
        """Logs the valid execution attempt."""
        with open(self.history_path, 'a') as f:
            f.write(f"{datetime.datetime.now()} - EXEC: {self.requested_slot}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hallucination_trap.py '<Requested Slot String>'")
        sys.exit(1)
        
    trap = HallucinationTrap(sys.argv[1])
    if trap.check_plan_integrity():
        trap.log_execution()
        sys.exit(0) # Success
    else:
        sys.exit(1) # Block execution
