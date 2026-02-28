#!/usr/bin/env python3
import sys
import os
import json

CORE_PATH = "/home/levdanskiy/.gemini/"
DNA_FILE = os.path.join(CORE_PATH, "CORE/knowledge/SUPREME_VISUAL_DNA.json")

def get_channel_nuance(channel_id):
    channel_id = channel_id.upper()
    if not os.path.exists(DNA_FILE):
        return "❌ DNA Missing."
    
    with open(DNA_FILE, 'r') as f:
        dna = json.load(f)
    
    nuance = dna["channels"].get(channel_id, {})
    if not nuance: return ""

    output = f"\n📸 **VISUAL & TECHNICAL NUANCE ({channel_id}):**\n"
    output += f"• Editorial Lens: {nuance.get('editorial_lens', 'Standard')}\n"
    output += f"• Photography DNA: {nuance.get('photographer_dna', 'Pro')}\n"
    output += f"• Gear Simulation: {nuance.get('camera_gear', 'Digital')}\n"
    output += f"• Lighting Mandate: {nuance.get('lighting', 'Natural')}\n"
    output += f"• Current Trend: {nuance.get('current_trend', 'Standard')}\n"
    
    if channel_id == "SW":
        output += "• CRITICAL MANDATE: ALL SW posts MUST include a structured recipe: 1) Ingredients (grams) 2) Step-by-step instructions.\n"
    
    return output

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else "AC"
    print(get_channel_nuance(cid))