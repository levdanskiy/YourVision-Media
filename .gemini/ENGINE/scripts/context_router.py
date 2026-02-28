#!/usr/bin/env python3
import sys
import os
import datetime
import json
import re

# --- CONFIGURATION (TOTAL INTEGRITY V30.0) ---
CORE_PATH = "/home/levdanskiy/.gemini/"
SCRIPTS_PATH = os.path.join(CORE_PATH, "ENGINE/scripts/")
KNOWLEDGE_PATH = os.path.join(CORE_PATH, "CORE/knowledge/")
TIMELINE_PATH = os.path.join(CORE_PATH, "TIMELINE/daily_workflow/")
HIVE_PATH = os.path.join(CORE_PATH, "ENGINE/agents/")
GEMINI_MD = os.path.join(CORE_PATH, "GEMINI.md")

PROMPTS = {
    "ac": os.path.join(CORE_PATH, "CORE/skills/User_Promts_Almanac.md"),
    "nb": os.path.join(CORE_PATH, "CORE/skills/User_Promts_Almanac.md"),
    "sw": os.path.join(CORE_PATH, "CORE/skills/User_Promts_Almanac.md"),
    "yv": os.path.join(CORE_PATH, "CORE/skills/User_Promts_YourVision.md"),
    "news": os.path.join(CORE_PATH, "CORE/skills/User_Promts_YourVision_News.md")
}

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except: return f"❌ ERROR: File not found: {path}"

def extract_location(topic):
    cities = ["Zurich", "Milan", "Vienna", "Auckland", "Paris", "London", "Berlin", "Stockholm", "Tokyo", "Helsinki"]
    for city in cities:
        if city.lower() in topic.lower(): return city
    return "Zurich"

def execute_power_pack(channel, args):
    topic = " ".join(args) if args else "General Context"
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    time = datetime.datetime.now().strftime("%H:%M")
    city = extract_location(topic)
    
    # 1. INTEGRITY, SYNERGY & STATUS SYNC
    os.popen(f"python3 {SCRIPTS_PATH}integrity_check.py").read()
    synergy = os.popen(f"python3 {HIVE_PATH}mnemosyne_nexus.py get_context").read()

    output = f"\n🌌 **SUPREME INTELLIGENCE PACK (V30.0): {channel.upper()}**\n"
    output += f"🎯 TARGET: {topic} | 📍 LOC: {city} | 🕒 TIME: {time}\n"
    output += synergy
    output += "================================================\n"

    # 2. ADAPTIVE PIPELINE (TOTAL CONSOLIDATION)
    pipeline = ["true_time.py", f"GOD_EYE_CORE.py {date}", f"Global_Event_Oracle.py {date}", "nasa_rss.py"]
    
    # Mining Logic
    if any(k in topic.lower() for k in ["news", "latest", "trends", "новости"]):
        pipeline.extend(["data_miner.py", "esc_crawler.py"])
    if any(k in topic.lower() for k in ["odds", "stats", "chance", "шансы"]):
        pipeline.extend(["intel_hub.py", "hype_meter.py"])
    if any(k in topic.lower() for k in ["myth", "legend", "миф", "сказка"]):
        pipeline.extend(["myth_finder.py"])

    # DNA & Production
    dna_map = {"ac": "ARCHITECT", "nb": "TRAVELER", "sw": "HEDONIST", "yv": "INSIDER"}
    dna = dna_map.get(channel, "ARCHITECT")
    
    pipeline.extend([
        f"glossary_injector.py {dna}",
        f"nuance_injector.py {channel}",
        f"weather_engine.py '{city}'",
        f"arcane_engine.py {channel.upper()} {date} {time}",
        f"smart_ar_engine.py {channel} '{topic}'",
        f"read_time_calc.py"
    ])
    
    output += "⚙️ **HIVE AGENTS ACTIVITY (Full Omni-Loop):**\n"
    for cmd in pipeline:
        s_name = cmd.split()[0]
        if os.path.exists(os.path.join(SCRIPTS_PATH, s_name)):
            res = os.popen(f"python3 {SCRIPTS_PATH}{cmd}").read().strip()
            output += f"   ▶️ {cmd} -> {res[:100]}...\n"

    # 3. DYNAMIC KNOWLEDGE
    kw = topic.split()[0] if topic.split() else "None"
    res = os.popen(f"grep -i -h '{kw}' {KNOWLEDGE_PATH}*.json | head -n 3").read().strip()
    if res:
        output += "\n📚 **KNOWLEDGE LINKED:**\n"
        output += f"   {res[:300]}...\n"

    return output

def handle_command(trigger, args):
    t = trigger.lower()
    
    # --- SAFETY LOCK & DIRECT REQUEST PROTOCOL ---
    is_user_request = "--user-request" in args
    if is_user_request:
        args.remove("--user-request")
    
    if t in ["ac", "nb", "sw", "yv"]:
        if not is_user_request:
            return "🔒 **BLOCK:** Autonomous generation detected. Provide a direct request with the '--user-request' flag."
        
        # If it IS a user request, we proceed but will LOCK the system immediately after.
        res = execute_power_pack(t, args)
        os.popen(f"python3 {SCRIPTS_PATH}safety_lock.py on").read()
        return f"{res}\n\n🔒 **SYSTEM RE-LOCKED.** Wait for the next direct user request."

    if t == "unlock": return os.popen(f"python3 {SCRIPTS_PATH}safety_lock.py off").read()
    if t == "lock": return os.popen(f"python3 {SCRIPTS_PATH}safety_lock.py on").read()
    
    if t == "init": 
        os.popen(f"python3 {HIVE_PATH}hive_commander.py daemon &")
        return f"✅ SYSTEM INITIALIZED.\n🐝 **HIVE ACTIVATED (V30.0 - Omni Core).**\n{read_file(GEMINI_MD)}\n{execute_power_pack('ac', args)}"

    if t == "plan": 
        p_path = os.path.join(TIMELINE_PATH, f"daily_plan_{datetime.datetime.now().strftime('%d.%m')}.md")
        return read_file(p_path)
    
    # Bypassing lock for non-content commands like 'fix', 'save', 'sync'
    if t == "fix": return os.popen(f"python3 {SCRIPTS_PATH}validation_fixer.py {args[0]}").read()
    if t == "save": return os.popen(f"python3 {SCRIPTS_PATH}auto_archivist.py {args[0]}").read()
    if t == "sync": return os.popen(f"python3 {SCRIPTS_PATH}trend_sync.py").read()

    return f"❌ Unknown command or restricted access: @{trigger}"

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    print(handle_command(sys.argv[1], sys.argv[2:]))
