import os
import subprocess

REPO_DIR = "/home/levdanskiy/.gemini/ENGINE/repos"

# ОБНОВЛЕННЫЙ СПИСОК (ПУБЛИЧНЫЕ ГИГАНТЫ)
TARGETS = {
    # --- MUSIC ---
    "fma-dataset": "https://github.com/mdeff/fma.git", # Free Music Archive
    "spotify-playlist": "https://github.com/mackorone/spotify-playlist-database.git", # Миллион плейлистов
    
    # --- ART & HISTORY ---
    "moma-collection": "https://github.com/MuseumofModernArt/collection.git", # MoMA Art
    "tate-collection": "https://github.com/tategallery/collection.git", # Tate Gallery
    
    # --- FOOD ---
    "open-cocktails": "https://github.com/ybon/open-cocktails.git",
    "openfoodfacts-server": "https://github.com/openfoodfacts/openfoodfacts-server.git", # ГИГАНТ
    "taco-recipes": "https://github.com/sinker/tacofancy.git", # Рецепты тако (для примера)
    
    # --- EUROVISION & DATA ---
    "awesome-public-datasets": "https://github.com/awesomedata/awesome-public-datasets.git",
}

def harvest():
    print("🚜 STARTING MASSIVE HARVEST (DEPTH 1)...")
    
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
        
    for name, url in TARGETS.items():
        target_path = os.path.join(REPO_DIR, name)
        
        if os.path.exists(target_path):
            print(f"⚠️  Skipping {name} (Already exists)")
            continue
            
        print(f"⬇️  Cloning {name}...")
        try:
            # Используем depth 1 для скорости и экономии места
            subprocess.run(["git", "clone", "--depth", "1", url, target_path], check=True) # Removed stdout redirection to see errors if any
            print(f"✅ Cloned: {name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone: {name}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("🔄 Updating Brain Index...")
    subprocess.run(["python3", "/home/levdanskiy/.gemini/ENGINE/scripts/indexer.py"])
    print("🏁 HARVEST COMPLETE.")

if __name__ == "__main__":
    harvest()