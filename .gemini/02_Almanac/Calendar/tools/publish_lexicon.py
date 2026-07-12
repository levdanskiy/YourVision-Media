#!/usr/bin/env python3
"""
Publish Lexicon Post
Usage: python3 tools/publish_lexicon.py <filepath>
Validates the post (typography, length, headers) and changes its status from draft to ready.
"""

import sys
import os
import re

def validate_and_publish(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Typography Check
    if '—' in content or '–' in content:
        errors.append("Forbidden dashes ('—' or '–') found. Use short hyphens ('-').")

    # Length Check
    char_count = len(content)
    if char_count > 3500:
        errors.append(f"Post is too long: {char_count} chars. Max allowed: 3500 chars (for TG with image).")

    # Frontmatter status check
    is_ready = 'status: ready' in content
    has_draft = 'status: draft' in content or 'СТАТУС: DRAFT' in content

    if not is_ready and not has_draft:
        errors.append("File does not contain a recognized draft or ready status.")

    if errors:
        print(f"❌ Validation failed for {filepath}:")
        for err in errors:
            print(f"  - {err}")
        return False

    if is_ready:
        print(f"✅ Validation passed. Post is already marked as READY: {filepath}")
        return True

    # Publish
    new_content = content.replace("status: draft", "status: ready")
    new_content = new_content.replace("СТАТУС: DRAFT", "СТАТУС: ГОТОВ")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Post successfully validated and marked as READY: {filepath}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tools/publish_lexicon.py <filepath>")
        sys.exit(1)
        
    success = validate_and_publish(sys.argv[1])
    sys.exit(0 if success else 1)
