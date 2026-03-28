import requests
import json
import os
import html
import re
from datetime import datetime

# BOT CONFIG
BOT_TOKEN = "8687268784:AAEg59N9z0Fryad5MU3lf9BwIXv3RRfi2qg"
CHANNELS = [
    {"id": "70", "username": "@YourEurovision"},
    {"id": "lv", "username": "@almanac_marginalia"}
]

def parse_poll(msg_html):
    try:
        q_match = re.search(r'tgme_widget_message_poll_question">(.*?)</div>', msg_html, re.DOTALL)
        if not q_match: return None
        question = re.sub(r'<[^>]+>', '', q_match.group(1)).strip()
        options = []
        opt_matches = re.findall(r'tgme_widget_message_poll_option_text">(.*?)</div>', msg_html, re.DOTALL)
        for opt in opt_matches:
            options.append(re.sub(r'<[^>]+>', '', opt).strip())
        return {"question": question, "options": options}
    except: return None

def get_telegram_news():
    all_posts = []
    for ch in CHANNELS:
        try:
            url = f"https://t.me/s/{ch['username'].replace('@', '')}?v={datetime.now().timestamp()}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(url, headers=headers, timeout=15)
            messages = res.text.split('<div class="tgme_widget_message ')[1:]
            for msg in messages:
                try:
                    link_match = re.search(r'href="(https://t\.me/[^/]+/(\d+))"', msg)
                    if not link_match: continue
                    post_url = link_match.group(1)
                    date_match = re.search(r'datetime="([^"]+)"', msg)
                    if not date_match: continue
                    dt = datetime.fromisoformat(date_match.group(1).replace('Z', '+00:00'))
                    
                    text_match = re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', msg, re.DOTALL)
                    raw_text = html.unescape(text_match.group(1)) if text_match else ""
                    raw_text = re.sub(r'<br\s*/?>', '\n', raw_text)
                    raw_text = re.sub(r'<[^>]+>', '', raw_text)
                    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
                    title = lines[0] if lines else "Update"
                    body = '\n'.join(lines[1:]) if len(lines) > 1 else ""
                    
                    img_url = ""
                    media_match = re.search(r"background-image:url\(['\"](.*?)['\"]\)", msg)
                    if media_match:
                        temp = media_match.group(1)
                        if "telegram.org/img/emoji" not in temp: img_url = temp
                    
                    vid_url = ""
                    is_video = False
                    video_match = re.search(r'<video[^>]+src=["\']([^"\']+)["\']', msg)
                    if video_match:
                        vid_url = video_match.group(1)
                        is_video = True
                    
                    poll_data = None
                    if "tgme_widget_message_poll" in msg:
                        poll_data = parse_poll(msg)
                        if poll_data: title = "📊 ОПРОС: " + poll_data["question"]
                    
                    all_posts.append({
                        "m": dt.strftime("%d.%m | %H:%M"),
                        "id": ch["id"], "u": post_url, "t": title, "b": body, 
                        "img": img_url, "vid": vid_url, "isVideo": is_video,
                        "ts": dt.timestamp(), "poll": poll_data
                    })
                except: continue
        except: continue
    return all_posts

def sync():
    posts = get_telegram_news()
    posts.sort(key=lambda x: x["ts"], reverse=True)
    final_news = posts[:25]
    
    if os.path.exists("data.js"):
        with open("data.js", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Надежный парсинг через JSON
        match = re.search(r"var DATA = ({.*});", content, re.DOTALL)
        if match:
            data_obj = json.loads(match.group(1))
            data_obj["news"] = final_news
            new_js = "var DATA = " + json.dumps(data_obj, indent=4, ensure_ascii=False) + ";"
            
            with open("data.js", 'w', encoding='utf-8') as f:
                f.write(new_js)
            with open("YourEurovision_Hub_Deploy/data.js", 'w', encoding='utf-8') as f:
                f.write(new_js)
            print("Sync complete. Data is clean.")

if __name__ == "__main__":
    sync()
