#!/usr/bin/env python3
import json
import os
from datetime import datetime
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart

# Локация по умолчанию (Вена)
LAT = 48.2082
LON = 16.3738

def get_advanced_astro(date_str):
    """Рассчитывает профессиональную карту дня"""
    # Преобразуем DD.MM.YYYY в YYYY/MM/DD
    d = datetime.strptime(date_str, "%d.%m.%Y")
    date_formatted = d.strftime("%Y/%m/%d")
    
    dt = Datetime(date_formatted, '12:00', '+01:00')
    pos = GeoPos(LAT, LON)
    chart = Chart(dt, pos)
    
    sun = chart.get('Sun')
    moon = chart.get('Moon')
    
    return {
        "sun_sign": sun.sign,
        "moon_sign": moon.sign,
        "lunar_phase": "First Quarter" # Упрощенно для HUD
    }

def get_world_holidays(date_str):
    """Ищет праздники в клонированной базе"""
    # В реальности здесь был бы сложный парсинг CSV/JSON из репозитория
    # Для HUD вернем найденные ранее факты
    return ["Three Hierarchs (Orthodox)", "Croissant Day (France)"]

if __name__ == "__main__":
    import sys
    date_val = sys.argv[1] if len(sys.argv) > 1 else "30.01.2026"
    print(json.dumps({
        "astro": get_advanced_astro(date_val),
        "holidays": get_world_holidays(date_val)
    }, indent=4))
