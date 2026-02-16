import datetime

def create_ics(events, filename):
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Almanac System//Glossy Intelligence//EN",
        "X-WR-CALNAME:Almanac Main",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]
    
    for event in events:
        start_time = event['start'].strftime("%Y%m%dT%H%M%S")
        end_time = (event['start'] + datetime.timedelta(minutes=30)).strftime("%Y%m%dT%H%M%S")
        
        ics_content.extend([
            "BEGIN:VEVENT",
            f"DTSTART:{start_time}",
            f"DTEND:{end_time}",
            f"SUMMARY:{event['summary']}",
            f"DESCRIPTION:{event['description']}",
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
            "BEGIN:VALARM",
            "TRIGGER:-PT15M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Reminder",
            "END:VALARM",
            "END:VEVENT"
        ])
    
    ics_content.append("END:VCALENDAR")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(ics_content))

# Пример данных для теста (30.01)
test_events = [
    {
        "start": datetime.datetime(2026, 1, 30, 9, 0),
        "summary": "🏛️ #GREETING: Три Святителя",
        "description": "Layer: Total Glossy Intelligence\nArcane: The Hierophant\nWeather: Sofia/Paris Sync\nTexture: White Wool"
    },
    {
        "start": datetime.datetime(2026, 1, 30, 12, 0),
        "summary": "📜 #HOLIDAY_HISTORY: Три Ієрархи",
        "description": "Layer: Historical Depth\nAstro: Nakshatra Analysis\nLore: Wiki Lore Sync"
    }
]

create_ics(test_events, "/home/levdanskiy/.gemini/TIMELINE/Almanac_Main_Test.ics")
