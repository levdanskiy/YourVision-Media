#!/usr/bin/env python3
import sys

def build_expert_post(song_name, experts_data):
    """
    experts_data = [
        {"name": "Имя", "role": "Звук", "opinion": "текст", "score": "8/10"},
        ...
    ]
    """
    ru_text = f"🗣 **ЭКСПЕРТНЫЙ РЕЗОНАНС: {song_name.upper()}**\n\n"
    ru_text += "Мы собрали мнения нашего закрытого пула экспертов. Разброс мнений критический. Читайте между строк.\n\n"
    
    for exp in experts_data:
        ru_text += f"{exp['role'].upper()} | {exp['name']}\n"
        ru_text += f"«{exp['opinion']}»\n"
        ru_text += f"📊 Вердикт: {exp['score']}\n\n"
    
    # Здесь я добавлю автоматический перевод на UA в будущем
    print(ru_text)

if __name__ == "__main__":
    # Пример вызова
    sample_data = [
        {"name": "Маркус", "role": "Продюсер", "opinion": "Слишком много компрессии в припеве, но хук убойный.", "score": "9/10"},
        {"name": "Стефан", "role": "Аналитик", "opinion": "Букмекеры верят, но сетка полуфинала может его сожрать.", "score": "7/10"}
    ]
    build_expert_post("Norway: Electric Pulse", sample_data)
