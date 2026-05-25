import os
import json

CORE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/"

class ESCRepo:
    def __init__(self):
        self.live_data_path = os.path.join(CORE_PATH, "ESC_2026_LIVE.json")
        self.network_path = os.path.join(CORE_PATH, "ebu_network.json")

    def load_json(self, path):
        if not os.path.exists(path): return {}
        with open(path, 'r') as f:
            return json.load(f)

    def get_country_status(self, country):
        data = self.load_json(self.live_data_path)
        return data.get("countries", {}).get(country, "No data")

    def get_next_event(self):
        data = self.load_json(self.live_data_path)
        return data.get("next_event", "Unknown")

if __name__ == "__main__":
    repo = ESCRepo()
    print(repo.get_next_event())
