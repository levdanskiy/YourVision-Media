import json
import re
import os
import hashlib

HUB_DIR = "/home/levdanskiy/.gemini/01_YOURVISION/08_HUB"
DEPLOY_DIR = "/home/levdanskiy/YourEurovision_Hub_Deploy"

def rebuild():
    # 1. Read index.html from Hub directory (which contains the 2132-line version)
    index_path = os.path.join(HUB_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"ERROR: index.html not found at {index_path}")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. Read data.js to calculate a hash for cache-busting
    data_path = os.path.join(HUB_DIR, "data.js")
    if not os.path.exists(data_path):
        print(f"ERROR: data.js not found at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data_content = f.read()

    # Calculate data hash
    data_hash = hashlib.md5(data_content.encode("utf-8")).hexdigest()[:10]

    # 3. Update the cache-buster version parameter for data.js
    # e.g., src="data.js?v=1775125563" -> src="data.js?v=HASH"
    updated_html = re.sub(
        r'src="data.js\?v=[^"]*"', 
        f'src="data.js?v={data_hash}"', 
        html_content
    )

    # 4. Write back to local Hub directory
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated_html)
    print(f"Updated cache-buster in local Hub index.html (hash: {data_hash})")

    # 5. Write to deploy directory index.html
    if os.path.exists(DEPLOY_DIR):
        deploy_index_path = os.path.join(DEPLOY_DIR, "index.html")
        with open(deploy_index_path, "w", encoding="utf-8") as f:
            f.write(updated_html)
        print(f"Copied updated index.html to deploy directory")

if __name__ == "__main__":
    rebuild()
