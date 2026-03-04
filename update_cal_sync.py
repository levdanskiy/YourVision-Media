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

new_events = [
    {"id": "EVT_AZ_REV", "date": "2026-03-06", "time": "16:00", "country": "AZ", "country_name": "Азербайджан", "event": "Объявление представителя", "type": "RELEASE", "status": "CONFIRMED", "link": ""},
    {"id": "EVT_CZ_ART", "date": "2026-03-08", "time": "21:00", "country": "CZ", "country_name": "Чехия", "event": "Объявление представителя", "type": "RELEASE", "status": "CONFIRMED", "link": ""},
    {"id": "EVT_PL_RES", "date": "2026-03-08", "time": "11:00", "country": "PL", "country_name": "Польша", "event": "Объявление результатов отбора", "type": "FINAL", "status": "CONFIRMED", "link": ""},
    {"id": "EVT_CZ_SONG", "date": "2026-03-11", "time": "21:00", "country": "CZ", "country_name": "Чехия", "event": "Презентация песни", "type": "RELEASE", "status": "CONFIRMED", "link": ""},
    {"id": "EVT_CH_SONG", "date": "2026-03-11", "time": "13:00", "country": "CH", "country_name": "Швейцария", "event": "Релиз песни Veronica Fusaro", "type": "RELEASE", "status": "CONFIRMED", "link": ""}
]

# remove old CZ and CH entries if they lack time or are duplicates
data['events'] = [e for e in data['events'] if not (e['country'] == 'CZ' and e['date'] == '2026-03-08')]
data['events'] = [e for e in data['events'] if not (e['country'] == 'CH' and e['date'] == '2026-03-11')]

data['events'].extend(new_events)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update Live Calendar
cal_path = '.gemini/KNOWLEDGE/Live_Calendars/YV_ESC_Live_Calendar.md'
with open(cal_path, 'r', encoding='utf-8') as f:
    cal_content = f.read()

# Replace specific lines
cal_content = re.sub(r'06\.03 🇬🇧 \*\*Великобритания\*\*: Премьера песни «Ein Zwei Drei» \(10:00\)', '06.03 🇬🇧 **Великобритания**: Премьера песни «Ein Zwei Drei» (10:00)\n06.03 🇦🇿 **Азербайджан**: Объявление представителя (16:00)', cal_content)
cal_content = re.sub(r'08\.03 🇨🇿 \*\*Чехия\*\*: Презентация участника и песни \(TBA\)', '08.03 🇵🇱 **Польша**: Объявление результатов отбора (11:00)\n08.03 🇨🇿 **Чехия**: Объявление представителя (21:00)', cal_content)
cal_content = re.sub(r'11\.03 🇨🇭 \*\*Швейцария\*\*: Релиз песни Veronica Fusaro', '11.03 🇨🇭 **Швейцария**: Релиз песни Veronica Fusaro (13:00)\n11.03 🇨🇿 **Чехия**: Презентация конкурсной песни (21:00)', cal_content)

with open(cal_path, 'w', encoding='utf-8') as f:
    f.write(cal_content)

# 3. Update Master Plan
plan_path = '.gemini/TIMELINE/master_plans/03/YV_Plan_03.md'
with open(plan_path, 'r', encoding='utf-8') as f:
    plan_content = f.read()

plan_content = plan_content.replace(
    '### 06.03 (Пт) — UNITED KINGDOM REVEAL\n* 10:00 | **YV** | ⚡ **#NEWS_WIRE:** Великобритания. Премьера песни «Ein Zwei Drei». - ⬜ [ОЖИДАНИЕ]',
    '### 06.03 (Пт) — UK & AZERBAIJAN REVEAL\n* 10:00 | **YV** | ⚡ **#NEWS_WIRE:** Великобритания. Премьера песни «Ein Zwei Drei». - ⬜ [ОЖИДАНИЕ]\n* 16:00 | **YV** | ⚡ **#NEWS_WIRE:** Азербайджан. Объявление представителя. - ⬜ [ОЖИДАНИЕ]'
)

plan_content = plan_content.replace(
    '### 08.03 (Вс) — CZECHIA REVEAL\n* TBA | **YV** | ⚡ **#NEWS_WIRE:** Чехия. Презентация участника и песни. - ⬜ [ОЖИДАНИЕ]',
    '### 08.03 (Вс) — POLAND & CZECHIA REVEAL\n* 11:00 | **YV** | ⚡ **#NEWS_WIRE:** Польша. Объявление победителя отбора. - ⬜ [ОЖИДАНИЕ]\n* 21:00 | **YV** | ⚡ **#NEWS_WIRE:** Чехия. Объявление представителя. - ⬜ [ОЖИДАНИЕ]'
)

if '### 11.03 (Ср)' not in plan_content:
    plan_content = plan_content.replace(
        '### 10.03 (Вт) — CHART DAY: ALLMIX WOMEN POWER\n* 12:00 | **YV** | 🗳️ **#VOTING_CLOSE:** AllMix Women Power. - ⬜ [ОЖИДАНИЕ]\n* 18:00 | **YV** | 📻 **#RADIO_PREMIERE:** AllMix Women Power на радио. - ⬜ [ОЖИДАНИЕ]\n* 19:20 | **YV** | 📊 **#CHART_RESULTS:** AllMix Women Power (Итоги). - ⬜ [ОЖИДАНИЕ]',
        '### 10.03 (Вт) — CHART DAY: ALLMIX WOMEN POWER\n* 12:00 | **YV** | 🗳️ **#VOTING_CLOSE:** AllMix Women Power. - ⬜ [ОЖИДАНИЕ]\n* 18:00 | **YV** | 📻 **#RADIO_PREMIERE:** AllMix Women Power на радио. - ⬜ [ОЖИДАНИЕ]\n* 19:20 | **YV** | 📊 **#CHART_RESULTS:** AllMix Women Power (Итоги). - ⬜ [ОЖИДАНИЕ]\n\n### 11.03 (Ср) — RELEASES: CH & CZ\n* 13:00 | **YV** | ⚡ **#NEWS_WIRE:** Швейцария. Релиз песни Veronica Fusaro. - ⬜ [ОЖИДАНИЕ]\n* 21:00 | **YV** | ⚡ **#NEWS_WIRE:** Чехия. Презентация песни. - ⬜ [ОЖИДАНИЕ]'
    )

with open(plan_path, 'w', encoding='utf-8') as f:
    f.write(plan_content)

print("Calendar and Plans Synced.")
