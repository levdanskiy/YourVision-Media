#!/usr/bin/env python3
import sys
import re
import os

def get_daily_digest(channel, date, current_time):
    # Финальные слоты
    FINAL_SLOTS = {
        "AC": "21:00",
        "NB": "21:30",
        "SW": "20:00"
    }
    
    if current_time != FINAL_SLOTS.get(channel):
        return "" # Не финальный пост - нет футера

    plan_path = f".gemini/system/daily_plan_{date}.md"
    if not os.path.exists(plan_path):
        return ""

    with open(plan_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    digest = []
    section_found = False
    
    # Ищем секцию канала
    channel_markers = {
        "AC": "### 🏛️ ALMANAC (Main)",
        "NB": "### 🌍 ALMANAC: NEIGHBORS",
        "SW": "### 🍰 ALMANAC: SWEET"
    }
    
    marker = channel_markers.get(channel)
    
    for line in lines:
        if line.strip() == marker:
            section_found = True
            continue
        if section_found and line.startswith("### "): # Следующая секция
            break
        
        if section_found and line.strip().startswith("|"):
            # Парсим строку таблицы: | Время | Язык | Тема | Статус |
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 3 and ":" in parts[1]: # Это строка с временем
                time = parts[1].replace("`", "")
                topic_raw = parts[3].replace("**", "")
                # Очищаем тему от #TAG
                if "#" in topic_raw:
                    try:
                        tag, title = topic_raw.split(":", 1)
                        clean_title = f"{tag.strip()}: {title.strip()}"
                    except:
                        clean_title = topic_raw
                else:
                    clean_title = topic_raw
                
                # Не добавляем текущий пост в список "Ранее"
                if time != current_time:
                    digest.append(f"- {clean_title}")

    if not digest:
        return ""

    # Формируем красивый блок
    headers = {
        "AC": "👇 **АРХИТЕКТУРА ДНЯ** 👇",
        "NB": "👇 **МАРШРУТ ДНЯ** 👇",
        "SW": "👇 **МЕНЮ ДНЯ** 👇"
    }
    
    footer = f"\n• • •\n\n{headers[channel]}\n"
    footer += "\n".join(digest)
    footer += "\n\nПрисоединяйтесь: [https://t.me/addlist/Z-91kI9P3MpkMzI0](https://t.me/addlist/Z-91kI9P3MpkMzI0)"
    
    return footer

if __name__ == "__main__":
    # python3 footer_manager.py AC 24.01 21:00
    if len(sys.argv) < 4:
        print("")
        sys.exit(0)
        
    print(get_daily_digest(sys.argv[1], sys.argv[2], sys.argv[3]))
