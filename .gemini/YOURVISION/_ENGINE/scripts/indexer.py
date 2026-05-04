import os
import json

ENGINE_ROOT = "/home/levdanskiy/.gemini/ENGINE"
CONTENT_ROOT = "/home/levdanskiy/.gemini/CONTENT"
INDEX_FILE = "/home/levdanskiy/.gemini/CORE/knowledge/DATA_INDEX.json"

def scan_total():
    index = {
        "agents": [],
        "scripts": [],
        "repos": {},
        "history": [] # Content & Posts
    }
    
    # 1. Scan Engine
    for root, dirs, files in os.walk(ENGINE_ROOT):
        rel_path = os.path.relpath(root, ENGINE_ROOT)
        if any(part.startswith('.') and part != '.' for part in rel_path.split(os.sep)): continue
        for file in files:
            full_path = os.path.join(root, file)
            if "/agents" in root: index["agents"].append(full_path)
            elif "/scripts" in root: index["scripts"].append(full_path)
            elif "/repos" in root:
                cat = "general"
                if "eurovision" in full_path.lower(): cat = "eurovision"
                elif "chart" in full_path.lower(): cat = "charts"
                if cat not in index["repos"]: index["repos"][cat] = []
                index["repos"][cat].append(full_path)

    # 2. Scan Content
    for root, dirs, files in os.walk(CONTENT_ROOT):
        for file in files:
            if file.endswith(".md"):
                index["history"].append(os.path.join(root, file))

    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=4)
    print(f"✅ Total Index Updated. History files: {len(index['history'])}")

if __name__ == "__main__":
    scan_total()