import os
import re

BASE_DIR = "/home/levdanskiy/.gemini"
WORKFLOW_DIR = os.path.join(BASE_DIR, "TIMELINE/daily_workflow")
MASTER_PLANS_DIR = os.path.join(BASE_DIR, "TIMELINE/master_plans/02")
CONTENT_DIR = os.path.join(BASE_DIR, "CONTENT/posts")

STATUS_PENDING = "⬜ [ОЖИДАНИЕ]"
STATUS_DONE = "✅ [ГОТОВО]"

def get_all_post_keys():
    """Returns a set of (channel, date, time, tag) tuples for existing posts."""
    keys = set()
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if not file.endswith(".md"): continue
            file_path = os.path.join(root, file)
            try:
                filename = os.path.basename(file)
                # Channel-DD.MM-HH-MM
                channel_match = re.match(r"^([A-Z]+)-", filename)
                date_match = re.search(r"-(\d{2}\.\d{2})-", filename)
                time_match = re.search(r"-\d{2}\.\d{2}-(\d{2})[-.](\d{2})", filename)
                
                if channel_match and date_match and time_match:
                    channel = channel_match.group(1).upper()
                    date_str = date_match.group(1)
                    time_str = f"{time_match.group(1)}:{time_match.group(2)}"
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)
                    
                    topic_match = re.search(r"#([A-Z_]+):", content)
                    if topic_match:
                        tag = topic_match.group(1).upper()
                        keys.add((channel, date_str, time_str, tag))
            except:
                continue
    return keys

def cleanup_file(file_path, existing_keys):
    if not os.path.exists(file_path): return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    updated = False
    new_lines = []
    current_date = None
    
    file_date_match = re.search(r"daily_plan_(\d{2}\.\d{2})", os.path.basename(file_path))
    file_date = file_date_match.group(1) if file_date_match else None

    for line in lines:
        date_header_match = re.search(r"### (\d{2}\.\d{2})", line)
        if date_header_match:
            current_date = date_header_match.group(1)
        
        target_date = file_date or current_date
        
        if STATUS_DONE in line:
            time_match = re.search(r"(\d{2}:\d{2})", line)
            tag_match = re.search(r"#(\w+)", line)
            channel_match = re.search(r"\*\*([A-Z]{2})\*\*", line) # Match **AC**, **NB**, **SW**
            
            if time_match and tag_match and channel_match and target_date:
                time_val = time_match.group(1)
                tag_val = tag_match.group(1).upper()
                channel_val = channel_match.group(1).upper()
                
                if (channel_val, target_date, time_val, tag_val) not in existing_keys:
                    line = line.replace(STATUS_DONE, STATUS_PENDING)
                    updated = True
                    print(f"  [FIXED] {os.path.basename(file_path)}: {channel_val} {target_date} {time_val} {tag_val} -> WAITING")
        
        new_lines.append(line)
        
    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    print("--- 🛡️ EMERGENCY STATUS CLEANUP V2 (CHANNEL AWARE) ---")
    existing_keys = get_all_post_keys()
    print(f"Found {len(existing_keys)} valid posts in CONTENT.")
    
    for f in os.listdir(WORKFLOW_DIR):
        if f.endswith(".md"): cleanup_file(os.path.join(WORKFLOW_DIR, f), existing_keys)
            
    for f in os.listdir(MASTER_PLANS_DIR):
        if f.endswith(".md"): cleanup_file(os.path.join(MASTER_PLANS_DIR, f), existing_keys)
            
    print("--- ✅ CLEANUP COMPLETE ---")

if __name__ == "__main__":
    main()