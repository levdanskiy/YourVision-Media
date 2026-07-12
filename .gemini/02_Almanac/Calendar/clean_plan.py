import sys

with open("03_REPORTS/CONTENT_PLAN_2026-06-23_2026-07-31.md", "r") as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if "- **ALMANAC THEME I MIGRATION (EARLY:" in line:
        start_idx = i
        break

end_idx = -1
if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "## WEEK 5:" in lines[i]:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]

# Check Week 5 section for EARLY block
start_idx_2 = -1
for i, line in enumerate(lines):
    if "- **ALMANAC THEME I MIGRATION (EARLY: 21.07" in line:
        start_idx_2 = i
        break

end_idx_2 = -1
if start_idx_2 != -1:
    for i in range(start_idx_2, len(lines)):
        if "- **ALMANAC THEME I MIGRATION (FULL:" in lines[i]:
            end_idx_2 = i
            break

if start_idx_2 != -1 and end_idx_2 != -1:
    del lines[start_idx_2:end_idx_2]

with open("03_REPORTS/CONTENT_PLAN_2026-06-23_2026-07-31.md", "w") as f:
    f.writelines(lines)
