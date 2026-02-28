#!/usr/bin/env python3
import sys
import json
import os
import random

DNA_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/SUPREME_VISUAL_DNA.json"

def get_smart_ar(channel, topic):
    channel = channel.upper()
    topic = topic.lower()
    
    # 1. ТРЕНДОВЫЕ ИНТЕНТЫ (Абсолютный приоритет)
    if any(k in topic for k in ["reels", "story", "shorts"]): return "9:16"
    if any(k in topic for k in ["cinema", "panoramic", "landscape"]): return "21:9"
    if any(k in topic for k in ["chart", "stats", "grid"]): return "1:1"

    # 2. ВЕРОЯТНОСТНАЯ РОТАЦИЯ (75% Тренды / 25% Классика)
    if os.path.exists(DNA_PATH):
        with open(DNA_PATH, 'r') as f:
            dna = json.load(f)
        
        ar_pool = dna.get("ar_trends", {
            "trending": ["4:5", "9:16"], 
            "classic": ["1:1", "16:9", "3:2"]
        })

        chance = random.random()
        if chance < 0.75: # 75% вероятность ТРЕНДА
            return random.choice(ar_pool["trending"])
        else: # 25% вероятность КЛАССИКИ
            return random.choice(ar_pool["classic"])
    
    return "3:2"

if __name__ == "__main__":
    ch = sys.argv[1] if len(sys.argv) > 1 else "AC"
    top = sys.argv[2] if len(sys.argv) > 2 else "General"
    print(f"🖼️ **SMART AR SELECTED:** --ar {get_smart_ar(ch, top)}")