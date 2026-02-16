import sqlite3
import random
import json

DB_PATH = '/home/levdanskiy/.gemini/content_plan.db'

def get_last_data(channel):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Берем последние 3 поста канала для анализа
    cursor.execute("SELECT grade, gender, ethnicity, aspect_ratio, lighting, angle, rubric FROM posts WHERE channel=? ORDER BY id DESC LIMIT 3", (channel,))
    history = cursor.fetchall()
    conn.close()
    return history

def get_job_spec(channel):
    history = get_last_data(channel)
    last = history[0] if history else None
    
    # 1. Чередование пола
    next_gender = "FEMALE" if last and last[1] == "MALE" else "MALE"
    
    # 2. Ротация Grade
    grade_options = ['Q', 'S', 'F', 'B', 'N', 'C', 'A', 'R', 'E', 'M']
    forbidden_grade = last[0] if last else ""
    next_grade = random.choice([g for g in grade_options if g != forbidden_grade])
    
    # 3. Ротация Освещения
    lighting_options = ["Natural Side-light", "Cinematic Backlight", "Golden Hour", "Moody Mist", "High-Key White", "Neon Contrast"]
    forbidden_lighting = last[4] if last else ""
    next_lighting = random.choice([l for l in lighting_options if l != forbidden_lighting])

    # 4. Ротация Ракурса
    angle_options = ["Eye-level", "Low-angle heroic", "Top-down macro", "Side-profile", "Close-up detail"]
    forbidden_angle = last[5] if last else ""
    next_angle = random.choice([x for x in angle_options if x != forbidden_angle])

    spec = {
        "channel": channel,
        "next_grade": next_grade,
        "next_gender": next_gender if channel in ['AC', 'NB'] else "NONE",
        "next_lighting": next_lighting,
        "next_angle": next_angle,
        "optics": "Phase One Macro" if channel == "SW" else "Leica Summilux" if channel == "NB" else "Hasselblad Prime",
        "vibe": "Organic Realism / Imperfect by Design"
    }
    return spec

if __name__ == "__main__":
    import sys
    ch = sys.argv[1] if len(sys.argv) > 1 else "AC"
    print(json.dumps(get_job_spec(ch), indent=4))
