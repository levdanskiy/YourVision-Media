#!/usr/bin/env python3
import json
import sys

VOICE_CONFIG = {
    "ARCHITECT": {
        "markers": ["структура", "ось", "цикл", "закон", "фундамент", "тектоника"],
        "forbidden": ["кухня", "шепот", "миленький", "!"],
        "target_avg_sentence": 12
    },
    "TRAVELER": {
        "markers": ["запах", "корни", "обряд", "земля", "память", "шепот"],
        "forbidden": ["алгоритм", "биткоин", "криптовалюта"],
        "target_avg_sentence": 18
    },
    "ALCHEMIST": {
        "markers": ["хруст", "велюр", "ганаш", "текстура", "алхимия", "разлом"],
        "forbidden": ["люди", "дети", "архитектор", "война"],
        "target_avg_sentence": 15
    },
    "INSIDER": {
        "markers": ["хайп", "котировки", "релиз", "чарт", "инсайд", "балл"],
        "forbidden": ["праздник", "тишина", "архитектура"],
        "target_avg_sentence": 14
    }
}

def check_voice(text, persona):
    text = text.lower()
    config = VOICE_CONFIG.get(persona.upper(), {})
    
    found_markers = [m for m in config.get('markers', []) if m in text]
    found_forbidden = [f for f in config.get('forbidden', []) if f in text]
    
    score = len(found_markers) * 20 - len(found_forbidden) * 50
    
    return {
        "score": max(0, min(100, score + 50)),
        "integrity": "High" if score > 40 else "Low",
        "warnings": found_forbidden,
        "status": "Validated (Russian Only)"
    }

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(json.dumps(check_voice(sys.argv[1], sys.argv[2]), indent=4, ensure_ascii=False))