#!/usr/bin/env python3
"""Run focused checks for staged Almanac files."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE_PATH = re.compile(r"02_CONTENT/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/")


def call(*command: str) -> int:
    return subprocess.call(command, cwd=ROOT)


def main() -> int:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    dates = sorted(
        {
            f"{match.group('year')}-{match.group('month')}-{match.group('day')}"
            for path in paths
            if (match := DATE_PATH.search(path))
        }
    )
    codes: list[int] = []
    for target in dates:
        codes.append(call(sys.executable, "tools/almanac", "doctor", target))
    if any(".gemini/02_ALMANAC/" in path or path.startswith("02_ALMANAC/") for path in paths):
        codes.append(call(sys.executable, "tools/audit_system_docs.py"))
    return 1 if any(code != 0 for code in codes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
