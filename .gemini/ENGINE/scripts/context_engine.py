#!/usr/bin/env python3
import json
import os
from datetime import datetime

# Пути к базам
BASE_DIR = "/home/levdanskiy/.gemini"
STRATEGY_PATH = os.path.join(BASE_DIR, "TIMELINE/strategy/2026/SKELETON_2026.md")
WEATHER_SCRIPT = os.path.join(BASE_DIR, "ENGINE/scripts/weather_engine.py")
ARCANE_PATH = os.path.join(BASE_DIR, "CORE/knowledge/arcane_engine.json")

class ContextEngine:
    def __init__(self, date_str, channel):
        self.date = date_str
        self.channel = channel

    def get_strategy_focus(self):
        # Логика определения квартала и темы из SKELETON_2026
        month = int(self.date.split('.')[1])
        if 1 <= month <= 3:
            return "Q1: THE SPARK (Structure, Purity, Achievement)"
        return "Season Focus: Global Sync"

import sqlite3

    def get_user_schedule(self):
        """Читает локальный календарь"""
        db_path = "/home/levdanskiy/.gemini/CORE/calendar.db"
        if not os.path.exists(db_path): return "No calendar found"
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # Ищем события на целевую дату
        target_date = datetime.strptime(self.date, "%d.%m.%Y").strftime("%Y-%m-%d")
        c.execute("SELECT start_time, title FROM events WHERE start_time LIKE ?", (f"{target_date}%",))
        events = c.fetchall()
        conn.close()
        
        if not events: return "Free schedule"
        return ", ".join([f"{e[0].split('T')[1][:5]} {e[1]}" for e in events])

    def get_sweet_context(self):
        """Пункт 100+: Глубокая аналитика для канала Sweet"""
        vault_path = "/home/levdanskiy/.gemini/CORE/knowledge/SWEET_KNOWLEDGE_VAULT.json"
        if not os.path.exists(vault_path): return "Standard Pastry"
        
        with open(vault_path, 'r') as f:
            vault = json.load(f)
        
        # Выбираем случайную категорию и подпункт для вдохновения
        cat = random.choice(list(vault['SWEET_KNOWLEDGE_VAULT'].keys()))
        sub = random.choice(vault['SWEET_KNOWLEDGE_VAULT'][cat])
        return f"{cat}: {sub}"

    def get_context_packet(self):
        # Здесь будет сборка из всех модулей
        packet = {
            "meta": {
                "date": self.date,
                "channel": self.channel,
                "strategy": self.get_strategy_focus(),
                "user_schedule": self.get_user_schedule(),
                "sweet_intel": self.get_sweet_context() if self.channel == "SW" else "N/A",
                "neighbors_intel": self.get_neighbors_context() if self.channel == "NB" else "N/A"
            },
        }
        return packet

    def get_neighbors_context(self):
        """Пункт 100+: Глубокая этнография для канала Neighbors"""
        vault_path = "/home/levdanskiy/.gemini/CORE/knowledge/NEIGHBORS_KNOWLEDGE_VAULT.json"
        if not os.path.exists(vault_path): return "Standard Travel"
        with open(vault_path, 'r') as f:
            vault = json.load(f)
        cat = random.choice(list(vault['NEIGHBORS_KNOWLEDGE_VAULT'].keys()))
        sub = random.choice(vault['NEIGHBORS_KNOWLEDGE_VAULT'][cat])
        return f"{cat}: {sub}"

if __name__ == "__main__":
    engine = ContextEngine("30.01.2026", "AC")
    print(json.dumps(engine.get_context_packet(), indent=4, ensure_ascii=False))
