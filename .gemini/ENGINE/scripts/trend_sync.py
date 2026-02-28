#!/usr/bin/env python3
import os
import json
import datetime

# ПУТИ К БАЗАМ ЗНАНИЙ
DNA_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/SUPREME_VISUAL_DNA.json"
GLOSSARY_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/glossary.json"
MINING_PATH = "/home/levdanskiy/.gemini/CORE/knowledge/TREND_MINING.json"

def sync_all_nuances():
    print("🚀 **EXECUTING DATA-DRIVEN SUPREME SYNC (Zero Hardcode)...**")
    
    if not os.path.exists(MINING_PATH):
        print("❌ ERROR: No mining data. Run data_miner first.")
        return

    with open(MINING_PATH, 'r') as f:
        mining = json.load(f)

    # 1. ОБНОВЛЯЕМ AR ТРЕНДЫ В DNA
    if os.path.exists(DNA_PATH):
        with open(DNA_PATH, 'r') as f:
            dna = json.load(f)
        
        dna["ar_trends"] = mining["ar_trends"]
        
        # Обновляем технические нюансы каналов из майнинга
        for ch in dna["channels"]:
            mining_key = ch # AC, NB, etc
            if ch == "AC": mining_key = "ARCHITECT"
            if ch == "NB": mining_key = "TRAVELER"
            if ch == "SW": mining_key = "HEDONIST"
            if ch == "YV": mining_key = "INSIDER"
            
            # Добавляем свежий тренд в описание канала
            latest_nuance = mining["channel_nuances"].get(mining_key, ["Standard"])[0]
            dna["channels"][ch]["current_trend"] = latest_nuance
            
        dna["last_sync"] = str(datetime.datetime.now())
        with open(DNA_PATH, 'w') as f:
            json.dump(dna, f, indent=4)
        print("✅ AR and Visual DNA updated from LIVE mining.")

    # 2. ОБНОВЛЯЕМ ГЛОССАРИЙ (ТОНВОЙС)
    if os.path.exists(GLOSSARY_PATH):
        with open(GLOSSARY_PATH, 'r') as f:
            glossary = json.load(f)
        
        for dna_key, words in mining["channel_nuances"].items():
            if dna_key in glossary:
                # Наполняем глоссарий реальными словами из поиска
                glossary[dna_key] = list(set(glossary[dna_key] + words))
        
        with open(GLOSSARY_PATH, 'w') as f:
            json.dump(glossary, f, indent=4)
        print("✅ Channel-specific Tone of Voice updated.")

if __name__ == "__main__":
    sync_all_nuances()