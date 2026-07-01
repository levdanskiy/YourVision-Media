#!/usr/bin/env python3
"""
CONTENT AUDITOR v2.0
====================
Скрипт полного аудита контентных папок Almanac и Lexicon.

Проверяет:
1. Количество символов тела поста vs грейд (Grade Q/S/F/B/C/A)
2. Абсолютный лимит 3500 символов
3. Наличие длинных тире (em-dash, en-dash)
4. Наличие флагов-эмодзи
5. Наличие системного заголовка (//)
6. Наличие секций Ингредиенты / Приготовление в рецептах Альманаха
7. Корректность формата футера

Использование:
    python3 content_auditor.py                        # Аудит всех файлов
    python3 content_auditor.py --day 30               # Аудит конкретного дня
    python3 content_auditor.py --channel LEXICON      # Аудит конкретного канала
    python3 content_auditor.py --fix-grades           # Автоматическая коррекция грейдов
"""

import os
import re
import sys
import glob
import json
import argparse
from datetime import datetime

# === CONFIGURATION ===

BASE_ALMANAC = os.path.expanduser(
    "~/GEMINI_PROJECT/02_ALMANAC/02_CONTENT/2026/06"
)
BASE_LEXICON = os.path.expanduser(
    "~/GEMINI_PROJECT/05_LEXICON/02_CONTENT/2026/06"
)

GRADE_LIMITS = {
    'Q': (100, 300),
    'S': (301, 500),
    'F': (501, 1000),
    'B': (1001, 1300),
    'C': (1301, 1800),
    'A': (1801, 2400),
}

ABSOLUTE_MAX = 3500

BAD_DASHES = ['\u2014', '\u2013']  # em-dash, en-dash

# Rubrics that are NOT recipes (no Ingredients/Preparation needed)
NON_RECIPE_RUBRICS = [
    'TRANSITION', 'SOURCE', 'ETYMON', 'CALENDAR', 'CYCLES',
    'HERITAGE', 'OMENS', 'ANNOUNCEMENT'
]

FLAG_PATTERN = re.compile(r'[\U0001F1E0-\U0001F1FF]{2}')


def extract_body(content):
    """Extract the main body text, ignoring YAML frontmatter, // headers, and footer."""
    lines = content.split('\n')

    # Skip YAML frontmatter (--- ... ---)
    start_idx = 0
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                start_idx = i + 1
                break

    # Skip // header lines
    while start_idx < len(lines) and (
        lines[start_idx].startswith('//') or not lines[start_idx].strip()
    ):
        start_idx += 1

    # Find footer: first '---' line after body start that precedes Grade/timer
    footer_idx = len(lines)
    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()
        if stripped == '---':
            # Check if this is a footer separator (near end or before Grade)
            remaining = '\n'.join(lines[i:])
            if 'Grade:' in remaining or 'Время чтения' in remaining:
                footer_idx = i
                break

    body = '\n'.join(lines[start_idx:footer_idx]).strip()
    return body


def determine_correct_grade(char_count):
    """Given a character count, return the correct grade."""
    for grade, (lo, hi) in sorted(GRADE_LIMITS.items(), key=lambda x: x[1][0]):
        if lo <= char_count <= hi:
            return grade
    if char_count > 2400:
        return 'A+'  # over max grade but under absolute limit
    return None


