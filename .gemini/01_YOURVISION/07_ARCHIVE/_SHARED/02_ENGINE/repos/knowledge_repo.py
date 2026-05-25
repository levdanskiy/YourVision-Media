import os
import json

CORE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/"

class KnowledgeRepo:
    def __init__(self):
        self.world_bible_path = os.path.join(CORE_PATH, "WORLD_BIBLE.json")
        self.glossary_path = os.path.join(CORE_PATH, "glossary.json")
        self.themes_path = os.path.join(CORE_PATH, "THEME_REGISTRY.json")

    def load_json(self, path):
        if not os.path.exists(path): return {}
        with open(path, 'r') as f:
            return json.load(f)

    def get_world_context(self):
        data = self.load_json(self.world_bible_path)
        return data.get("history", [])[-5:] # Last 5 events

    def get_term_definition(self, term):
        data = self.load_json(self.glossary_path)
        return data.get(term, "Unknown term")

if __name__ == "__main__":
    repo = KnowledgeRepo()
    print(repo.get_world_context())
