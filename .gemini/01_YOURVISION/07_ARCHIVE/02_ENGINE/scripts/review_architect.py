#!/usr/bin/env python3
import sys

def build_review(artist, song, user_thoughts, tech_data):
    """
    subject = "Artist - Song"
    user_thoughts = {
        "sound": "...",
        "vibe": "...",
        "verdict": "..."
    }
    """
    print(f"--- 🖋 ГЕНЕРАЦИЯ РЕЦЕНЗИИ: {artist.upper()} ---")
    
    review_structure = f"""
🎧 **REVIEW: {artist.upper()} - {song.upper()}**

**ЗВУКОВАЯ АРХИТЕКТУРА**
{user_thoughts['sound']}

**ЭМОЦИОНАЛЬНЫЙ РЕЗОНАНС**
{user_thoughts['vibe']}

**#TECH_PASSPORT**
- Стриминг: {tech_data['streaming']}
- Тренды: {tech_data['trends']}
- Прогноз: {user_thoughts['verdict']}

---
[UA BLOCK WILL BE HERE]
"""
    print(review_structure)

if __name__ == "__main__":
    # Пример данных
    build_review(
        "Sander Silva", "Electric Pulse",
        {"sound": "Дорогой индастриал с элементами киберпанка.", "vibe": "Холодный, отстраненный, но мощный.", "verdict": "Главный фаворит отбора."},
        {"streaming": "+15% daily", "trends": "Norse Futurism"}
    )
