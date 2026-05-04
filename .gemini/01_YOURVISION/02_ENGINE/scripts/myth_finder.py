#!/usr/bin/env python3
import csv
import random
import sys
import json

class MythFinder:
    def __init__(self):
        self.tmi_path = "/home/levdanskiy/.gemini/ENGINE/repos/trilogy/data/tmi.csv"
        
    def get_random_motif(self, keyword=None):
        try:
            with open(self.tmi_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                if keyword:
                    filtered = [row for row in rows if keyword.lower() in row['motif_name'].lower()]
                    if filtered:
                        rows = filtered
                
                if not rows:
                    return {"motif": "Unknown", "id": "000"}
                
                choice = random.choice(rows)
                return {
                    "id": choice['id'],
                    "motif": choice['motif_name'],
                    "chapter": choice['chapter_name'],
                    "notes": choice['notes']
                }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    finder = MythFinder()
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(finder.get_random_motif(keyword), indent=4))