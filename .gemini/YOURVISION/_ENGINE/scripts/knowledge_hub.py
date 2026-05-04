#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

# Пути
BASE_DIR = "/home/levdanskiy/.gemini"
REPOS_DIR = os.path.join(BASE_DIR, "ENGINE/repos")
FEEDS_DIR = os.path.join(BASE_DIR, "system/feeds")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "CORE/knowledge")
SCRIPTS_DIR = os.path.join(BASE_DIR, "ENGINE/scripts")

class KnowledgeHubV3:
    def __init__(self):
        self.context = {}

    def get_astro_data(self):
        """Вызывает астро-калькулятор"""
        try:
            res = subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "astro_calc.py")], capture_output=True, text=True)
            return res.stdout.strip().split("\n")
        except:
            return ["Astro: Local error"]

    def get_symbol_info(self, keyword):
        """Ищет символ в базе алхимии"""
        path = os.path.join(KNOWLEDGE_DIR, "alchemy_symbols.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return data['symbols'].get(keyword.upper(), "Symbol not found")
        return None

    def get_lore_snippet(self, topic):
        """Вызывает синтезатор легенд"""
        try:
            res = subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "lore_synthesizer.py"), topic], capture_output=True, text=True)
            return json.loads(res.stdout)
        except:
            return None

    def refresh_daily_context(self, date_obj):
        """Собирает полный контекст на день"""
        print(f"🧠 KNOWLEDGE HUB V3.0: Синхронизация {date_obj.strftime('%d.%m')}...")
        
        # Пример: 30.01 - День Круассана. Ищем лор.
        lore = self.get_lore_snippet("Круассан")
        
        self.context = {
            "date": date_obj.strftime("%Y-%m-%d"),
            "astro": self.get_astro_data(),
            "active_symbol": self.get_symbol_info("BREAD"),
            "daily_lore": lore,
            "status": "TOTAL_SYNC_ACTIVE"
        }
        
        output_path = os.path.join(FEEDS_DIR, "daily_knowledge_context.json")
        with open(output_path, 'w') as f:
            json.dump(self.context, f, indent=4, ensure_ascii=False)
        print(f"✅ Центр знаний готов. Все модули подключены.")

if __name__ == "__main__":
    hub = KnowledgeHubV3()
    hub.refresh_daily_context(datetime.now())
