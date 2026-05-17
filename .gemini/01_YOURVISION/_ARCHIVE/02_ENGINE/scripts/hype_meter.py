#!/usr/bin/env python3
import subprocess
import json
import sys

YT_DLP_PATH = "/home/levdanskiy/.gemini/ENGINE/bin/yt-dlp"

def get_video_stats(query):
    """Возвращает статистику первого видео по запросу"""
    cmd = [
        YT_DLP_PATH,
        f"ytsearch1:{query}",
        "--dump-json",
        "--no-playlist",
        "--quiet"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "title": data.get("title", "Unknown"),
                "views": data.get("view_count", 0),
                "likes": data.get("like_count", 0),
                "uploader": data.get("uploader", "Unknown"),
                "url": data.get("webpage_url", "")
            }
        else:
            return {"error": "Search failed"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Eurovision 2026"
    stats = get_video_stats(query)
    print(json.dumps(stats, indent=4))
