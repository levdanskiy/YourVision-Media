import os

root_dir = "/home/levdanskiy/.gemini/02_Almanac/Calendar"

replacements = {
    "CONFINIUM": "LEXICON",
    "Confinium": "Lexicon",
    "confinium": "lexicon",
    "CF-": "LX-"
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = content
        for old_str, new_str in replacements.items():
            modified = modified.replace(old_str, new_str)
            
        if modified != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith((".md", ".yaml", ".txt", ".py")):
            # Don't edit this script itself just in case
            if file == "replace_name.py":
                continue
            filepath = os.path.join(subdir, file)
            process_file(filepath)

print("Name replacement complete.")
