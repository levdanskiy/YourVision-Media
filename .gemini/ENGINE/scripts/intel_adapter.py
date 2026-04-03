#!/usr/bin/env python3
import json
import os
import sys

DATA_PATH = "/home/levdanskiy/.gemini/ENGINE/repos/EurovisionDataset/dataset/eurovision.json"

class IntelAdapter:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(DATA_PATH):
            return []
        with open(DATA_PATH, 'r') as f:
            return json.load(f)

    def get_country_stats(self, country_code):
        """Возвращает реальную статистику страны"""
        wins = 0
        participations = 0
        qualifications = 0
        semis_participated = 0

        for contest in self.data:
            year = contest.get('year', 0)
            
            # Ищем во всех раундах
            for rnd in contest.get('rounds', []):
                for p in rnd.get('performances', []):
                    # В датасете страны могут быть по кодам или именам. 
                    # Здесь упрощенная логика, требующая доработки под маппинг кодов.
                    # Предполагаем, что запрос идет по коду (SE, UA, IT)
                    
                    # В этом датасете нет кода страны в performance, он есть в contestantId -> contestants
                    # Это сложная связь. Для скорости я сделаю прямой поиск по contestantId, если он доступен.
                    # Но для надежности лучше считать общие тренды.
                    pass 
        
        # Временное решение: Возвращаем данные из real_analytics logic
        return {"status": "Integration in progress", "message": "Use specific calculation methods"}

    def get_semifinal_advantage(self):
        """Возвращает точный % преимущества 2-й половины"""
        fh, sh = 0, 0
        fh_q, sh_q = 0, 0
        
        for contest in self.data:
            if contest.get('year', 0) < 2008: continue
            for rnd in contest.get('rounds', []):
                if rnd.get('name') in ['semifinal1', 'semifinal2']:
                    parts = rnd.get('performances', [])
                    mid = len(parts) / 2
                    for p in parts:
                        if p.get('running', 0) <= mid:
                            fh += 1
                            if p.get('place', 99) <= 10: fh_q += 1
                        else:
                            sh += 1
                            if p.get('place', 99) <= 10: sh_q += 1
                            
        rate1 = (fh_q / fh * 100) if fh else 0
        rate2 = (sh_q / sh * 100) if sh else 0
        return round(rate2 - rate1, 2)

if __name__ == "__main__":
    adapter = IntelAdapter()
    print(json.dumps({
        "semifinal_advantage": adapter.get_semifinal_advantage()
    }, indent=4))