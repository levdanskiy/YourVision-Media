#!/usr/bin/env python3
import arrow
import subprocess
import os
import json
import re

CORE_DIR = "/home/levdanskiy/.gemini/"
RADAR_FILE = os.path.join(CORE_DIR, "CORE/knowledge/global_event_radar.json")
YV_FILE = os.path.join(CORE_DIR, "TIMELINE/database/yv_live.json")

def get_current_plan_content():
    raw_date = subprocess.check_output(['date', '+%d.%m']).decode('utf-8').strip()
    plan_path = os.path.join(CORE_DIR, f"TIMELINE/daily_workflow/daily_plan_{raw_date}.md")
    if os.path.exists(plan_path):
        with open(plan_path, 'r') as f:
            return f.read()
    return ""

def check_pulse():
    now = arrow.now()
    today_str = now.format('DD.MM')
    plan_content = get_current_plan_content()
    
    print(f"--- 🕒 CHRONOS PULSE V10.0 (Total Context Awareness) ---")
    print(f"REAL TIME: {now.format('DD.MM.YYYY HH:mm:ss')}")
    
    # 1. MARKET DATA
    m_file = os.path.join(CORE_DIR, "ENGINE/feeds/market_data.json")
    if os.path.exists(m_file):
        with open(m_file, 'r') as f:
            m = json.load(f)
            print(f"💰 GOLD PRICE: ${m.get('Gold', 'N/A')}")

    # 2. EVENT RADAR
    all_events = []
    
    # Load YV Events
    if os.path.exists(YV_FILE):
        with open(YV_FILE, 'r') as f:
            yv = json.load(f)
            for e in yv.get('master_calendar', []):
                if e['status'] == 'pending':
                    all_events.append({"cat": "🎤 YV", "name": e['event'], "date": e['date']})

    # Load Global Events
    if os.path.exists(RADAR_FILE):
        with open(RADAR_FILE, 'r') as f:
            radar = json.load(f)
            for e in radar.get('events', []):
                if e['status'] in ['pending', 'ongoing']:
                    icon = "🏆" if e['category'] == "Sport" else "🎭" if e['category'] == "Culture" else "🎬" if e['category'] == "Cinema" else "📅"
                    all_events.append({"cat": f"{icon} {e['category'].upper()}", "name": e['name'], "date": e['date']})

    print("\n🌍 UPCOMING GLOBAL EVENTS:")
    proposed_extras = []
    
    for e in sorted(all_events, key=lambda x: x['date'])[:6]:
        print(f"   🔹 [{e['cat']}] {e['date']}: {e['name']}")
        
        # Logic: If event date matches today AND name not in plan -> Propose Extra
        if e['date'] == today_str and e['name'].lower() not in plan_content.lower():
            proposed_extras.append(e)

    if proposed_extras:
        print("\n🚨 PROPOSED EXTRAS (Not in current plan!):")
        for extra in proposed_extras:
            print(f"   🔴 EXTRA: {extra['name']} ({extra['cat']})")

    print("-------------------------------------------------")

if __name__ == "__main__":
    check_pulse()