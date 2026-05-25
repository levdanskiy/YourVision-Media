#!/usr/bin/env python3
import json
import trafilatura
from duckduckgo_search import DDGS
import sys

def deep_research(query, max_results=3):
    results = []
    try:
        with DDGS() as ddgs:
            # Новый синтаксис
            search_results = ddgs.text(query, max_results=max_results)
            
            for res in search_results:
                url = res['href']
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    content = trafilatura.extract(downloaded)
                    if content:
                        results.append({
                            "url": url,
                            "title": res['title'],
                            "content": content[:1500]
                        })
    except Exception as e:
        return [{"error": str(e)}]
    
    return results

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Eurovision 2026 news"
    print(json.dumps(deep_research(query), indent=4, ensure_ascii=False))