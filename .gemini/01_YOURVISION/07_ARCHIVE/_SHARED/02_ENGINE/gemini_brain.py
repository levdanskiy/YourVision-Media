import sys
import os
import json
import subprocess
import datetime

CORE_PATH = "/home/levdanskiy/.gemini/"
INDEX_PATH = os.path.join(CORE_PATH, "CORE/knowledge/DATA_INDEX.json")
HIVE_PATH = os.path.join(CORE_PATH, "CORE/knowledge/AGENT_HIVE.json")

class GeminiBrain:
    def __init__(self):
        self.index = self._load_json(INDEX_PATH)
        self.hive = self._load_json(HIVE_PATH)

    def _load_json(self, path):
        if not os.path.exists(path): return {}
        with open(path, 'r') as f:
            return json.load(f)

    def status(self):
        print("\n🧠 GEMINI BRAIN STATUS REPORT")
        print("===========================")
        print(f"🕒 Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📚 Knowledge Index: {sum(len(v) for v in self.index.values())} files indexed.")
        print(f"🐝 Agent Hive: {self.hive.get('hive_status', 'UNKNOWN')}")
        
        # Check active plan debts
        plan_path = os.path.join(CORE_PATH, "TIMELINE/daily_workflow/daily_plan_13.02.md")
        if os.path.exists(plan_path):
            with open(plan_path, 'r') as f:
                debts = [l.strip() for l in f if "⬜" in l]
            print(f"🚨 Pending Tasks (13.02): {len(debts)}")
        else:
            print("⚠️ No active plan found for 13.02")

    def find_data(self, query):
        print(f"\n🔍 SEARCHING KNOWLEDGE BASE FOR: '{query}'")
        matches = []
        for category, files in self.index.items():
            for f in files:
                if query.lower() in f.lower():
                    matches.append(f)
        
        if not matches:
            print("❌ No direct matches found.")
        else:
            print(f"✅ Found {len(matches)} matches. Top 5:")
            for m in matches[:5]:
                print(f"   - {m}")
        return matches

    def execute(self, task_type, target):
        print(f"\n🚀 EXECUTING: {task_type} -> {target}")
        # Routing logic
        if task_type in ["chart", "poll", "news", "review"]:
            print(f"   -> Routing to ARGUS CONTROLLER")
            cmd = f"python3 {CORE_PATH}ENGINE/agents/argus_controller.py {task_type} '{target}'"
            os.system(cmd)
        else:
            print("⚠️ Unknown task type. Manual intervention required.")

if __name__ == "__main__":
    brain = GeminiBrain()
    
    if len(sys.argv) < 2:
        brain.status()
    else:
        cmd = sys.argv[1]
        if cmd == "status":
            brain.status()
        elif cmd == "find":
            brain.find_data(sys.argv[2])
        elif cmd == "execute":
            brain.execute(sys.argv[2], sys.argv[3])
