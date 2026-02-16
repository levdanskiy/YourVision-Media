#!/usr/bin/env python3
import os
import sys
import json
import time
import logging

# --- HIVE ENGINE CONFIGURATION (V8-STYLE) ---
class HiveConfig:
    HIVE_ROOT = "/home/levdanskiy/.gemini/"
    AGENTS_DIR = os.path.join(HIVE_ROOT, "ENGINE/agents/")
    STATE_FILE = os.path.join(HIVE_ROOT, "CORE/knowledge/AGENT_HIVE.json")
    LOG_FILE = os.path.join(HIVE_ROOT, "system/hive_engine.log")

class HiveEngine:
    """
    Autonomous Engine for Agent Management.
    Architecture: Isolated Agents (Isolates) with centralized state control.
    """
    def __init__(self):
        self.is_initialized = False
        self.agents = ["ARGUS", "VITRUVIUS", "MNEMOSYNE", "HELIOS", "HERMES", "HEPHAESTUS", "DIKE"]
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            filename=HiveConfig.LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | [HIVE_ENGINE] %(message)s'
        )

    def Initialize(self):
        """Initializes the Hive Platform and loads Agent Snapshots."""
        logging.info("Initializing Hive Engine...")
        if not os.path.exists(HiveConfig.STATE_FILE):
            self._create_default_state()
        self.is_initialized = True
        logging.info("Hive Engine Initialized Successfully.")
        return True

    def _create_default_state(self):
        state = {
            "version": "1.0.0",
            "status": "RUNNING",
            "agents": {name: {"status": "IDLE", "uptime": 0} for name in self.agents}
        }
        with open(HiveConfig.STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)

    def RunIsolate(self, agent_name):
        """Executes a specific agent task in an isolated context."""
        if not self.is_initialized:
            return False
        
        logging.info(f"Starting Isolate: {agent_name}")
        
        if agent_name == "ARGUS":
            # Возвращаем глобальные задачи
            os.popen(f"python3 {HiveConfig.HIVE_ROOT}ENGINE/agents/argus_global_scout.py").read()
            self._update_state(agent_name, "GLOBAL_SCOUTING")
        else:
            self._update_state(agent_name, "ACTIVE")
        
        return True

    def _update_state(self, name, status):
        with open(HiveConfig.STATE_FILE, 'r') as f:
            data = json.load(f)
        data["agents"][name]["status"] = status
        data["agents"][name]["last_tick"] = time.time()
        with open(HiveConfig.STATE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def Dispose(self):
        """Releases resources and stops all utility threads."""
        logging.info("Disposing Hive Engine...")
        self.is_initialized = False
        return True

# --- CLI INTERFACE ---
if __name__ == "__main__":
    engine = HiveEngine()
    if engine.Initialize():
        command = sys.argv[1] if len(sys.argv) > 1 else "tick"
        
        if command == "daemon":
            try:
                while True:
                    for agent in engine.agents:
                        engine.RunIsolate(agent)
                    time.sleep(60) # Heartbeat
            except KeyboardInterrupt:
                engine.Dispose()
        else:
            # Single tick for hooks
            for agent in engine.agents:
                engine.RunIsolate(agent)