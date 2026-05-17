#!/usr/bin/env python3
import feedparser
import json
import os

FEEDS_DIR = "/home/levdanskiy/.gemini/ENGINE/feeds/"

def get_space_news():
    url = "https://www.nasa.gov/rss/dyn/breaking_news.rss"
    try:
        feed = feedparser.parse(url)
        news = []
        for entry in feed.entries[:3]:
            news.append({"title": entry.title, "link": entry.link})
        
        with open(os.path.join(FEEDS_DIR, "space_news.json"), 'w') as f:
            json.dump(news, f, indent=2)
            
        print("✅ NASA NEWS:")
        for n in news: print(f"   🚀 {n['title']}")
            
    except Exception as e:
        print(f"❌ NASA Sync Error: {e}")

if __name__ == "__main__":
    get_space_news()
