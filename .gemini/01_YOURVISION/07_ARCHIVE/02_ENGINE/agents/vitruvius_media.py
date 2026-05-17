#!/usr/bin/env python3
import os
import glob
import shutil
import sys

DOWNLOADS_PATH = "/home/levdanskiy/Загрузки/"
MEDIA_VAULT = "/home/levdanskiy/.gemini/CONTENT/media/"

def link_latest_image(post_id):
    """
    Finds the most recent image in Downloads and moves it to the Media Vault
    with the name of the post_id.
    """
    types = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    files = []
    for t in types:
        files.extend(glob.glob(os.path.join(DOWNLOADS_PATH, t)))
    
    if not files:
        return "❌ ERROR: No images found in Downloads."
    
    # Sort by modification time
    latest_file = max(files, key=os.path.getmtime)
    extension = os.path.splitext(latest_file)[1]
    new_name = f"{post_id}{extension}"
    dest_path = os.path.join(MEDIA_VAULT, new_name)
    
    shutil.move(latest_file, dest_path)
    return f"✅ ASSET LINKED: {latest_file} -> {dest_path}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vitruvius_media.py <post_id>")
    else:
        print(link_latest_image(sys.argv[1]))
