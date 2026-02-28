#!/usr/bin/env python3
import os
import re
import sys

def audit_style(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fn = os.path.basename(file_path).upper()
    errors = []

    # 1. Проверка моноширинных акцентов
    if not re.search(r'`.*?`', content):
        errors.append("UX: Добавьте моноширинные акценты (бэктики).")

    # 2. Канальная специфика (V4.0 Minimalist)
    if "AC-" in fn:
        if "─── 💠 ───" not in content: errors.append("STYLE: Нет разделителя '─── 💠 ───'.")
    
    elif "NB-" in fn:
        if "· · 🔹 · ·" not in content: errors.append("STYLE: Нет разделителя '· · 🔹 · ·'.")

    elif "SW-" in fn:
        if "✧ ── 🔸 ── ✧" not in content: errors.append("STYLE: Нет разделителя '✧ ── 🔸 ── ✧'.")
        if "●" not in content: errors.append("STYLE: Нет рейтингов ●●●○○.")

    if errors:
        for err in errors: print(f"❌ {err}")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    if audit_style(sys.argv[1]):
        print("✅ STYLE AUDIT PASSED (V4.0 Minimalist)")
        sys.exit(0)
    else:
        sys.exit(1)
