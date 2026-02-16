#!/usr/bin/env python3
import json
import sys
import os

GLOSSARY_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/glossary.json"

def get_dna(channel_dna):
    if not os.path.exists(GLOSSARY_PATH):
        return "❌ DNA Error: Glossary not found."
    
    with open(GLOSSARY_PATH, 'r') as f:
        glossary = json.load(f)
    
    words = glossary.get(channel_dna.upper(), [])
    if words:
        return f"📖 **UPDATED TONE-OF-VOICE DNA ({channel_dna}):** Use keywords: {', '.join(words)}."
    return ""

if __name__ == "__main__":
    dna_type = sys.argv[1] if len(sys.argv) > 1 else "ARCHITECT"
    print(get_dna(dna_type))