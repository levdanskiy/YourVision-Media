#!/usr/bin/env python3
"""
stats-apply.py - Применяет stats_deltas из POLL_LOG к STATS.json

Идемпотентен: каждый опрос применяется к STATS только один раз
(маркируется поле applied_to_stats: true).

Использование:
    python3 stats-apply.py kingmaker vs-1-d4-q1        # один опрос
    python3 stats-apply.py kingmaker --all-unapplied   # все, что ещё не применялись
    python3 stats-apply.py vs --check                  # только проверить, без записи
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import date

NOVELLS_ROOT = Path("/home/levdanskiy/.gemini/03_NOVELLS")

PROJECT_DIRS = {
    "kingmaker": "02_KINGMAKER",
    "km": "02_KINGMAKER",
    "vienna_special": "10_VIENNA_SPECIAL",
    "vs": "10_VIENNA_SPECIAL",
    "orchid": "05_ORCHID",
    "donor": "03_DONOR",
    "order": "06_ORDER",
    "horizon": "04_HORIZON",
    "code": "07_CODE",
    "anthropos": "08_ANTHROPOS",
    "eleyia": "01_ELEYIA",
}

AFFINITY_THRESHOLDS = [25, 50, 75, 100]


def project_paths(project_key):
    if project_key not in PROJECT_DIRS:
        raise ValueError(f"Неизвестный проект: {project_key}")
    base = NOVELLS_ROOT / PROJECT_DIRS[project_key] / "02_SYSTEM"
    return {
        "poll_log": base / "POLL_LOG.json",
        "stats": base / "STATS.json",
    }


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def compute_trend(history, current):
    """Считает тренд по последним 2 значениям истории"""
    if len(history) < 1:
        return "→"
    last_delta = history[-1].get("delta", 0)
    if last_delta <= -0.5:
        return "↑↑"  # большая улучшение (lower number = better)
    elif last_delta < 0:
        return "↑"
    elif last_delta == 0:
        return "→"
    elif last_delta <= 0.5:
        return "↓"
    else:
        return "↓↓"


def apply_delta(stats, delta, poll_id, narrative_day):
    """Применяет один delta к STATS. Возвращает список событий (для лога)."""
    char_id = delta["character"]
    param = delta["param"]
    value = delta["delta"]
    reason = delta.get("reason", "")

    events = []
    chars = stats.setdefault("characters", {})

    if char_id not in chars:
        events.append({"type": "warn", "msg": f"Персонаж '{char_id}' не найден в STATS.json - пропуск"})
        return events

    char = chars[char_id]

    if param == "reputation":
        rep = char.setdefault("reputation", {"current": 0, "start": 0, "trend": "→", "history": []})
        old = rep.get("current", 0)
        new = round(old + value, 2)
        rep["current"] = new
        history_entry = {
            "day": narrative_day,
            "poll_id": poll_id,
            "delta": value,
            "from": old,
            "to": new,
            "reason": reason,
        }
        rep.setdefault("history", []).append(history_entry)
        rep["trend"] = compute_trend(rep["history"], new)
        events.append({"type": "info", "msg": f"  {char.get('name', char_id)}.reputation: {old} → {new} ({'+' if value >= 0 else ''}{value}) {rep['trend']}"})

    elif param == "affinity":
        aff = char.setdefault("affinity", {"current": 0, "unlocks": {}, "history": []})
        old = aff.get("current", 0)
        new = max(0, old + value)  # affinity не падает ниже 0
        aff["current"] = new
        history_entry = {
            "day": narrative_day,
            "poll_id": poll_id,
            "delta": value,
            "from": old,
            "to": new,
            "reason": reason,
        }
        aff.setdefault("history", []).append(history_entry)
        events.append({"type": "info", "msg": f"  {char.get('name', char_id)}.affinity: {old} → {new} ({'+' if value >= 0 else ''}{value})"})

        # Проверяем пороги
        unlocks = aff.setdefault("unlocks", {})
        for threshold in AFFINITY_THRESHOLDS:
            key = str(threshold)
            if new >= threshold and old < threshold:
                unlock = unlocks.get(key, {})
                if not unlock.get("triggered"):
                    concept = unlock.get("concept", "?")[:80]
                    events.append({
                        "type": "unlock",
                        "msg": f"  🔓 UNLOCK: {char.get('name', char_id)} достиг {threshold}% - нужен пост типа {unlock.get('type', 'UNKNOWN')}: «{concept}...»"
                    })
    else:
        events.append({"type": "warn", "msg": f"Неизвестный параметр '{param}' - пропуск"})

    return events


def apply_poll(poll_log, stats, poll_id, check_only=False):
    """Применяет один опрос. Возвращает (success, events)."""
    polls = poll_log.get("polls", [])
    poll = next((p for p in polls if p.get("id") == poll_id), None)

    if poll is None:
        return False, [{"type": "error", "msg": f"Опрос {poll_id} не найден в POLL_LOG.json"}]

    if poll.get("applied_to_stats"):
        return False, [{"type": "warn", "msg": f"Опрос {poll_id} уже применён ранее. Пропуск."}]

    deltas = poll.get("stats_deltas", [])
    if not deltas:
        return False, [{"type": "warn", "msg": f"Опрос {poll_id} не имеет stats_deltas. Пропуск."}]

    if poll.get("total_votes") is None:
        return False, [{"type": "warn", "msg": f"Опрос {poll_id} ещё не закрыт (total_votes is null). Пропуск."}]

    events = [{"type": "header", "msg": f"\n📊 {poll_id}: {poll.get('question', '?')}"}]

    narrative_day = poll.get("narrative_day", 0)
    for delta in deltas:
        events.extend(apply_delta(stats, delta, poll_id, narrative_day))

    if not check_only:
        poll["applied_to_stats"] = True

    return True, events


def print_events(events):
    for e in events:
        t = e["type"]
        msg = e["msg"]
        prefix = {
            "header": "",
            "info": "",
            "warn": "  ⚠️ ",
            "error": "  ❌ ",
            "unlock": "",
        }.get(t, "")
        print(f"{prefix}{msg}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", help="Код проекта (kingmaker, vs, orchid, ...)")
    parser.add_argument("poll_id", nargs="?", help="ID опроса (например vs-1-d4-q1)")
    parser.add_argument("--all-unapplied", action="store_true", help="Применить все ещё не применённые опросы")
    parser.add_argument("--check", action="store_true", help="Только показать что произойдёт, без записи")
    args = parser.parse_args()

    try:
        paths = project_paths(args.project)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not paths["poll_log"].exists():
        print(f"❌ Нет POLL_LOG.json для {args.project}")
        sys.exit(1)
    if not paths["stats"].exists():
        print(f"❌ Нет STATS.json для {args.project}")
        sys.exit(1)

    poll_log = load_json(paths["poll_log"])
    stats = load_json(paths["stats"])

    if args.all_unapplied:
        targets = [p["id"] for p in poll_log.get("polls", [])
                   if not p.get("applied_to_stats")
                   and p.get("total_votes") is not None
                   and p.get("stats_deltas")]
        if not targets:
            print("✅ Все опросы с deltas уже применены, либо ещё открыты.")
            return
        print(f"📋 К применению: {len(targets)} опросов")
        for pid in targets:
            ok, events = apply_poll(poll_log, stats, pid, check_only=args.check)
            print_events(events)
    elif args.poll_id:
        ok, events = apply_poll(poll_log, stats, args.poll_id, check_only=args.check)
        print_events(events)
        if not ok:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if not args.check:
        today = date.today().isoformat()
        poll_log["last_updated"] = today
        stats["last_updated"] = today
        save_json(paths["poll_log"], poll_log)
        save_json(paths["stats"], stats)
        print(f"\n✅ Сохранено в:")
        print(f"   {paths['poll_log']}")
        print(f"   {paths['stats']}")
    else:
        print(f"\n(--check режим, изменения НЕ сохранены)")


if __name__ == "__main__":
    main()
