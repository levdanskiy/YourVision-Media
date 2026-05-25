import os
import re
import json
from collections import Counter

MASTER_PLAN_PATH = ".gemini/TIMELINE/master_plans/03/YV_Plan_03.md"
RUBRICS = ["HERITAGE", "SOURCE", "CALENDAR", "FRAGMENT", "RECIPE", "TEXTS"]
FINALE_RUBRIC = "ALMANAC_FINALE"

def get_rubric_counts():
    if not os.path.exists(MASTER_PLAN_PATH):
        return {r: 0 for r in RUBRICS}
    
    with open(MASTER_PLAN_PATH, 'r') as f:
        content = f.read()
    
    counts = Counter(re.findall(r"#(HERITAGE|SOURCE|CALENDAR|FRAGMENT|RECIPE|TEXTS)", content))
    return {r: counts.get(r, 0) for r in RUBRICS}

def suggest_next_rubric():
    counts = get_rubric_counts()
    # Find rubrics with the minimum count
    min_count = min(counts.values())
    candidates = [r for r, c in counts.items() if c == min_count]
    return candidates

if __name__ == "__main__":
    counts = get_rubric_counts()
    candidates = suggest_next_rubric()
    print(json.dumps({"counts": counts, "next_candidates": candidates}, indent=2, ensure_ascii=False))
