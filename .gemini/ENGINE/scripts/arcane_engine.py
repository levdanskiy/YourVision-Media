#!/usr/bin/env python3
import sys
import random
import json
import os
import hashlib

REPOS_PATH = "/home/levdanskiy/.gemini/ENGINE/repos/esoteric_data"

def load_system(filename):
    path = os.path.join(REPOS_PATH, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def get_arcane_prediction(channel, date, time_salt):
    # Seed for reproducibility per slot
    seed_str = f"{channel}{date}{time_salt}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    random.seed(seed)

    # Expanded Systems
    systems = [
        {"file": "tarot_full.json", "name": "Tarot", "key": "cards"},
        {"file": "runes.json", "name": "Nordic Runes", "key": "runes"},
        {"file": "iching.json", "name": "I-Ching", "key": "hexagrams"},
        {"file": "omens.json", "name": "Folk Omen", "key": "signs"},
        {"file": "crystals.json", "name": "Lithotherapy", "key": "stones"},
        {"file": "horoscopes_extended.json", "name": "Planetary Transit", "key": "aspects"}
    ]
    
    selected = random.choice(systems)
    data = load_system(selected["file"])
    
    if not data:
        return "🔮 ARCANE SYSTEM: Void (Data not found). Focus on inner silence."

    # Handle both dict and list structures
    if isinstance(data, dict):
        items = data.get(selected["key"], [])
    else:
        items = data # Assume it is a list already

    if not items:
        return f"🔮 ARCANE SYSTEM: {selected['name']} (Empty). Look at the sky."

    item = random.choice(items)
    
    # Formatting
    name = item.get("name", "Unknown")
    meaning = item.get("meaning", "Mystery")
    advice = item.get("advice", "Observe.")
    
    return f"🔮 **ARCANE SYSTEM: {selected['name']}**\n   💎 Symbol: {name}\n   📜 Meaning: {meaning}\n   ⚡ Advice: {advice}"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(get_arcane_prediction("AC", "13.02.2026", "12:00"))
    else:
        print(get_arcane_prediction(sys.argv[1], sys.argv[2], sys.argv[3]))