import os
import re

BASE_DIR = "/home/levdanskiy/.gemini/TIMELINE/daily_workflow"
SOURCE_PLAN = os.path.join(BASE_DIR, "daily_plan_11.02.md")
TARGET_PLAN = os.path.join(BASE_DIR, "daily_plan_12.02.md")

def transfer_debts():
    if not os.path.exists(SOURCE_PLAN) or not os.path.exists(TARGET_PLAN):
        return

    with open(SOURCE_PLAN, 'r', encoding='utf-8') as f:
        source_lines = f.readlines()

    debts = []
    capture = False
    
    # Собираем долги (всё, что помечено как ОЖИДАНИЕ) из секции ДОЛГИ и СЕГОДНЯ
    for line in source_lines:
        if "⬜ [ОЖИДАНИЕ]" in line:
            debts.append(line)

    if not debts: return

    # Читаем целевой план
    with open(TARGET_PLAN, 'r', encoding='utf-8') as f:
        target_content = f.read()

    # Формируем секцию долгов
    debt_section = "## 🚨 КРИТИЧЕСКИЕ ДОЛГИ (ПЕРЕНОС С 11.02)\n" + "".join(debts) + "\n"

    # Вставляем долги после заголовка (или заменяем пустую секцию)
    if "## 🚨 КРИТИЧЕСКИЕ ДОЛГИ" in target_content:
        target_content = re.sub(r"## 🚨 КРИТИЧЕСКИЕ ДОЛГИ.*?\n\n", debt_section, target_content, flags=re.DOTALL)
    else:
        # Вставляем после заголовка файла
        target_content = re.sub(r"(\*\*// .*? //\*\*\n\n)", r"\1" + debt_section, target_content)

    with open(TARGET_PLAN, 'w', encoding='utf-8') as f:
        f.write(target_content)
    
    print(f"✅ Transferred {len(debts)} pending tasks to {TARGET_PLAN}")

if __name__ == "__main__":
    transfer_debts()
