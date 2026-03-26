import requests
import re
import json
import os
import html
from datetime import datetime

CHANNELS = [
    {"id": "70", "url": "https://t.me/s/YourEurovision"},
    {"id": "lv", "url": "https://t.me/s/almanac_marginalia"}
]

def parse_channel(channel_info):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        res = requests.get(channel_info["url"], headers=headers, timeout=15)
        res_html = res.text
    except:
        return []
    
    posts = []
    # Split by message start tag
    messages = re.split(r'<div class="tgme_widget_message ', res_html)[1:]
    
    for msg in messages:
        try:
            # 1. Message Link (from the date anchor)
            link_match = re.search(r'class="tgme_widget_message_date"[^>]+href="(https://t\.me/[^/]+/(\d+))"', msg)
            if not link_match:
                # Try general message link search
                link_match = re.search(r'href="(https://t\.me/[^/]+/(\d+))"', msg)
            
            if not link_match: continue
            post_url = link_match.group(1)
            
            # 2. Date
            date_match = re.search(r'datetime="([^"]+)"', msg)
            if not date_match: continue
            dt = datetime.fromisoformat(date_match.group(1).replace('Z', '+00:00'))
            date_str = dt.strftime("%d.%m | %H:%M")
            
            # 3. Text
            text_match = re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', msg, re.DOTALL)
            raw_text = text_match.group(1) if text_match else ""
            
            raw_text = html.unescape(raw_text)
            raw_text = re.sub(r'<br\s*/?>', '\n', raw_text)
            raw_text = re.sub(r'<[^>]+>', '', raw_text)
            
            # 4. Title and Body
            lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
            title = lines[0] if lines else "Update"
            body = '\n'.join(lines[1:]) if len(lines) > 1 else ""
            
            # 5. Media Detection
            img_url = ""
            is_video = False
            
            # Check for various video indicators
            if 'tgme_widget_message_video_player' in msg or 'tgme_widget_message_roundvideo_player' in msg:
                is_video = True
            
            # Extract background image (thumbnail)
            media_match = re.search(r"background-image:url\(['\"](.*?)['\"]\)", msg)
            if media_match:
                img_url = media_match.group(1)

            posts.append({
                "m": date_str,
                "id": channel_info["id"],
                "u": post_url,
                "t": title,
                "b": body,
                "img": img_url,
                "isVideo": is_video,
                "ts": dt.timestamp()
            })
        except:
            continue
    return posts

def sync():
    all_posts = []
    for ch in CHANNELS:
        posts = parse_channel(ch)
        print(f"Found {len(posts)} posts in {ch['id']}")
        all_posts.extend(posts)
    
    if not all_posts:
        return

    # Sort newest first
    all_posts.sort(key=lambda x: x["ts"], reverse=True)
    final_posts = all_posts[:20]
    
    clean_posts = []
    for p in final_posts:
        clean_posts.append({
            "m": p["m"],
            "id": p["id"],
            "u": p["u"],
            "t": p["t"],
            "b": p["b"],
            "img": p["img"],
            "isVideo": p["isVideo"]
        })

    news_json = json.dumps(clean_posts, ensure_ascii=False, indent=4)
    
    files = ["YV_Editor_Hub.html", "YourEurovision_Hub_Deploy/index.html"]
    for file_path in files:
        if not os.path.exists(file_path): continue
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'(news:\s*\[)', content)
        if not match: continue
            
        start_idx = match.start()
        array_start = match.end() - 1
        
        depth = 0
        end_idx = -1
        for i in range(array_start, len(content)):
            if content[i] == '[': depth += 1
            elif content[i] == ']':
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
        
        if end_idx != -1:
            new_content = content[:start_idx] + f"news: {news_json}" + content[end_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    sync()
