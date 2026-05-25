#!/usr/bin/env python3
import sys

def build_post(subject, experts):
    """
    experts = [{"name": "...", "type": "AUTHOR/READER", "feedback": "...", "prediction": "..."}]
    """
    ru = f"🗣 **ЭКСПЕРТНЫЙ РЕЗОНАНС: {subject.upper()}**\n\n"
    ru += "Мы прогнали эту заявку через фильтры наших авторов и самых опытных слушателей YourVision. Истинный пульс здесь.\n\n"
    
    for e in experts:
        label = "🛡 INSIDER" if e['type'].upper() == "AUTHOR" else "👁 COMMUNITY"
        ru += f"{label} | {e['name']}\n"
        ru += f"«{e['feedback']}»\n"
        ru += f"📉 Прогноз: {e['prediction']}\n\n"
    
    ru += "#YourVision #Eurovision2026 #ExpertOpinion"
    
    # В будущем здесь будет UA-блок
    print(ru)

if __name__ == "__main__":
    # Пример структуры данных для вызова
    test_subject = "Norway: Electric Pulse"
    test_experts = [
        {"name": "Маркус", "type": "AUTHOR", "feedback": "Слишком много индастриала, жюри не оценит, но телевоут взорвется.", "prediction": "TOP-5"},
        {"name": "Digger2026", "type": "READER", "feedback": "Вайб 2016-го, но очень качественно. Хочется переслушать.", "prediction": "12-15 место"}
    ]
    build_post(test_subject, test_experts)
