#!/usr/bin/env python3
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ContentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            print(f"📁 New post detected: {event.src_path}")
            # Запускаем скрипт синхронизации статусов
            subprocess.run(["python3", "/home/levdanskiy/.gemini/ENGINE/scripts/sync_status.py"])

if __name__ == "__main__":
    path = "/home/levdanskiy/.gemini/CONTENT/posts"
    event_handler = ContentHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    print(f"🚦 Status Watchdog started on {path}")
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
