import os

CONTENT_DIR = ".gemini/CONTENT/posts"

def sanitize_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Замена всех длинных и средних тире на дефисы (МАНДАТ)
    new_content = content.replace("—", "-").replace("–", "-")
    
    if content != new_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Sanitized: {os.path.basename(filepath)}")
    else:
        print(f"Clean: {os.path.basename(filepath)}")

def main():
    print("--- STARTING CONTENT SANITIZATION ---")
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                sanitize_file(os.path.join(root, file))
    print("--- SANITIZATION COMPLETE ---")

if __name__ == "__main__":
    main()