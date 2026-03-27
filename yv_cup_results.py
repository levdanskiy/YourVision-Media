import requests
import sys
import datetime
import json
import os

# YourVision Cup Voting Engine V1.2 (3rd Place Logic)
TOKEN = '8687268784:AAEg59N9z0Fryad5MU3lf9BwIXv3RRfi2qg'
CHAT_ID = -1001588837632
STATE_FILE = '/home/levdanskiy/tournament_state.json'

def update_tournament_state(group_name, winners, third_place):
    if not os.path.exists(STATE_FILE):
        print("Error: State file not found")
        return

    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # 1. Add Top 2 to direct qualifiers
    for w in winners:
        if not any(q['country'] == w for q in state['qualifiers']):
            state['qualifiers'].append({
                'country': w,
                'group': group_name,
                'status': 'QUALIFIED'
            })

    # 2. Add 3rd place to Second Chance Pool
    if not any(wc['country'] == third_place for wc in state['wildcards']):
        state['wildcards'].append({
            'country': third_place,
            'group': group_name,
            'status': 'SECOND_CHANCE'
        })

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)
    print(f"✅ Sync Complete: {', '.join(winners)} qualified. {third_place} to Second Chance.")

def generate_result_post(group_name, winners, third_place):
    date_str = datetime.datetime.now().strftime("%d.%m")
    text = f"// ИД-ПОСТА: YV-{date_str}-10-05-Cup-Results-{group_name}\n"
    text += f"// ТЕМА: Итоги Группы {group_name}. Победители определены.\n"
    text += f"// ДАТА ПУБЛИКАЦИИ: {date_str}.2026, 10:05 (Europe/Рига)\n"
    text += f"⚔️ **YOURVISION CUP 2026: ГРУППОВОЙ РАУНД - ИТОГИ ГРУППЫ {group_name}**\n\n"
    text += f"Голосование закрыто. Группа {group_name} сделала свой выбор. Борьба за выход в плей-офф была бескомпромиссной, и мы готовы объявить имена счастливчиков.\n\n"
    text += "---\n\n"
    text += f"🥇 **1 МЕСТО:** {winners[0]} — Прямой выход\n"
    text += f"🥈 **2 МЕСТО:** {winners[1]} — Прямой выход\n"
    text += f"🥉 **3 МЕСТО:** {third_place} — Лист ожидания (Второй Шанс)\n\n"
    text += "---\n\n"
    text += "Поздравляем лидеров! Напоминаем, что только две лучшие страны из «Второго шанса» дополнят сетку 1/8 финала по итогам всех голосований.\n\n"
    text += f"`⏱ Время чтения: 0.5 мин | ⚔️ YourVision: Results`"
    
    file_path = f"/home/levdanskiy/YourVision_Studio/CONTENT/posts/2026/03/{date_str.split('.')[0]}/YV-Results-Group-{group_name}.md"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(text)
    print(f"✅ Draft Ready: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        group = sys.argv[1].upper()
        win1 = sys.argv[2]
        win2 = sys.argv[3]
        third = sys.argv[4]
        generate_result_post(group, [win1, win2], third)
        update_tournament_state(group, [win1, win2], third)
    else:
        print("Usage: yv_cup_results <GROUP> <WINNER1> <WINNER2> <THIRD_PLACE>")
