#!/usr/bin/env python3
import requests
import json
import sys

def get_weather(city):
    try:
        # Increased timeout and added a fallback to a simpler format
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            curr = data['current_condition'][0]
            return {
                "temp": curr['temp_C'],
                "desc": curr['weatherDesc'][0]['value'],
                "humidity": curr['humidity'],
                "wind": curr['windspeedKmph'],
                "city": city
            }
    except Exception:
        pass
    
    # Fallback simulation based on seasonal climate if API fails
    return {
        "temp": "Unknown",
        "desc": "Climate data unavailable",
        "humidity": "N/A",
        "wind": "N/A",
        "city": city
    }

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Riga"
    print(json.dumps(get_weather(city), indent=4))