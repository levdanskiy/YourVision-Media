#!/usr/bin/env python3
import sys
import holidays
from datetime import datetime

def get_global_holidays(date_str=None):
    if date_str:
        dt = datetime.strptime(date_str, "%d.%m.%Y")
    else:
        dt = datetime.now()
    
    # Список стран для мониторинга (можно расширять)
    countries = ["UA", "RU", "US", "DE", "FR", "JP", "NO", "SE", "IL"]
    found = []
    
    for country in countries:
        country_holidays = holidays.CountryHoliday(country)
        name = country_holidays.get(dt)
        if name:
            found.append(f"{country}: {name}")
            
    return found

if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    results = get_global_holidays(date_arg)
    if results:
        print("\n".join(results))
    else:
        print("No official holidays found for this date in monitored countries.")
