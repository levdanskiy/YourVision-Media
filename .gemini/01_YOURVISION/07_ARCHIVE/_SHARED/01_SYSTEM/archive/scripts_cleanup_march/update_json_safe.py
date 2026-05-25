import json

file_path = '.gemini/TIMELINE/database/yv_season_2026.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading: {e}")
    exit(1)

updates = {
    "AL": {"name": "Албания", "artist": "Alis", "song": "Nân"},
    "AT": {"name": "Австрия", "artist": "COSMȮ", "song": "TANZSCHEIN"},
    "BE": {"name": "Бельгия", "artist": "Essyla", "song": "Dancing on the ice"},
    "BG": {"name": "Болгария", "artist": "Dara", "song": "Bangaranga"},
    "CY": {"name": "Кипр", "artist": "Antigoni", "song": "JALLA"},
    "DK": {"name": "Дания", "artist": "Søren Torpegaard Lund", "song": "Før Vi Går Hjem"},
    "ES": {"name": "Испания", "artist": "Tony Grox y LUCYCALYS", "song": "T AMARÉ"},
    "FI": {"name": "Финляндия", "artist": "Linda Lampenius & Pete Parkkonen", "song": "Liekinheitin"},
    "HR": {"name": "Хорватия", "artist": "LELEK", "song": "Andromeda"},
    "LT": {"name": "Литва", "artist": "Lion Ceccah", "song": "Sólo Quiero Más"},
    "LV": {"name": "Латвия", "artist": "Atvara", "song": "Ēnā"},
    "ME": {"name": "Черногория", "artist": "Tamara Živković", "song": "Nova Zora"},
    "NO": {"name": "Норвегия", "artist": "JONAS LOVV", "song": "Ya Ya Ya"},
    "RS": {"name": "Сербия", "artist": "Lavina", "song": "Kraj mene"},
    "UA": {"name": "Украина", "artist": "Lelėka", "song": "Ridnym"}
}

# Update countries safely
for code, info in updates.items():
    if code not in data["countries"]:
        data["countries"][code] = {"name": info["name"]}
    
    data["countries"][code]["artist"] = info["artist"]
    data["countries"][code]["song"] = info["song"]
    
    if "winners" not in data:
        data["winners"] = {}
        
    data["winners"][code] = {
        "country_name": info["name"],
        "artist": info["artist"],
        "song": info["song"]
    }

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Safely updated JSON")
