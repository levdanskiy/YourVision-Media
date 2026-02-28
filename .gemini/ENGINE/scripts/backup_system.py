#!/usr/bin/env python3
import shutil
import os
from datetime import datetime

def make_backup():
    backup_dir = f".gemini/system/archive/backups/{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    source_dir = ".gemini/system/calendars/"
    for f in os.listdir(source_dir):
        if f.endswith(".md"):
            shutil.copy(os.path.join(source_dir, f), backup_dir)
            
    print(f"✅ Backup created in: {backup_dir}")

if __name__ == "__main__":
    make_backup()
