#!/usr/bin/env python3
import requests
import json
import sys

def fetch_lore(query, lang="ru"):
    """Ищет краткую справку по теме в Википедии"""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {
                "title": data.get("title"),
                "extract": data.get("extract"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page")
            }
    except:
        pass
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lore_synthesizer.py [QUERY]")
        sys.exit(1)
    
    result = fetch_lore(sys.argv[1])
    if result:
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("Ничего не найдено.")
