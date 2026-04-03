import os
import re
from collections import Counter

def audit_usage():
    models = []
    for root, dirs, files in os.walk(".gemini/CONTENT/"):
        for file in files:
            if file.endswith(".md"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        match = re.search(r"Использованная модель: (.*)", content)
                        if match: models.append(match.group(1).strip())
                except: continue

    stats = Counter(models)
    print("\n🌐 AGNOSTIC STACK REPORT:")
    print("-" * 60)
    for model, count in stats.items():
        print(f"• {model:.<45} {count} задач")
    
    print(f"\nРазнообразие стека: {len(stats.keys())} уникальных моделей.")
