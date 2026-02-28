#!/usr/bin/env python3
import sys
import os
import shutil
from datetime import datetime

POSTS_BASE = "/home/levdanskiy/.gemini/CONTENT/posts/"

def archive_post(file_path):
    if not os.path.exists(file_path):
        return f"❌ Error: {file_path} not found."

    # Extract date from filename or content (Simplified: use current date)
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    target_dir = os.path.join(POSTS_BASE, year, month, day)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    filename = os.path.basename(file_path)
    target_path = os.path.join(target_dir, filename)

    try:
        shutil.copy2(file_path, target_path)
        return f"📦 ARCHIVED: {filename} moved to {year}/{month}/{day}"
    except Exception as e:
        return f"❌ Archive failed: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    print(archive_post(sys.argv[1]))
