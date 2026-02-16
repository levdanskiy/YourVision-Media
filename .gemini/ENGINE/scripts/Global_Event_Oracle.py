#!/usr/bin/env python3
import sys
import json
from datetime import datetime

class GlobalEventOracle:
    def __init__(self):
        # Расширенная база данных с категоризацией
        self.master_db = {
            "03.02": {
                "STATE": ["День освобождения (Вьетнам)", "День героев (Мозамбик)"],
                "SACRED": ["День святого Власия (Праздник горла)", "Сетсубун (Финальные обряды, Япония)"],
                "GEEK": ["День морковного торта (Geek/Gastro)", "Годовщина основания SoftBank"],
                "CULTURE": ["The Day the Music Died (Память Бадди Холли, Ричи Валенса)"],
                "WEIRD": ["День золотистого ретривера", "День кормления птиц", "День 'Работайте голышом' (Work Naked Day - да, это существует)"]
            },
            "04.02": {
                "STATE": ["День Независимости Шри-Ланки"],
                "SACRED": ["Праздник начала весны (Личунь, Китай)"],
                "GEEK": ["Всемирный день борьбы против рака (Science/Global)", "День создания Facebook (2004)"],
                "CULTURE": ["День рождения Джорджа Пойи (Математика)"],
                "WEIRD": ["День домашнего супа", "День вакуумного пакета"]
            }
        }
        
    def get_all_events(self, date_str):
        key = date_str[:5]
        events = self.master_db.get(key, {
            "STATE": ["Standard Int. Day"],
            "SACRED": ["Solar Alignment"],
            "GEEK": ["Tech Pulse Check"],
            "CULTURE": ["World Heritage Moment"],
            "WEIRD": ["Day of Unexpected Insights"]
        })
        
        return {
            "date": date_str,
            "categories": events,
            "synergy_level": "High" if key in self.master_db else "Normal"
        }

if __name__ == "__main__":
    date_input = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%d.%m.%Y")
    oracle = GlobalEventOracle()
    print(json.dumps(oracle.get_all_events(date_input), indent=4))