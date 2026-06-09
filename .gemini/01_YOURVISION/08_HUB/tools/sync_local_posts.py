#!/usr/bin/env python3
"""
sync_local_posts.py - Подтягивает локальные .md-посты из 04_CONTENT/ в Hub data.js.news[].

Параллельно с yv_tg_sync.py (cron), который тянет посты из Telegram.

Логика:
- Читает все .md из 04_CONTENT/YYYY/MM/DD/ за последние LOOKBACK_DAYS дней
- Парсит header (ИД-ПОСТА, ТЕМА, ДАТА ПУБЛИКАЦИИ) + body (всё между --- и футером)
- Извлекает H1 (первая строка с **bold** после header)
- Формирует news-объекты с id="local" (отличается от TG-постов с id="70")
- Сливает с существующим news[]:
  * Сохраняет TG-посты (id != "local")
  * Заменяет старые локальные на свежие (по ИД-ПОСТА)
  * Сортирует по ts desc, обрезает до MAX_NEWS

Запускать вручную после написания/правки локального поста, либо из pre-commit.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HUB_DIR = Path("/home/levdanskiy/.gemini/01_YOURVISION/08_HUB")
DEPLOY_DIR = Path("/home/levdanskiy/YourEurovision_Hub_Deploy")
CONTENT_ROOT = Path("/home/levdanskiy/.gemini/01_YOURVISION/04_CONTENT")
RIGA_TZ = timezone(timedelta(hours=3))  # EEST UTC+3
LOOKBACK_DAYS = 30
MAX_NEWS = 25
LOCAL_ID = "local"

HEADER_RE = re.compile(r"//\s*([А-ЯA-Z\- ]+?):\s*(.+)")
BODY_SPLIT_RE = re.compile(r"^---\s*$", re.MULTILINE)


def parse_post(path: Path):
    """Return dict with parsed fields or None if file is invalid."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    header = {}
    body_start = 0
    for i, line in enumerate(text.split("\n")):
        m = HEADER_RE.match(line.strip())
        if m:
            header[m.group(1).strip()] = m.group(2).strip()
        elif line.startswith("//"):
            continue
        elif line.strip() == "":
            body_start = i + 1
            continue
        else:
            body_start = i
            break

    raw_body = "\n".join(text.split("\n")[body_start:])

    parts = BODY_SPLIT_RE.split(raw_body)
    if len(parts) < 2:
        return None

    h1 = parts[0].strip()
    middle = "---".join(parts[1:-1]) if len(parts) > 2 else parts[1]

    h1_match = re.search(r"(\S+)\s+\*\*(.+?)\*\*", h1)
    if h1_match:
        flag = h1_match.group(1)
        title_text = h1_match.group(2).strip()
        title = f"{flag} {title_text}"
    else:
        title = h1.replace("**", "").strip()

    body_lines = []
    for line in middle.split("\n"):
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith("**Grade:") or clean.startswith("**Prompt:"):
            break
        if clean.startswith("`⏱") or clean.startswith("`Время чтения"):
            continue
        body_lines.append(clean)
    body = "\n".join(body_lines).strip()

    ts = None
    date_str = header.get("ДАТА ПУБЛИКАЦИИ", "")
    date_match = re.match(r"(\d{2})\.(\d{2})\.(\d{4}),?\s+(\d{2}):(\d{2})", date_str)
    if date_match:
        day, month, year, hour, minute = map(int, date_match.groups())
        dt = datetime(year, month, day, hour, minute, tzinfo=RIGA_TZ)
        ts = dt.timestamp()
        m_str = dt.strftime("%d.%m | %H:%M")
    else:
        return None

    return {
        "post_id": header.get("ИД-ПОСТА", path.stem),
        "m": m_str,
        "id": LOCAL_ID,
        "u": "",
        "t": title,
        "b": body,
        "img": "",
        "vid": "",
        "isVideo": False,
        "ts": ts,
        "poll": None,
    }


def collect_local_posts(lookback_days=LOOKBACK_DAYS):
    """Walk 04_CONTENT, return list of news-objects."""
    now = datetime.now(tz=RIGA_TZ)
    cutoff = now - timedelta(days=lookback_days)
    posts = []
    for md_path in CONTENT_ROOT.rglob("YV-*.md"):
        parsed = parse_post(md_path)
        if not parsed:
            continue
        if parsed["ts"] < cutoff.timestamp():
            continue
        if parsed["ts"] > now.timestamp():
            # Skip future/scheduled posts that are not yet published to Telegram
            continue
        posts.append(parsed)
    return posts


def merge_with_existing(existing_news, local_posts):
    """Keep TG news (id != local), replace local entries by post_id key,
    and filter out duplicate local posts using a normalized title check.
    """
    tg_news = [n for n in existing_news if n.get("id") != LOCAL_ID]

    def normalize_title(title):
        if not title:
            return ""
        return re.sub(r'[^\w\s]', '', title).lower().strip()

    tg_normalized = {normalize_title(p.get("t", "")) for p in tg_news}

    local_by_id = {p["post_id"]: p for p in local_posts}
    locals_out = []
    for lp in local_by_id.values():
        if normalize_title(lp.get("t", "")) not in tg_normalized:
            locals_out.append(lp)

    merged = tg_news + locals_out
    merged.sort(key=lambda x: x.get("ts", 0), reverse=True)
    merged = merged[:MAX_NEWS]

    for item in merged:
        item.pop("post_id", None)
    return merged


def write_data_js(data_obj):
    new_js = "var DATA = " + json.dumps(data_obj, indent=4, ensure_ascii=False) + ";"
    for path in (HUB_DIR / "data.js", DEPLOY_DIR / "data.js"):
        path.write_text(new_js, encoding="utf-8")


def main():
    data_path = HUB_DIR / "data.js"
    if not data_path.exists():
        print(f"ERROR: {data_path} not found", file=sys.stderr)
        sys.exit(1)

    content = data_path.read_text(encoding="utf-8")
    match = re.search(r"var DATA = ({.*});", content, re.DOTALL)
    if not match:
        print("ERROR: var DATA = {...} not parsed", file=sys.stderr)
        sys.exit(1)

    data_obj = json.loads(match.group(1))
    existing_news = data_obj.get("news", [])

    local_posts = collect_local_posts()
    if not local_posts:
        print("No local posts in lookback window. Nothing to sync.")
        return

    merged = merge_with_existing(existing_news, local_posts)
    data_obj["news"] = merged

    write_data_js(data_obj)

    print(f"Synced {len(local_posts)} local posts.")
    print(f"Total news[] size: {len(merged)} ({sum(1 for n in merged if n['id'] == LOCAL_ID)} local / {sum(1 for n in merged if n['id'] != LOCAL_ID)} TG).")

    # Automatically trigger rebuild_perfect.py to update index.html with new cache-buster
    try:
        import subprocess
        rebuild_script = "/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/tools/rebuild_perfect.py"
        if os.path.exists(rebuild_script):
            subprocess.run(["python3", rebuild_script], check=True)
        else:
            rebuild_script_alt = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/08_HUB/tools/rebuild_perfect.py"
            subprocess.run(["python3", rebuild_script_alt], check=True)
    except Exception as e:
        print(f"Error running rebuild_perfect.py: {e}")


if __name__ == "__main__":
    main()
