#!/usr/bin/env python3
import os
import sys

# Расширенный двуязычный маппинг
KEYWORDS = {
    "AC": ["SCIENCE", "LOGIC", "PHILOSOPHY", "INTELLECT", "HISTORY", "RADIO", "SPACE", "НАУКА", "ЛОГИКА", "ФИЛОСОФИЯ", "ПАМЯТЬ", "ЗНАНИЯ"],
    "NB": ["NATION", "CITY", "ETHNO", "COUNTRY", "FESTIVAL", "TRADITION", "СУРОК", "ГОРОД", "СТРАНА", "ЭТНО", "ТРАДИЦИЯ", "КИТАЙ", "УЭЛЬС", "ШОТЛАНДИЯ"],
    "SW": ["FOOD", "DRINK", "SWEET", "TASTE", "INGREDIENT", "CHOCOLATE", "NUTELLA", "WINE", "CAKE", "ЕДА", "ВКУС", "ШОКОЛАД", "ВИНО", "ТОРТ", "ДЕСЕРТ", "ПИРОГ"]
}

def get_recommendation(holiday_name):
    h = holiday_name.upper()
    
    # Сначала проверяем на прямое вхождение ключевых слов
    for channel, keys in KEYWORDS.items():
        for key in keys:
            if key in h:
                return channel
                
    return "AC" # Базовый канал для неопределенных дат

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 balance_greetings.py 'Название праздника'")
        sys.exit(1)
        
    holiday = sys.argv[1]
    recommendation = get_recommendation(holiday)
    
    print(f"🎯 ПРАЗДНИК: {holiday}")
    print(f"🚀 КАНАЛ: {recommendation}")

if __name__ == "__main__":
    main()
