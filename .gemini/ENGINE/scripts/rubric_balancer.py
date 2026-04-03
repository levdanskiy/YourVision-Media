import os
import re
from datetime import datetime, timedelta

def get_history():
    history = []
    base_dir = ".gemini/CONTENT/almanac/"
    # Собираем все посты за последние 5 дней
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                # Извлекаем дату и рубрику из имени файла (например, AL-01.04-18-00-BAKERY...)
                match = re.search(r"AL-(\d{2}\.\d{2}).*?-(BAKERY|LORE|LISTS|CHRONOS)", file)
                if match:
                    history.append({"date": match.group(1), "rubric": match.group(2)})
    return history

def analyze():
    history = get_history()
    # Сортируем по дате (упрощенно)
    history.sort(key=lambda x: x["date"], reverse=True)
    
    last_rubrics = [h["rubric"] for h in history[:2]]
    all_rubrics = ["BAKERY", "LORE", "LISTS", "CHRONOS"]
    
    available = [r for r in all_rubrics if r not in last_rubrics]
    
    print("\n⚖️  БАЛАНС РУБРИК АЛЬМАНАХА:")
    print("-" * 40)
    print(f"Последние использованные: {', '.join(last_rubrics)}")
    print(f"РЕКОМЕНДОВАНЫ ДЛЯ СЛЕДУЮЩЕГО ПЛАНА: {', '.join(available)}")
    print("-" * 40)

if __name__ == "__main__":
    analyze()
