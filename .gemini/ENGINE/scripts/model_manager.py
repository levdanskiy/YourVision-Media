#!/usr/bin/env python3
import json
import os
import sys
import random

KNOWLEDGE_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/model_database.json"

def get_model(gender):
    if not os.path.exists(KNOWLEDGE_PATH):
        return "Model database not found."
    with open(KNOWLEDGE_PATH, 'r') as f:
        data = json.load(f)
    
    gender = gender.lower()
    if gender not in data:
        return f"Unknown gender: {gender}"
    
    # Selecting a model (could be rotated by storing state, for now random)
    model = random.choice(data[gender])
    return f"👤 **SELECTED MODEL ({gender.upper()}):** {model}"

if __name__ == "__main__":
    gender = sys.argv[1] if len(sys.argv) > 1 else "female"
    print(get_model(gender))
