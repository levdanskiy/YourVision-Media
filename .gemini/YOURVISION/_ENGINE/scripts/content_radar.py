import os
import sqlite3
import requests
import json
from datetime import datetime

# Конфигурация
DB_PATH = '/home/levdanskiy/.gemini/TIMELINE/database/content_plan.db'
BRAVE_KEY = 'BSAs5mEJGWIbVKE3uP9mrbHzHieSzmx'
GITHUB_TOKEN = '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'

KEYWORDS = {
    'YV': ['Eurovision 2026 news', 'Melodifestivalen snippets', 'Sanremo results'],
    'SW': ['pastry trends 2026', 'chocolate innovation', 'michelin star desserts'],
    'AC': ['architectural milestones 2026', 'sacred geometry symbols', 'historical mysteries'],
    'NB': ['folk festivals February 2026', 'traditional costume exhibition', 'local spirit Menton']
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ideas (id INTEGER PRIMARY KEY AUTOINCREMENT, concept TEXT, channel TEXT, priority INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_idea(concept, channel):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ideas (concept, channel, priority) VALUES (?, ?, ?)", (concept, channel, 1))
        conn.commit()
    except Exception as e:
        print(f"Error saving: {e}")
    conn.close()

def search_brave(query):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {"Accept": "application/json", "X-Subscription-Token": BRAVE_KEY}
    params = {"q": query, "count": 3}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('web', {}).get('results', [])
    except:
        return []
    return []

def get_github_trends():
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"q": "topic:creative-coding", "sort": "stars", "order": "desc", "per_page": 3}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
    except:
        return []
    return []

def main():
    init_db()
    print(f"--- 📡 CONTENT RADAR SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M')} ---")
    
    # 1. Поиск новостей
    for channel, queries in KEYWORDS.items():
        print(f"Scanning for {channel}...")
        for q in queries:
            results = search_brave(q)
            for res in results:
                concept = f"{res['title']}: {res['url']}"
                save_idea(concept, channel)
                print(f"  [+] Idea found: {res['title'][:50]}...")

    # 2. GitHub Тренды
    print("Checking GitHub Trends...")
    repos = get_github_trends()
    for repo in repos:
        concept = f"GitHub Trend: {repo['name']} - {repo['description']} ({repo['html_url']})"
        save_idea(concept, "AC")
        print(f"  [+] Repo found: {repo['name']}")

    print("\n--- 🏁 SCAN COMPLETE. All ideas saved to SQLite. ---")

if __name__ == "__main__":
    main()
