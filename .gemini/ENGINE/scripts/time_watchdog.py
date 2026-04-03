import time
import json
from datetime import datetime
import os

LOG_PATH = "/home/levdanskiy/.gemini/system/REAL_TIME.json"

def watchdog():
    while True:
        now = datetime.now()
        data = {
            "timestamp": time.time(),
            "readable": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%d.%m.%Y"),
            "path_segment": now.strftime("%Y/%m/%d"),
            "hour": now.hour,
            "minute": now.minute
        }
        with open(LOG_PATH, 'w') as f:
            json.dump(data, f)
        time.sleep(1)

if __name__ == "__main__":
    # Ensure dir exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    watchdog()
