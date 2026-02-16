import sys
import os
import json

# Add repos to path
sys.path.append("/home/levdanskiy/.gemini/ENGINE/repos")
sys.path.append("/home/levdanskiy/.gemini/ENGINE/scripts")

from esc_repo import ESCRepo
from knowledge_repo import KnowledgeRepo

class ArgusController:
    def __init__(self):
        self.esc_repo = ESCRepo()
        self.knowledge_repo = KnowledgeRepo()
        self.scripts_path = "/home/levdanskiy/.gemini/ENGINE/scripts/"

    def execute_mission(self, mission_type, target):
        print(f"👁️ ARGUS CONTROLLER: Starting mission '{mission_type}' on '{target}'")
        
        context = ""
        
        # 1. Consult Repositories
        if mission_type in ["poll", "chart_results", "news"]:
            # Try to find in ESC Repo
            esc_data = self.esc_repo.get_country_status(target)
            if esc_data != "No data":
                print(f"   - ✅ Found in ESC Repo: {esc_data}")
                context += f"Repo Data: {esc_data} "
            else:
                print(f"   - ❌ Not found in Repos. Initiating Web Search Protocol.")
                # Signal to LLM to perform search
                print(f"   - [[NEED_WEB_SEARCH: {target} {mission_type} latest news 2026]]")
                return # Stop here, wait for LLM to provide search results

        # 2. Activate Intel Hub (Simulation of analysis)
        # In a real loop, we would pass the web search results back here.
        # For now, we proceed to generation preparation.
        
        print(f"   - ⚙️ Generating Intel Report via 'intel_hub.py'...")
        cmd = f"python3 {self.scripts_path}intel_hub.py --topic '{target} {mission_type}'"
        os.system(cmd)
        
        print("✅ ARGUS: Mission Intel Secured (Ready for Content Generation).")

if __name__ == "__main__":
    agent = ArgusController()
    if len(sys.argv) > 2:
        agent.execute_mission(sys.argv[1], sys.argv[2])
    else:
        print("Usage: argus_controller.py <mission> <target>")