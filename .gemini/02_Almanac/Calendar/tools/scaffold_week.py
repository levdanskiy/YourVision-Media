#!/usr/bin/env python3
"""
Scaffolds a week of empty Lexicon posts based on the 4-slot structure:
11:45 (AURORA), 15:15 (ANIMA), 17:15 (LOCUS), 20:15 (MYTHOS).
Usage: python3 tools/scaffold_week.py [YYYY-MM-DD]
Generates 7 days of empty post templates starting from the given date.
"""

import sys
import os
import datetime
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "02_CONTENT"

SLOTS = {
    "11:45": "AURORA",
    "15:15": "ANIMA",
    "17:15": "LOCUS",
    "20:15": "MYTHOS"
}

TEMPLATE = """---
post_id: AL-{short_date}-{time_slug}-{slot_name}
date: {full_date}
slot: "{time}"
rubric: #{rubric_placeholder}
series_id:
status: draft
---

// ИД-ПОСТА: AL-{short_date}-{time_slug}-{slot_name}
// ТЕМА: [Укажите тему]
// ДАТА ПУБЛИКАЦИИ: {full_date}, {time} (Europe/Riga)
// ПРОТОКОЛЫ: Lexicon, {slot_name}
// СТАТУС: DRAFT

[ФЛАГ] **[{slot_name}]: ТЕМА - ПОДТЕМА**

[Текст поста. 4000-6000 символов. Никаких длинных тире.]

---
`⏱ Время чтения: X.X мин | 🏛 Lexicon: {slot_name}`
***

**Grade:** S
**Visual Prompt:** High-end museum archive photography. [Describe the subject]. Shot on Phase One, stark dramatic lighting, clinical and documentary style. No text. {ar_flag} --v 6.1 --style raw --s 750
"""

def generate_week(start_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format.")
        sys.exit(1)

    for i in range(7):
        current_date = start_date + datetime.timedelta(days=i)
        year_str = current_date.strftime("%Y")
        month_str = current_date.strftime("%m")
        day_str = current_date.strftime("%d")
        short_date = f"{day_str}.{month_str}"
        full_date = current_date.strftime("%Y-%m-%d")

        target_dir = CONTENT_DIR / year_str / month_str / day_str
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Scaffolding {full_date}...")
        for time, slot_name in SLOTS.items():
            time_slug = time.replace(":", "-")
            filename = f"LX-{short_date}-{time_slug}-{slot_name}.md"
            filepath = target_dir / filename
            
            if filepath.exists():
                print(f"  Skipping {filename} (already exists)")
                continue
                
            rubric_placeholder = "RUBRIC"
            
            ar_options = ["1:1", "4:5", "16:9", "3:2", "2:3", "9:16", "5:4", "21:9"]
            ar_flag = f"--ar {random.choice(ar_options)}"

            if slot_name == "AURORA":
                rubric_placeholder = "OMENS"
            elif slot_name == "ANIMA": 
                rubric_placeholder = "BESTIARY"
            elif slot_name == "LOCUS": 
                rubric_placeholder = "LOCUS"
            elif slot_name == "MYTHOS": 
                rubric_placeholder = "MORPHOLOGY"

            content = TEMPLATE.format(
                short_date=short_date,
                time_slug=time_slug,
                slot_name=slot_name,
                full_date=full_date,
                time=time,
                rubric_placeholder=rubric_placeholder,
                ar_flag=ar_flag
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Created {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tools/scaffold_week.py YYYY-MM-DD")
        sys.exit(1)
    
    generate_week(sys.argv[1])
