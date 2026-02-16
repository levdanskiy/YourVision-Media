#!/usr/bin/env python3
import json
import sys
import os

DB_PATH = "/home/levdanskiy/.gemini/TIMELINE/database/yv_live.json"

def get_country_info(country):
    if not os.path.exists(DB_PATH):
        return "❌ Error: Database not found."
        
    with open(DB_PATH, 'r') as f:
        data = json.load(f)
        
    country_data = data.get('detailed_database', {}).get(country.upper())
    if country_data:
        return json.dumps(country_data, indent=2, ensure_ascii=False)
    else:
        return f"❓ No data found for {country}."

def get_upcoming_events(limit=5):
    if not os.path.exists(DB_PATH):
        return []
        
    with open(DB_PATH, 'r') as f:
        data = json.load(f)
        
    calendar = data.get('master_calendar', [])
    pending = [e for e in calendar if e.get('status') == 'pending']
    return pending[:limit]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_yv_database.py [COUNTRY | upcoming]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "upcoming":
        events = get_upcoming_events()
        for e in events:
            print(f"📅 {e['date']}: {e['event']}")
    else:
        print(get_country_info(cmd))
