import json

file_path = '.gemini/TIMELINE/database/yv_season_2026.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading: {e}")
    exit(1)

# Correct 35 countries list
correct_countries = {
    "AL": {"name": "Албания", "artist": "Alis", "song": "Nân", "time": "03:09"},
    "AM": {"name": "Армения", "artist": "TBA", "song": "TBA"},
    "AU": {"name": "Австралия", "artist": "Delta Goodrem", "song": "Eclipse", "time": "03:00"},
    "AT": {"name": "Австрия", "artist": "COSMȮ", "song": "TANZSCHEIN", "time": "02:42"},
    "AZ": {"name": "Азербайджан", "artist": "TBA", "song": "TBA"},
    "BE": {"name": "Бельгия", "artist": "Essyla", "song": "Dancing on the ice", "time": "03:08"},
    "BG": {"name": "Болгария", "artist": "Dara", "song": "Bangaranga", "time": "02:58"},
    "HR": {"name": "Хорватия", "artist": "LELEK", "song": "Andromeda", "time": "03:00"},
    "CY": {"name": "Кипр", "artist": "Antigoni", "song": "JALLA", "time": "03:00"},
    "CZ": {"name": "Чехия", "artist": "TBA", "song": "TBA"},
    "DK": {"name": "Дания", "artist": "Søren Torpegaard Lund", "song": "Før Vi Går Hjem", "time": "02:54"},
    "EE": {"name": "Эстония", "artist": "Vanilla Ninja", "song": "Too Epic To Be True", "time": "02:59"},
    "FI": {"name": "Финляндия", "artist": "Linda Lampenius & Pete Parkkonen", "song": "Liekinheitin", "time": "03:00"},
    "FR": {"name": "Франция", "artist": "TBA", "song": "TBA"},
    "GE": {"name": "Грузия", "artist": "Bzikebi", "song": "TBA"},
    "DE": {"name": "Германия", "artist": "Sarah Engels", "song": "Fire", "time": "02:57"},
    "GR": {"name": "Греция", "artist": "Akylas", "song": "Ferto", "time": "03:00"},
    "IL": {"name": "Израиль", "artist": "Noam Bettan", "song": "TBA"},
    "IT": {"name": "Италия", "artist": "Sal Da Vinci", "song": "Per sempre sì", "time": "02:55"},
    "LV": {"name": "Латвия", "artist": "Atvara", "song": "Ēnā", "time": "02:53"},
    "LT": {"name": "Литва", "artist": "Lion Ceccah", "song": "Sólo Quiero Más", "time": "03:02"},
    "LU": {"name": "Люксембург", "artist": "Eva Marija", "song": "Mother Nature", "time": "02:58"},
    "MT": {"name": "Мальта", "artist": "AIDAN", "song": "Bella", "time": "02:57"},
    "MD": {"name": "Молдова", "artist": "Satoshi", "song": "Viva, Moldova!", "time": "02:40"},
    "ME": {"name": "Черногория", "artist": "Tamara Živković", "song": "Nova Zora", "time": "02:47"},
    "NO": {"name": "Норвегия", "artist": "JONAS LOVV", "song": "Ya Ya Ya", "time": "02:49"},
    "PL": {"name": "Польша", "artist": "TBA", "song": "TBA"},
    "PT": {"name": "Португалия", "artist": "TBA", "song": "TBA"},
    "RO": {"name": "Румыния", "artist": "TBA", "song": "TBA"},
    "SM": {"name": "Сан-Марино", "artist": "TBA", "song": "TBA"},
    "RS": {"name": "Сербия", "artist": "Lavina", "song": "Kraj mene", "time": "03:01"},
    "SE": {"name": "Швеция", "artist": "TBA", "song": "TBA"},
    "CH": {"name": "Швейцария", "artist": "Veronica Fusaro", "song": "TBA"},
    "UA": {"name": "Украина", "artist": "Lelėka", "song": "Ridnym", "time": "02:58"},
    "GB": {"name": "Великобритания", "artist": "TBA", "song": "Ein Zwei Drei"}
}

data["countries"] = correct_countries

winners = {}
for code, info in correct_countries.items():
    if info["artist"] != "TBA" and info["song"] != "TBA":
        winners[code] = {
            "country_name": info["name"],
            "artist": info["artist"],
            "song": info["song"]
        }

data["winners"] = winners

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON completely fixed")
