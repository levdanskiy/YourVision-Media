#!/usr/bin/env python3
"""Base validator for LEXICON archive."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIBLES = ROOT / "01_BIBLES"
CONTENT = ROOT / "02_CONTENT"
REPORTS = ROOT / "03_REPORTS"
DATABASES = ROOT / "04_DATABASES"
TOOLS = ROOT / "tools"

def check_exists(path: Path, name: str) -> bool:
    if not path.exists():
        print(f"❌ {name} directory missing: {path}")
        return False
    print(f"✅ {name} directory found: {path}")
    return True

def main():
    print("LEXICON validator.")
    print("-" * 40)
    
    directories = [
        (BIBLES, "Bibles"),
        (CONTENT, "Content"),
        (REPORTS, "Reports"),
        (DATABASES, "Databases"),
        (TOOLS, "Tools"),
    ]
    
    all_ok = True
    for path, name in directories:
        if not check_exists(path, name):
            all_ok = False

    # Check for duplicate 04_ folder
    automation_dir = ROOT / "04_AUTOMATION"
    if automation_dir.exists():
        print(f"⚠️ Warning: Found {automation_dir.name} conflicting with 04_DATABASES numbering.")
        all_ok = False
        
    print("-" * 40)
    if all_ok:
        print("✅ Validation passed.")
        return 0
    else:
        print("❌ Validation failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
