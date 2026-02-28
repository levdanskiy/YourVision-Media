# ⚖️ MASTER BALANCER V2.1 (SOUL & TRADITION)
# Распределение рубрик для концепции V2.0

ROSTER = {
    "AC": ["#TIME_WHEEL", "#SACRED_PERSON", "#SYMBOL_CODE", "#RITUAL_KEY", "#ART_SOUL"],
    "NB": ["#PLACE_OF_POWER", "#TRADITION_KEEPER", "#FOLK_LEGEND", "#COSTUME_CODE", "#VISUAL_ESCAPE"],
    "SW": ["#SIGNATURE_CAKE", "#SEASON_TASTE", "#VINTAGE_BAKE", "#CHOCOLATE_RITUAL", "#COZY_DRINK"]
}

def get_balanced_rubric(channel, slot_time):
    # Приоритет: Торты для SW утром
    if channel == "SW" and slot_time == "10:00":
        return "#SIGNATURE_CAKE"
    
    # Приоритет: Колесо Года для AC утром
    if channel == "AC" and slot_time in ["08:00", "08:30", "09:00"]:
        return "#TIME_WHEEL"

    # Приоритет: Легенды для NB вечером
    if channel == "NB" and slot_time == "21:30":
        return "#FOLK_LEGEND"

    # В остальных случаях — ротация
    import random
    return random.choice(ROSTER.get(channel, ["#GENERAL"]))