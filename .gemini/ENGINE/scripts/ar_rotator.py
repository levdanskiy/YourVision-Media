#!/usr/bin/env python3
import json
import random
import sys
import os

HISTORY_FILE = "/home/levdanskiy/.gemini/CORE/knowledge/ar_history.json"

# FULL CINEMATIC ARSENAL (23+ Formats)
ASPECT_RATIOS = [
    "16:9", "9:16", "1:1", "4:5", "5:4", "3:2", "2:3", 
    "21:9", "9:21", "2.39:1", "1:2.39", "2.76:1", # Ultra Panavision
    "1.43:1", "1.90:1", # IMAX
    "4:3", "3:4", "5:7", "7:5", 
    "10:16", "16:10", "2:1", "1:2", "1.85:1"
]

def get_ar(channel):
    channel = channel.lower()
    
    # Load History
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    else:
        history = {"ac": [], "nb": [], "sw": [], "yv": []}

    last_used = history.get(channel, [])
    
    # Filter out recently used to ensure variety
    available = [ar for ar in ASPECT_RATIOS if ar not in last_used[-10:]] 
    
    if not available:
        available = ASPECT_RATIOS # Reset if exhausted

    new_ar = random.choice(available)
    
    # Update History
    last_used.append(new_ar)
    if len(last_used) > 15: # Keep history short
        last_used.pop(0)
    history[channel] = last_used
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
        
    return new_ar

if __name__ == "__main__":
    channel = sys.argv[1] if len(sys.argv) > 1 else "ac"
    print(get_ar(channel))