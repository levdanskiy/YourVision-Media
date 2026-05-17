import os
import datetime
import re

BASE_DIR = "/home/levdanskiy/.gemini"
WORKFLOW_DIR = os.path.join(BASE_DIR, "TIMELINE/daily_workflow")
STATE_FILE = os.path.join(BASE_DIR, "CORE/STATE.md")

def get_current_plan_file():
    """Находит файл плана на сегодня (или ближайший будущий)."""
    # ... (rest of the logic remains similar but with correct directory)
    today = datetime.date.today()
    plans = []
    if not os.path.exists(WORKFLOW_DIR):
        print(f"❌ Error: {WORKFLOW_DIR} does not exist.")
        return None
        
    for file in os.listdir(WORKFLOW_DIR):
        if file.startswith("daily_plan_") and file.endswith(".md"):
            try:
                date_str = file.replace("daily_plan_", "").replace(".md", "")
                plan_date = datetime.datetime.strptime(f"{date_str}.{today.year}", "%d.%m.%Y").date()
                plans.append((plan_date, os.path.join(WORKFLOW_DIR, file)))
            except ValueError:
                continue
    
    plans.sort(key=lambda x: x[0])
    
    # Сначала ищем точное совпадение
    for date, path in plans:
        if date == today:
            return path
            
    # Если на сегодня нет, берем ближайший будущий или последний из прошлого
    # Для целей системы возвращаем тот, что сейчас 'в фокусе' (например, 30.01)
    # Если пользователь работает с 30.01, нам нужен он.
    target_plan = os.path.join(WORKFLOW_DIR, "daily_plan_30.01.md")
    if os.path.exists(target_plan):
        return target_plan
        
    return plans[-1][1] if plans else None

def analyze_plan(file_path):
    """Анализирует план и возвращает статистику."""
    if not file_path or not os.path.exists(file_path):
        return {}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Формат: ⬜ [ОЖИДАНИЕ] или ✅ [ГОТОВО]
    pending = len(re.findall(r"⬜\s*\[ОЖИДАНИЕ\]", content))
    done = len(re.findall(r"✅\s*\[ГОТОВО\]", content))
    # Долги помечаются тегом ⚠️
    debts = len(re.findall(r"⚠️.+⬜\s*\[ОЖИДАНИЕ\]", content))
    
    return {
        "file": os.path.basename(file_path),
        "debts": debts,
        "pending": pending - debts, # Обычные посты без учета долгов
        "done": done,
        "total_active": pending
    }

def update_state_file(stats):
    """Записывает состояние в STATE.md."""
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%d.%m.%Y")
    
    content = f"""# 🧠 GEMINI SYSTEM STATE
**Last Updated:** {now_str}

---

### 📅 CURRENT CONTEXT
*   **Real Date:** {date_str}
*   **Active Plan:** `{stats.get('file', 'N/A')}`

### 📊 STATUS
*   🔴 **CRITICAL DEBTS:** {stats.get('debts', 0)}
*   🟠 **PENDING TASKS:** {stats.get('pending', 0)}
*   🟢 **COMPLETED:** {stats.get('done', 0)}

---

### 🚀 NEXT PRIORITY
*(Auto-generated based on logic)*
1.  Check for `[ДОЛГ]` tags in Active Plan.
2.  Execute oldest debt first.
3.  Proceed to current day schedule.

### 📝 SYSTEM NOTES
*   **Sync Status:** Active (Script `sync_status.py` available).
*   **Protocol:** ABSOLUTE SYNCHRONIZATION enabled.
"""
    
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"STATE.md updated based on {stats.get('file')} for {date_str}")

def main():
    plan_file = get_current_plan_file()
    stats = analyze_plan(plan_file)
    update_state_file(stats)

if __name__ == "__main__":
    main()
