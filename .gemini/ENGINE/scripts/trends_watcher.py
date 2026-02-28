#!/usr/bin/env python3
import json
import trafilatura
from duckduckgo_search import DDGS
import sys

def audit_trends():
    print("🕵️ Starting System Audit: Visual & Textual Trends...")
    queries = [
        "Midjourney latest parameters 2026",
        "Vogue high fashion text style trends 2026",
        "Graphic design color of the month February 2026"
    ]
    
    audit_results = {}
    with DDGS() as ddgs:
        for q in queries:
            res = list(ddgs.text(q, max_results=1))
            if res:
                audit_results[q] = res[0]['title']
                
    return audit_results

if __name__ == "__main__":
    if "--audit" in sys.argv:
        print(json.dumps(audit_trends(), indent=4))
    else:
        # Старая логика Google Trends
        pass