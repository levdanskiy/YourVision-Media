#!/usr/bin/env python3
import os
import sys
import subprocess

KNOWLEDGE_DIR = "/home/levdanskiy/.gemini/CORE/knowledge/"

def harvest_repo(repo_url, target_file=None):
    """Clones a repo or downloads a specific file from GitHub."""
    print(f"⛏️ **HARVESTING DATA FROM:** {repo_url}")
    
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    temp_dir = f"/home/levdanskiy/.gemini/tmp/{repo_name}"
    
    try:
        # Use git to clone into tmp
        subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], check=True)
        
        if target_file:
            # Copy specific file to knowledge
            source = os.path.join(temp_dir, target_file)
            dest = os.path.join(KNOWLEDGE_DIR, target_file)
            if os.path.exists(source):
                subprocess.run(["cp", source, dest], check=True)
                print(f"✅ FILE HARVESTED: {target_file}")
        else:
            print(f"✅ REPO CLONED TO TMP: {temp_dir}")
            
    except Exception as e:
        print(f"❌ HARVEST FAILED: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 repo_harvester.py <repo_url> [target_file]")
        sys.exit(1)
    
    url = sys.argv[1]
    file = sys.argv[2] if len(sys.argv) > 2 else None
    harvest_repo(url, file)
