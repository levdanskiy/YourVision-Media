#!/usr/bin/env python3
"""
affinity-tally.py - Кросс-проверка аффинити по poll-дельтам (анти-ручная-математика).

Суммирует ВСЕ stats_deltas из POLL_LOG.json по персонажам/параметрам и печатает
накопленный итог + флажит пересечённые пороги аффинити (25/50/75/100).

ВАЖНО: считает ТОЛЬКО дельты из опросов. Не-опросные беаты (заряж-беат 18:00,
раскрытие правды, интим) в POLL_LOG не попадают - они ведутся напрямую в STATE.
Поэтому это СВЕРКА (poll-driven часть), а источник истины - STATE.md.
Расхождение «tally vs STATE» = на величину не-опросных беатов (это норма).

Использование:
    python3 affinity-tally.py orchid
    python3 affinity-tally.py km
"""

import json
import sys
from pathlib import Path

NOVELLS_ROOT = Path("/home/levdanskiy/.gemini/03_NOVELLS")
PROJECT_DIRS = {
    "kingmaker": "02_KINGMAKER", "km": "02_KINGMAKER",
    "vienna_special": "10_VIENNA_SPECIAL", "vs": "10_VIENNA_SPECIAL",
    "orchid": "05_ORCHID", "donor": "03_DONOR", "order": "06_ORDER",
    "horizon": "04_HORIZON", "code": "07_CODE", "anthropos": "08_ANTHROPOS",
    "eleyia": "01_ELEYIA",
}
THRESHOLDS = [25, 50, 75, 100]


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in PROJECT_DIRS:
        print("Использование: affinity-tally.py <project>")
        print("Проекты:", ", ".join(sorted(set(PROJECT_DIRS))))
        sys.exit(1)

    path = NOVELLS_ROOT / PROJECT_DIRS[sys.argv[1]] / "02_SYSTEM" / "POLL_LOG.json"
    if not path.exists():
        print(f"❌ Нет POLL_LOG.json: {path}")
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    polls = data.get("polls", [])

    # char -> param -> [(poll_id, delta)]
    tally = {}
    for p in polls:
        for d in p.get("stats_deltas", []):
            c = d.get("character", "?")
            par = d.get("param", "affinity")
            tally.setdefault(c, {}).setdefault(par, []).append((p.get("id", "?"), d.get("delta", 0)))

    if not tally:
        print("  (нет stats_deltas в POLL_LOG)")
        return

    print(f"\n💠 AFFINITY-TALLY (только poll-дельты; сверка с STATE) - {PROJECT_DIRS[sys.argv[1]]}")
    print("─" * 64)
    for c in sorted(tally):
        for par in sorted(tally[c]):
            entries = tally[c][par]
            total = sum(x[1] for x in entries)
            chain = " ".join(f"{'+' if d >= 0 else ''}{d}" for _, d in entries)
            line = f"  {c:<14} {par:<9} = {total:>4}   ({chain})"
            # пороги, пересечённые накоплением poll-дельт
            crossed = [t for t in THRESHOLDS if total >= t]
            if crossed and par == "affinity":
                line += f"   ⚑ порог {crossed[-1]}"
            print(line)
    print("\n  Σ = только опросы. Не-опросные беаты (18:00/правда/интим) - в STATE поверх этого.")
    print()


if __name__ == "__main__":
    main()
