import os

# Define the directory to search
root_dir = "/home/levdanskiy/.gemini/02_Almanac/Calendar"

# Define the strings to replace
replacements = {
    "—": "-",
    "–": "-"
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
        if file.endswith(".md") or file.endswith(".yaml") or file.endswith(".txt"):
            filepath = os.path.join(subdir, file)
            process_file(filepath)

print("Replacement complete.")
