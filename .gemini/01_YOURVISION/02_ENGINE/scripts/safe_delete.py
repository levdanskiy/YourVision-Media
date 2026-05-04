#!/usr/bin/env python3
import sys
import os
import shutil
import datetime

TRASH_DIR = "/home/levdanskiy/.gemini/TRASH"

def safe_delete(path):
    if not os.path.exists(path):
        print(f"❌ ERROR: File not found: {path}")
        return

    # Create trash directory if it doesn't exist
    if not os.path.exists(TRASH_DIR):
        os.makedirs(TRASH_DIR)

    # Generate timestamped name to avoid collisions
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(path)
    trash_path = os.path.join(TRASH_DIR, f"{filename}_{timestamp}")

    try:
        shutil.move(path, trash_path)
        print(f"♻️  MOVED TO TRASH: {path} -> {trash_path}")
    except Exception as e:
        print(f"❌ ERROR moving file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 safe_delete.py <file_path>")
        sys.exit(1)
    
    # Support wildcards processed by shell expansion passed as separate args
    for file_path in sys.argv[1:]:
        safe_delete(file_path)
