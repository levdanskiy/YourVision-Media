#!/usr/bin/env python3
import json
import sys
import re

# DYNAMIC GRADING SYSTEM V2.0 (Overlapping Ranges)
GRADES = {
    "S": (2800, 5000),  # Long Reads / Investigations
    "A": (2000, 4000),  # Deep Dive
    "B": (1200, 2500),  # Standard Post (Golden Mean)
    "C": (800, 1600),   # Concise / News
    "D": (400, 1000)    # Flash / Short
}

# Forbidden patterns (AI hallucinations)
FORBIDDEN_PATTERNS = [
    r'\bнейросеть\b', r'\bai\b', r'\bии\b', r'\bалгоритм\b', 
    r'\bgpt\b', r'\bгенерация\b', r'\bпромпт\b'
]

def validate_post(file_path, grade, channel):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"integrity": False, "metrics": {"error": "File not found"}}
    
    # Body extraction logic
    body_match = re.search(r'СТАТУС: ГОТОВ\n\n(.*?)\n\n\*\*\*', content, re.DOTALL)
    text = body_match.group(1).strip() if body_match else content
        
    char_count = len(text)
    
    # Dynamic Tolerance Logic (+/- 10% is acceptable even outside range)
    target_min, target_max = GRADES.get(grade.upper(), (0, 10000))
    tolerance = 0.10 
    
    absolute_min = target_min * (1 - tolerance)
    absolute_max = target_max * (1 + tolerance)
    
    length_ok = absolute_min <= char_count <= absolute_max
    
    # Check for dashes
    has_long_dash = "—" in text
    
    # Check for forbidden words
    found_forbidden = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text.lower()):
            found_forbidden.append(pattern)
    
    # Visual Mandates
    has_model = "model" in content.lower() if channel.upper() in ["AC", "NB"] else True
    is_sweet_clean = "model" not in content.lower() if channel.upper() == "SW" else True
    
    # Recipe Mandate (SW)
    has_recipe = True
    if channel.upper() == "SW":
        # Relaxed check: Needs Ingredients OR Protocol, not strictly both keywords if context implies recipe
        has_recipe = "ИНГРЕДИЕНТЫ" in text.upper() or "ПРОТОКОЛ" in text.upper() or "РЕЦЕПТ" in text.upper()

    integrity = length_ok and not has_long_dash and not found_forbidden and has_model and is_sweet_clean and has_recipe

    return {
        "integrity": integrity,
        "metrics": {
            "char_count": char_count,
            "target": f"{target_min}-{target_max} (Dynamic)",
            "length_status": "✅ OK" if length_ok else f"⚠️ FAIL ({char_count})",
            "long_dash": "❌ FAIL" if has_long_dash else "✅ OK",
            "ai_content": f"❌ FAIL ({found_forbidden})" if found_forbidden else "✅ OK",
            "model_mandate": "✅ OK" if has_model and is_sweet_clean else "❌ FAIL",
            "recipe_mandate": "✅ OK" if has_recipe else "❌ FAIL"
        }
    }

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(json.dumps(validate_post(sys.argv[1], sys.argv[2], sys.argv[3]), indent=4))
