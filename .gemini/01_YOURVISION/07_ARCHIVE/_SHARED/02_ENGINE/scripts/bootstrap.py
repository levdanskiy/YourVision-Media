import os

CRITICAL_FILES = [
    ".gemini/GEMINI.md",
    ".gemini/KNOWLEDGE/Resource_Map.md",
    ".gemini/KNOWLEDGE/Visual_Presets_2026.md",
    ".gemini/COMMAND_REFERENCE.md"
]

def load_context():
    print("\n🔥 SYSTEM BOOTSTRAP: LOADING CRITICAL MANDATES 🔥\n")
    
    for path in CRITICAL_FILES:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                # Извлекаем только заголовки и мандаты для краткости
                print(f"--- {os.path.basename(path)} ---")
                for line in content.split('\n'):
                    if "MANDATE" in line.upper() or "ЗАПРЕЩЕНО" in line.upper() or "СТРОГО" in line.upper():
                        print(f"🛑 {line.strip()}")
        else:
            print(f"⚠️ ERROR: Missing {path}")

    print("\n✅ CONTEXT LOADED. DO NOT HALLUCINATE. DO NOT IGNORE.")

if __name__ == "__main__":
    load_context()
