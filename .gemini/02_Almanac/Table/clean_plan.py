import sys

with open("01_BIBLES/PLAN_JULY.md", "r") as f:
    lines = f.readlines()

# Find start of 16.07
start_idx = -1
for i, line in enumerate(lines):
    if "### 📅 16.07" in line:
        start_idx = i
        break

# Find end of 22.07 (which is the start of 23.07)
end_idx = -1
for i, line in enumerate(lines):
    if "### 📅 23.07" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]
    
    # Insert a placeholder
    lines.insert(start_idx, "### [16.07 - 22.07 ОСТАВЛЕНО ДЛЯ ПЛАНИРОВАНИЯ ПЕРЕХОДА ОБОИХ КАНАЛОВ]\n\n")

with open("01_BIBLES/PLAN_JULY.md", "w") as f:
    f.writelines(lines)
