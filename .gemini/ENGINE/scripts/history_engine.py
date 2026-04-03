import sys
import json
import os
from datetime import datetime

DB_PATH = ".gemini/TIMELINE/database/esc_history.json"

def load_db():
    if not os.path.exists(DB_PATH): return {}
    with open(DB_PATH, 'r') as f: return json.load(f)

def get_history(date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%m-%d")
    
    db = load_db()
    events = db.get(date_str, [])
    
    print(f"\n📜 **ON THIS DAY IN EUROVISION ({date_str})**")
    print("---")
    
    if not events:
        print("No historical records found for this date yet.")
        print("To add one, edit .gemini/TIMELINE/database/esc_history.json")
    else:
        for e in sorted(events, key=lambda x: x['year']):
            print(f"• **{e['year']}**: {e['event']} ({e.get('country', 'Europe')})")
    
    print("---\n")

if __name__ == "__main__":
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    get_history(target_date)
