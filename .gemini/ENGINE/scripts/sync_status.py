import os
import re
from datetime import datetime, timedelta

BASE_DIR = "/home/levdanskiy/.gemini"
CONTENT_DIR = os.path.join(BASE_DIR, "CONTENT/posts")
WORKFLOW_DIR = os.path.join(BASE_DIR, "TIMELINE/daily_workflow")
MASTER_PLANS_DIR = os.path.join(BASE_DIR, "TIMELINE/master_plans")

STATUS_PENDING = "⬜ [ОЖИДАНИЕ]"
STATUS_DONE = "✅ [ГОТОВО]"

def get_recent_posts(hours=72):
    posts = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    if not os.path.exists(CONTENT_DIR): return []
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    if datetime.fromtimestamp(os.path.getmtime(file_path)) > cutoff_time:
                        posts.append(file_path)
                except: continue
    return posts

def extract_post_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read(1000)
    filename = os.path.basename(file_path)
    
    # 1. Channel (AC, NB, SW, YV)
    channel_match = re.match(r"^([A-Z]+)-", filename)
    channel = channel_match.group(1).upper() if channel_match else ""

    # 2. Date (DD.MM)
    date_match = re.search(r"-(\d{2}\.\d{2})-", filename)
    date_str = date_match.group(1) if date_match else None

    # 3. Time (HH:MM)
    time_match = re.search(r"-\d{2}\.\d{2}-(\d{2})[-.](\d{2})", filename)
    time_str = f"{time_match.group(1)}:{time_match.group(2)}" if time_match else ""
    
    # 4. Rubric Tag
    tag_match = re.search(r"#([A-Z_]+):", content)
    rubric_tag = tag_match.group(1).upper() if tag_match else ""

    return {
        'channel': channel,
        'date': date_str,
        'time': time_str,
        'rubric_tag': rubric_tag
    }

def update_file_status(file_path, info):
    if not os.path.exists(file_path): return False
    target_date = info['date']
    if not target_date: return False

    is_daily = "daily_plan_" in os.path.basename(file_path)
    if is_daily:
        if f"daily_plan_{target_date}.md" != os.path.basename(file_path):
            return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    updated = False
    new_lines = []
    current_section_date = None
    
    for line in lines:
        date_header_match = re.search(r"### (\d{2}\.\d{2})", line)
        if date_header_match:
            current_section_date = date_header_match.group(1)
        
        if STATUS_PENDING in line and info['time'] in line:
            # Check Date
            date_ok = is_daily or (current_section_date == target_date)
            
            # Check Channel (NEW)
            channel_ok = info['channel'] in line.upper()
            
            # Check Rubric
            rubric_ok = True
            if info['rubric_tag']:
                rubric_ok = info['rubric_tag'] in line.upper().replace('_', '') or info['rubric_tag'].replace('_', '') in line.upper().replace('_', '')

            if date_ok and channel_ok and rubric_ok:
                new_line = line.replace(STATUS_PENDING, STATUS_DONE)
                if new_line != line:
                    new_lines.append(new_line)
                    updated = True
                    print(f"  [UPDATED] {os.path.basename(file_path)}: {info['time']} {info['channel']} {info['rubric_tag']} -> DONE")
                    continue

        new_lines.append(line)

    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    print("--- 🔄 STATUS SYNC V6.0 (CHANNEL AWARE) ---")
    recent_posts = get_recent_posts()
    for post_path in recent_posts:
        info = extract_post_info(post_path)
        if not info['time'] or not info['date'] or not info['channel']: continue
        
        # 1. Update daily workflow
        if os.path.exists(WORKFLOW_DIR):
            for f in os.listdir(WORKFLOW_DIR):
                if f.endswith(".md"): update_file_status(os.path.join(WORKFLOW_DIR, f), info)
        
        # 2. Update master plans
        if os.path.exists(MASTER_PLANS_DIR):
            for root, _, files in os.walk(MASTER_PLANS_DIR):
                for f in files:
                    if f.endswith(".md"): update_file_status(os.path.join(root, f), info)

if __name__ == "__main__":
    main()