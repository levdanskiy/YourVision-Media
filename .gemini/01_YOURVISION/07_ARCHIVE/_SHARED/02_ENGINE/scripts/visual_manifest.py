#!/usr/bin/env python3
import json
import os

KNOWLEDGE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/visual_manifest.json"

def get_visuals():
    if not os.path.exists(KNOWLEDGE_PATH):
        return "Visual manifest not found."
    with open(KNOWLEDGE_PATH, 'r') as f:
        data = json.load(f)
    
    return f"🎨 **VISUAL DNA ({data['month']} {data['year']}):**\n" \
           f"Style: {data['visual_code']} | Aesthetic: {data['aesthetic']}\n" \
           f"Color: {data['primary_color']} | MJ: {data['mj_parameters']}\n" \
           f"Branding: {data['branding_rule']}"

if __name__ == "__main__":
    print(get_visuals())

