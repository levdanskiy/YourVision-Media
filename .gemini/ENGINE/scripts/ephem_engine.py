#!/usr/bin/env python3
import json
import datetime
import math

def get_moon_phase(date_obj):
    """Рассчитывает точную фазу Луны (0-100%)"""
    diff = date_obj - datetime.datetime(2001, 1, 1)
    days = diff.total_seconds() / 86400
    lunations = 0.20439731 + (days * 0.03386319269)
    phase = lunations % 1.0
    return round(phase * 100, 2)

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(json.dumps({
        "moon_illumination": f"{get_moon_phase(now)}%",
        "solar_cycle": "Winter Transition"
    }, indent=4))
