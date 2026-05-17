import sys
from datetime import datetime
import os

def verify_path_date(file_path):
    # Get current system date
    now = datetime.now()
    expected_dir = now.strftime("%Y/%m/%d")
    
    # Normalize path
    file_path = os.path.abspath(file_path)
    
    # We only check posts and almanac entries
    if "CONTENT/posts" in file_path or "CONTENT/almanac" in file_path:
        if expected_dir not in file_path:
            print(f"🛑 ОШИБКА: Путь {file_path} не соответствует текущей дате {expected_dir}!")
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if not verify_path_date(sys.argv[1]):
            sys.exit(1)
