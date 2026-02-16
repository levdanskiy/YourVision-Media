import sys
import os
import json

# Список доверенных источников (The Holy Grail of ESC News)
TRUSTED_SOURCES = [
    "eurovisionworld.com",
    "eurovoix.com",
    "wiwibloggs.com",
    "escxtra.com",
    "eurovision.tv"
]

def scout_esc(query):
    # В будущем здесь будет прямой вызов mcp-cli brave-search
    # Сейчас создаем структуру запроса для Gemini, чтобы он знал где искать
    search_prompt = f"site:{' OR site:'.join(TRUSTED_SOURCES)} {query}"
    
    scout_report = {
        "status": "READY",
        "search_logic": search_prompt,
        "targets": ["Betting Odds", "Rehearsal Clips", "National Final Results"],
        "mandate": "ZERO HALLUCINATION. If data not found on these sites, report failure."
    }
    return scout_report

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "National Finals 2026 results"
    print(json.dumps(scout_esc(query), indent=4))
