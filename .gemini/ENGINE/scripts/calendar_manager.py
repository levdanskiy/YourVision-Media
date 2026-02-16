#!/usr/bin/env python3
import sqlite3
import sys
import datetime
import os

DB_PATH = "/home/levdanskiy/.gemini/CORE/calendar.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY, title TEXT, start_time TEXT, end_time TEXT, description TEXT)''')
    conn.commit()
    conn.close()

def add_event(title, start_time, duration_mins=60):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Парсим время (ожидаем формат YYYY-MM-DD HH:MM)
        start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end = start + datetime.timedelta(minutes=int(duration_mins))
        
        c.execute("INSERT INTO events (title, start_time, end_time) VALUES (?, ?, ?)",
                  (title, start.isoformat(), end.isoformat()))
        conn.commit()
        print(f"✅ Event added: {title} at {start}")
    except ValueError:
        print("❌ Error: Date format must be YYYY-MM-DD HH:MM")
    finally:
        conn.close()

def list_events(days=7):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.datetime.now()
    limit = now + datetime.timedelta(days=days)
    
    c.execute("SELECT title, start_time FROM events WHERE start_time BETWEEN ? AND ? ORDER BY start_time",
              (now.isoformat(), limit.isoformat()))
    
    events = c.fetchall()
    conn.close()
    
    if not events:
        print("📭 No upcoming events.")
        return []
        
    result = []
    print(f"📅 Upcoming events ({days} days):")
    for e in events:
        print(f"  • {e[1].replace('T', ' ')}: {e[0]}")
        result.append(f"{e[1]}: {e[0]}")
    return result

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 2:
        if sys.argv[1] == "add":
            add_event(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else 60)
        elif sys.argv[1] == "list":
            list_events()
    else:
        list_events()
