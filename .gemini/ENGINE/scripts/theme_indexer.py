import re
import json
import os

MASTER_DIR = "/home/levdanskiy/.gemini/TIMELINE/master_plans/02/"
REGISTRY_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/THEME_REGISTRY.json"

def build_registry():
    registry = {}
    if not os.path.exists(MASTER_DIR):
        print("❌ Master directory not found.")
        return
        
    for f_name in os.listdir(MASTER_DIR):
        if f_name.endswith(".md"):
            channel = f_name.split("_")[0]
            registry[channel] = []
            with open(os.path.join(MASTER_DIR, f_name), 'r', encoding='utf-8') as f:
                for line in f:
                    # Robust regex to catch: * HH:MM | **CH** | EMOJI #RUBRIC: TOPIC - [STATUS]
                    match = re.search(r'\* (\d{2}:\d{2}) \| \*\*(\w+)\*\* \|.*?#(\w+): (.*?) - (✅|⬜)', line)
                    if match:
                        time, ch, rubric, topic, status = match.groups()
                        registry[channel].append({
                            "time": time,
                            "rubric": rubric,
                            "topic": topic.strip().split('.')[0], # Match base topic without punctuation
                            "full_line": line.strip()
                        })
    
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)
    
    total = sum(len(v) for v in registry.values())
    print(f"✅ THEME REGISTRY BUILT: {total} slots indexed.")

if __name__ == "__main__":
    build_registry()