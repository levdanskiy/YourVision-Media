#!/usr/bin/env python3
import json
import os

def render_all():
    # 1. Загрузка данных
    with open(".gemini/system/database/yv_live.json", 'r') as f:
        yv_db = json.load(f)
    with open(".gemini/system/database/global_events.json", 'r') as f:
        global_db = json.load(f)
    
    out_path = ".gemini/system/calendars/YV_ESC_Live_Calendar.md"
    
    md = "# 📡 YourVision: ESC 2026 LIVE CALENDAR\n"
    md += "**// Интегрированный График: ESC + Глобальные События //**\n\n"
    
    # Секция ESC
    md += "### 📅 МАСТЕР-КАЛЕНДАРЬ ESC\n"
    md += "| Дата | Событие | Статус |\n| :--- | :--- | :--- |\n"
    for ev in yv_db['master_calendar']:
        icon = "✅" if ev['status'] == "done" else "⬜"
        md += f"| **{ev['date']}** | {ev['event']} | {icon} |\n"
    
    # Секция Глобал
    md += "\n### 🌍 ГЛОБАЛЬНЫЙ РАДАР (Music, Cinema, Sports)\n"
    md += "| Дата | Событие | Локация |\n| :--- | :--- | :--- |\n"
    for cat in global_db['categories'].values():
        for item in cat:
            date = item.get('date', f"{item.get('start_date')} - {item.get('end_date')}")
            md += f"| {date} | **{item['event']}** | {item['location']} |\n"

    # Добавляем Synergy Notes
    md += f"\n> 💡 **СИНЕРГИЯ:** {global_db['synergy_notes']['FEB_2026']}\n"

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print("✅ Календарь перерисован с учетом глобальных событий.")

if __name__ == "__main__":
    render_all()
