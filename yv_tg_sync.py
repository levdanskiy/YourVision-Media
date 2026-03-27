import requests
import json
import os
import html
import re
from datetime import datetime

# BOT CONFIG
BOT_TOKEN = "8687268784:AAEg59N9z0Fryad5MU3lf9BwIXv3RRfi2qg"
CHANNELS = [
    {"id": "70", "username": "@YourEurovision", "path": ".gemini/CONTENT/posts/"},
    {"id": "lv", "username": "@almanac_marginalia", "path": ".gemini/CONTENT/almanac/"}
]

def get_telegram_news():
    all_posts = []
    for ch in CHANNELS:
        try:
            url = f"https://t.me/s/{ch['username'].replace('@', '')}?v={datetime.now().timestamp()}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(url, headers=headers, timeout=15)
            res_html = res.text
            
            messages = res_html.split('<div class="tgme_widget_message ')[1:]
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
                    if media_match: img_url = media_match.group(1)

                    all_posts.append({
                        "m": dt.strftime("%d.%m | %H:%M"),
                        "id": ch["id"], "u": post_url, "t": title, "b": body, "img": img_url, "ts": dt.timestamp()
                    })
                except: continue
        except: continue
    return all_posts

def get_local_posts():
    local_posts = []
    now = datetime.now()
    # Проверяем последние 3 дня
    for i in range(3):
        date_seg = (datetime.now()).strftime("%Y/%m/%d") # Упростим для теста
        for ch in CHANNELS:
            # Рекурсивный поиск в папке канала
            base_path = ch["path"]
            if not os.path.exists(base_path): continue
            for root, dirs, files in os.walk(base_path):
                for filename in files:
                    if not filename.endswith(".md"): continue
                    try:
                        with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                            content = f.read()
                        if "// СТАТУС: ГОТОВ" not in content: continue
                        
                        date_match = re.search(r'ДАТА ПУБЛИКАЦИИ:\s*(\d{2}\.\d{2}\.\d{4},\s*\d{2}:\d{2})', content)
                        if not date_match: continue
                        pub_dt = datetime.strptime(date_match.group(1), "%d.%m.%Y, %H:%M")
                        
                        header_end = content.find('\n\n')
                        body_start = content.find('---', header_end)
                        raw_body = content[header_end:body_start].strip()
                        lines = [l.strip() for l in raw_body.split('\n') if l.strip()]
                        
                        local_posts.append({
                            "m": pub_dt.strftime("%d.%m | %H:%M"),
                            "id": ch["id"], "u": "https://t.me/" + ch["username"].replace('@', ''), 
                            "t": lines[0] if lines else "Update", 
                            "b": '\n'.join(lines[1:]) if len(lines) > 1 else "",
                            "ts": pub_dt.timestamp()
                        })
                    except: continue
    return local_posts

def sync():
    tg_posts = get_telegram_news()
    local_posts = get_local_posts()
    
    titles_in_tg = set([p["t"] for p in tg_posts])
    for lp in local_posts:
        if lp["t"] not in titles_in_tg:
            tg_posts.append(lp)
            
    tg_posts.sort(key=lambda x: x["ts"], reverse=True)
    final_news = tg_posts[:25]
    
    # Читаем текущий DATA из data.js, чтобы сохранить Battles и Chart
    if os.path.exists("data.js"):
        with open("data.js", 'r', encoding='utf-8') as f:
            js_content = f.read()
            # Извлекаем объект DATA через regex
            match = re.search(r'var DATA = (\{.*\});', js_content, re.DOTALL)
            if match:
                data_obj = json.loads(match.group(1))
                data_obj["news"] = final_news
                
                new_js = f"var DATA = {json.dumps(data_obj, ensure_ascii=False, indent=4)};"
                with open("data.js", 'w', encoding='utf-8') as f:
                    f.write(new_js)
                print(f"Updated data.js with {len(final_news)} mixed items (YV + Almanac)")

if __name__ == "__main__":
    sync()
