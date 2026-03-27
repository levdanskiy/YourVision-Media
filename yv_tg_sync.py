import requests
import json
import os
import html
import re
import subprocess
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

def sync():
    tg_posts = get_telegram_news()
    tg_posts = [p for p in tg_posts if p["t"] and p["ts"]]
    tg_posts.sort(key=lambda x: x["ts"], reverse=True)
    final_news = tg_posts[:25]
    
    if os.path.exists("data.js"):
        with open("data.js", 'r', encoding='utf-8') as f:
            js_content = f.read()
            match = re.search(r'var DATA = (\{.*\});', js_content, re.DOTALL)
            if match:
                data_obj = json.loads(match.group(1))
                data_obj["news"] = final_news
                new_js = f"var DATA = {json.dumps(data_obj, ensure_ascii=False, indent=4)};"
                new_js = new_js.replace("...", ".").replace('—', '-').replace('–', '-')
                
                # Обновляем data.js в корне
                with open("data.js", 'w', encoding='utf-8') as f:
                    f.write(new_js)
                
                # Обновляем data.js в деплое
                deploy_path = "YourEurovision_Hub_Deploy/data.js"
                with open(deploy_path, 'w', encoding='utf-8') as f:
                    f.write(new_js)
                
                # Выполняем авто-пуш в деплой-репозиторий
                try:
                    os.chdir("YourEurovision_Hub_Deploy")
                    subprocess.run(["git", "add", "data.js"], check=True)
                    subprocess.run(["git", "commit", "-m", "auto: update news data via bot sync"], check=True)
                    subprocess.run(["git", "push"], check=True)
                    os.chdir("..")
                    print("Deploy Sync Complete: data.js pushed to YourEurovision-Hub.")
                except Exception as e:
                    os.chdir("..")
                    print(f"Deploy Push Error: {e}")

if __name__ == "__main__":
    sync()
