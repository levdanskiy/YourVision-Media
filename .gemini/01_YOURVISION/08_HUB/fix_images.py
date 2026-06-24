import json
import re
import urllib.parse

with open('/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/08_HUB/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to parse the DATA object or just use regex to replace img fields
def replacer(match):
    full_match = match.group(0)
    artist_group = match.group(1) # We need to extract the artist name from the preceding block
    return full_match

# A simpler regex approach: replace ALL "img": "..." with pravatar based on "a": "..."
lines = content.split('\n')
for i in range(len(lines)):
    if '"img":' in lines[i] and '70-heart-sm' in lines[i] or 'flag_' in lines[i]:
        # Look up a few lines to find "a": "Artist Name"
        artist_name = "artist"
        for j in range(i-1, max(-1, i-5), -1):
            if '"a":' in lines[j]:
                m = re.search(r'"a":\s*"([^"]+)"', lines[j])
                if m:
                    artist_name = m.group(1)
                break
        
        # Replace the img line
        safe_name = urllib.parse.quote(artist_name)
        new_url = f"https://i.pravatar.cc/150?u={safe_name}"
        lines[i] = re.sub(r'"img":\s*"[^"]+"', f'"img": "{new_url}"', lines[i])

with open('/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/08_HUB/data.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Images replaced.")
