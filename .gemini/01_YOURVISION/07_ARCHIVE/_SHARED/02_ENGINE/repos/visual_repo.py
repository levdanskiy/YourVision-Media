import os
import json

CORE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/"

class VisualRepo:
    def __init__(self):
        self.atlas_path = os.path.join(CORE_PATH, "VISUAL_ATLAS.json")
        self.manifest_path = os.path.join(CORE_PATH, "visual_manifest.json")

    def load_json(self, path):
        if not os.path.exists(path): return {}
        with open(path, 'r') as f:
            return json.load(f)

    def get_style_guide(self, channel):
        data = self.load_json(self.manifest_path)
        return data.get(channel, {})

    def get_color_palette(self, mood):
        data = self.load_json(self.atlas_path)
        return data.get("palettes", {}).get(mood, [])

if __name__ == "__main__":
    repo = VisualRepo()
    print(repo.get_style_guide("NB"))
