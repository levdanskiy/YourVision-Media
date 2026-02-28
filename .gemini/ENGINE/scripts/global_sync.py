#!/usr/bin/env python3
import requests
import feedparser
import json
import os

FEEDS_DIR = "/home/levdanskiy/.gemini/ENGINE/feeds/"

def sync_news():
    # Billboard и NASA RSS
    feeds = {
        "music_news": "https://www.billboard.com/feed/",
        "nasa_breaking": "https://www.nasa.gov/feed/"
    }
    for name, url in feeds.items():
        feed = feedparser.parse(url)
        entries = [{"title": e.title, "link": e.link} for e in feed.entries[:5]]
        with open(os.path.join(FEEDS_DIR, f"{name}.json"), 'w') as f:
            json.dump(entries, f, indent=2)
    print("✅ Music & Space News Updated.")

def sync_all():
    # Праздники
    r = requests.get("https://date.nager.at/api/v3/NextPublicHolidaysWorldwide")
    if r.status_code == 200:
        with open(os.path.join(FEEDS_DIR, "global_holidays.json"), 'w') as f:
            f.write(r.text)
        print("✅ Global Holidays Updated.")
    
    sync_news()

if __name__ == "__main__":
    sync_all()
