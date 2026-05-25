#!/usr/bin/env python3
import json
import swisseph as swe
from datetime import datetime

class GodEyeCore:
    def __init__(self, lat=48.2082, lon=16.3738):
        self.lat = lat
        self.lon = lon

    def get_celestial_data(self, date_str):
        d = datetime.strptime(date_str, "%d.%m.%Y")
        julian_day = swe.julday(d.year, d.month, d.day, 12.0)
        
        # Получаем данные. calc_ut возвращает (values, flags)
        # где values - это кортеж из 6 элементов.
        sun_res, _ = swe.calc_ut(julian_day, swe.SUN)
        moon_res, _ = swe.calc_ut(julian_day, swe.MOON)
        
        # Первая координата - это долгота (float)
        sun_long = float(sun_res[0])
        moon_long = float(moon_res[0])
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        return {
            "sun_degree": round(sun_long % 30, 2),
            "sun_sign": signs[int(sun_long / 30)],
            "moon_degree": round(moon_long % 30, 2),
            "moon_sign": signs[int(moon_long / 30)]
        }

if __name__ == "__main__":
    core = GodEyeCore()
    try:
        print(json.dumps(core.get_celestial_data("30.01.2026"), indent=4))
    except Exception as e:
        print(json.dumps({"error": str(e), "type": str(type(e))}))