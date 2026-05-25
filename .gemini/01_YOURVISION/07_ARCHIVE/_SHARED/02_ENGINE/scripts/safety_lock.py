#!/usr/bin/env python3
import sys
import os

LOCK_FILE = "/home/levdanskiy/.gemini/.safety_lock"

def check_lock():
    if os.path.exists(LOCK_FILE):
        print("❌ SAFETY LOCK ACTIVE. Operation aborted. Explicit user confirmation required.")
        sys.exit(1)
    return True

def set_lock(state):
    if state == "on":
        with open(LOCK_FILE, "w") as f:
            f.write("LOCKED")
        print("🔒 SYSTEM LOCKED. Autonomous generation disabled.")
    elif state == "off":
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        print("🔓 SYSTEM UNLOCKED. Ready for single command execution.")
    else:
        print(f"Usage: {sys.argv[0]} [on|off]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_lock(sys.argv[1].lower())
    else:
        # Default behavior when imported or run without args: check lock
        check_lock()