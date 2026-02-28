#!/usr/bin/env python3
import json
import os

DATA_PATH = "/home/levdanskiy/.gemini/ENGINE/repos/EurovisionDataset/dataset/eurovision.json"

def calculate_semifinal_stats():
    if not os.path.exists(DATA_PATH):
        return {"error": "Dataset not found"}

    with open(DATA_PATH, 'r') as f:
        data = json.load(f)

    first_half_qualifiers = 0
    first_half_total = 0
    second_half_qualifiers = 0
    second_half_total = 0

    # Проходим по всем годам
    for contest in data:
        year = contest.get('year', 0)
        if year < 2008: continue # Анализируем эру двух полуфиналов

        rounds = contest.get('rounds', [])
        
        for rnd in rounds:
            # Ищем полуфиналы
            if rnd.get('name') not in ['semifinal1', 'semifinal2']:
                continue
            
            performances = rnd.get('performances', [])
            total_participants = len(performances)
            if total_participants == 0: continue
            
            midpoint = total_participants / 2

            for p in performances:
                running_order = p.get('running', 0)
                place = p.get('place', 99) # Если места нет, считаем что не прошел
                
                # Квалификация: место <= 10
                qualified = place <= 10

                if running_order <= midpoint:
                    first_half_total += 1
                    if qualified: first_half_qualifiers += 1
                else:
                    second_half_total += 1
                    if qualified: second_half_qualifiers += 1

    # Расчет процентов
    rate_1 = (first_half_qualifiers / first_half_total * 100) if first_half_total > 0 else 0
    rate_2 = (second_half_qualifiers / second_half_total * 100) if second_half_total > 0 else 0

    return {
        "stat_period": "2008-2024",
        "first_half_qualification_rate": round(rate_1, 2),
        "second_half_qualification_rate": round(rate_2, 2),
        "advantage": round(rate_2 - rate_1, 2)
    }

if __name__ == "__main__":
    print(json.dumps(calculate_semifinal_stats(), indent=4))