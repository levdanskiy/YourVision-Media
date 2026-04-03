import json
import re

# 1. Update JSON
file_path = '.gemini/TIMELINE/database/yv_season_2026.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading JSON: {e}")
    exit(1)

# Check if IL event exists, update time. If not, add it.
il_found = False
for e in data['events']:
    if e['country'] == 'IL' and e['date'] == '2026-03-05':
        e['time'] = '20:30'
        e['event'] = 'Специальная трансляция презентации песни Noam Bettan (с участием Yuval Raphael и Eden Golan)'
        il_found = True
        break

if not il_found:
    data['events'].append({
        "id": "EVT_IL_SONG", 
        "date": "2026-03-05", 
        "time": "20:30", 
        "country": "IL", 
        "country_name": "Израиль", 
        "event": "Специальная трансляция презентации песни Noam Bettan (с участием Yuval Raphael и Eden Golan)", 
        "type": "RELEASE", 
        "status": "CONFIRMED", 
        "link": "https://www.kan.org.il/"
    })

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update Live Calendar
cal_path = '.gemini/KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md'
with open(cal_path, 'r', encoding='utf-8') as f:
    cal_content = f.read()

cal_content = re.sub(r'05\.03 🇮🇱 \*\*Израиль\*\*: Релиз песни Noam Bettan', '05.03 🇮🇱 **Израиль**: Релиз песни Noam Bettan (20:30)', cal_content)

with open(cal_path, 'w', encoding='utf-8') as f:
    f.write(cal_content)

# 3. Update Master Plan
plan_path = '.gemini/TIMELINE/master_plans/03/YV_Plan_03.md'
with open(plan_path, 'r', encoding='utf-8') as f:
    plan_content = f.read()

# Add IL release to 05.03 if it exists, or create the block
if '### 05.03 (Чт)' not in plan_content:
    plan_content = plan_content.replace(
        '### 06.03 (Пт)',
        '### 05.03 (Чт) — ISRAEL REVEAL & SM SF2\n* 20:30 | **YV** | ⚡ **#NEWS_WIRE:** Израиль. Релиз песни Noam Bettan. - ⬜ [ОЖИДАНИЕ]\n* 22:05 | **YV** | ⚡ **#NEWS_WIRE:** Сан-Марино. Второй полуфинал. - ⬜ [ОЖИДАНИЕ]\n\n### 06.03 (Пт)'
    )

with open(plan_path, 'w', encoding='utf-8') as f:
    f.write(plan_content)

print("Israel Sync Complete.")