def audit_file(fpath):
    """Audit a single markdown file. Returns dict with results."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    basename = os.path.basename(fpath)
    results = {
        'file': basename,
        'path': fpath,
        'issues': [],
        'warnings': [],
        'info': [],
    }

    # 1. Check for bad dashes
    for bd in BAD_DASHES:
        if bd in content:
            name = "EM-DASH (\u2014)" if bd == '\u2014' else "EN-DASH (\u2013)"
            count = content.count(bd)
            results['issues'].append(f"ДЛИННОЕ ТИРЕ: {name} x{count}")

    # 2. Check for flag emojis
    flags = FLAG_PATTERN.findall(content)
    if flags:
        results['issues'].append(f"ФЛАГ ЭМОДЗИ: {flags}")

    # 3. Check system header
    has_yaml = content.startswith('---')
    has_header = '// ИД-ПОСТА:' in content
    if not has_header:
        results['issues'].append("НЕТ СИСТЕМНОГО ЗАГОЛОВКА (// ИД-ПОСТА:)")

    # 4. Extract grade
    grade_match = re.search(r'\*\*Grade:\*\*\s*([A-Z])', content)
    grade = grade_match.group(1) if grade_match else None
    results['grade'] = grade

    if not grade:
        results['issues'].append("НЕТ ГРЕЙДА (**Grade:**) В ФУТЕРЕ")

    # 5. Extract and count body
    body = extract_body(content)
    char_count = len(body)
    results['chars'] = char_count

    # 6. Validate grade vs chars
    if grade and grade in GRADE_LIMITS:
        lo, hi = GRADE_LIMITS[grade]
        correct_grade = determine_correct_grade(char_count)

        if char_count < lo:
            results['issues'].append(
                f"СЛИШКОМ КОРОТКО: {char_count} символов < минимум {lo} для Grade {grade}"
            )
            if correct_grade:
                results['issues'].append(
                    f"  -> Корректный грейд: {correct_grade}"
                )
        elif char_count > hi:
            results['warnings'].append(
                f"ПРЕВЫШАЕТ ГРЕЙД: {char_count} символов > максимум {hi} для Grade {grade}"
            )
            if correct_grade and correct_grade != grade:
                results['warnings'].append(
                    f"  -> Рекомендованный грейд: {correct_grade}"
                )

    # 7. Absolute max
    if char_count > ABSOLUTE_MAX:
        results['issues'].append(
            f"ПРЕВЫШАЕТ АБСОЛЮТНЫЙ ЛИМИТ: {char_count} > {ABSOLUTE_MAX}"
        )

    # 8. Recipe sections (Almanac only, non-transition)
    if basename.startswith('AL-'):
        is_recipe = True
        for nr in NON_RECIPE_RUBRICS:
            if nr in basename.upper():
                is_recipe = False
                break

        if is_recipe:
            if 'Ингредиенты' not in content:
                results['issues'].append("НЕТ СЕКЦИИ 'Ингредиенты'")
            if 'Приготовление' not in content:
                results['issues'].append("НЕТ СЕКЦИИ 'Приготовление'")

    # 9. Footer format check
    if '⏱' not in content:
        results['warnings'].append("НЕТ МЕТРИКИ ЧТЕНИЯ (⏱ Время чтения)")

    results['status'] = 'FAIL' if results['issues'] else (
        'WARN' if results['warnings'] else 'PASS'
    )
    return results


def fix_grades(results_list):
    """Auto-fix grades in files where text exceeds assigned grade."""
    fixed = 0
    for r in results_list:
        if r['status'] == 'PASS':
            continue
        chars = r.get('chars', 0)
        grade = r.get('grade')
        if not grade or not chars:
            continue

        correct = determine_correct_grade(chars)
        if correct and correct != grade and correct in GRADE_LIMITS:
            with open(r['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content.replace(
                f'**Grade:** {grade}',
                f'**Grade:** {correct}'
            )
            if new_content != content:
                with open(r['path'], 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  FIXED: {r['file']} Grade {grade} -> {correct}")
                fixed += 1
    return fixed


def main():
    parser = argparse.ArgumentParser(description='Content Auditor v2.0')
    parser.add_argument('--day', type=int, help='Audit specific day (1-31)')
    parser.add_argument('--channel', choices=['ALMANAC', 'LEXICON'],
                        help='Audit specific channel')
    parser.add_argument('--fix-grades', action='store_true',
                        help='Auto-fix mismatched grades')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--summary', action='store_true',
                        help='Show summary only')
    args = parser.parse_args()

    # Determine which directories to scan
    dirs_to_scan = []
    day_range = range(args.day, args.day + 1) if args.day else range(1, 32)

    for day in day_range:
        day_str = f"{day:02d}"
        if args.channel != 'LEXICON':
            al_dir = os.path.join(BASE_ALMANAC, day_str)
            if os.path.isdir(al_dir):
                dirs_to_scan.append(('ALMANAC', day_str, al_dir))
        if args.channel != 'ALMANAC':
            lx_dir = os.path.join(BASE_LEXICON, day_str)
            if os.path.isdir(lx_dir):
                dirs_to_scan.append(('LEXICON', day_str, lx_dir))

    all_results = []
    for channel, day, dirpath in dirs_to_scan:
        for f in sorted(glob.glob(os.path.join(dirpath, '*.md'))):
            r = audit_file(f)
            r['channel'] = channel
            r['day'] = day
            all_results.append(r)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
        return

    # Print report
    total = len(all_results)
    fails = sum(1 for r in all_results if r['status'] == 'FAIL')
    warns = sum(1 for r in all_results if r['status'] == 'WARN')
    passes = sum(1 for r in all_results if r['status'] == 'PASS')

    print("=" * 80)
    print(f"  CONTENT AUDITOR v2.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    if not args.summary:
        for r in all_results:
            icon = {'PASS': '✅', 'WARN': '⚠️', 'FAIL': '🚨'}[r['status']]
            print(f"\n{icon} [{r['channel']}] {r['day']}/{r['file']}")
            print(f"   Grade: {r.get('grade', '?')} | Символов: {r.get('chars', '?')}")

            for iss in r['issues']:
                print(f"   🔴 {iss}")
            for w in r['warnings']:
                print(f"   🟡 {w}")

    print(f"\n{'=' * 80}")
    print(f"  ИТОГО: {total} файлов | ✅ {passes} PASS | ⚠️ {warns} WARN | 🚨 {fails} FAIL")
    print(f"{'=' * 80}")

    if args.fix_grades:
        print("\n--- AUTO-FIX GRADES ---")
        fixed = fix_grades(all_results)
        print(f"Исправлено грейдов: {fixed}")

    # Exit code
    sys.exit(1 if fails > 0 else 0)


if __name__ == '__main__':
    main()
