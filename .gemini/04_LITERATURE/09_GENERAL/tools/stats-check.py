#!/usr/bin/env python3
"""
stats-check.py - валидатор числовых счётчиков дерева OMNIVERSE (Literature).

Схемо-агностичный: рекурсивно находит в STATS.json любой узел вида
{ "value": <число>, "history": [ {"delta": <число>, ...}, ... ] } и проверяет:

  1. АРИФМЕТИКА:  value == start + Σ(history.delta)
       - start = node["start"] если задан;
       - иначе, если есть "max" (ресурс - полный бак) - start = max;
       - иначе start = 0 (affinity/счётчики отношений/глобальные).
  2. ГРАНИЦЫ:     0/min <= value <= max/cap (если поля заданы).
  3. ПОРОГИ:      сообщает, какие thresholds достигнуты (для сверки unlock-постов),
                  и предупреждает про «застыл на капе».
  4. ГИГИЕНА:     каждый history-элемент имеет post_id; delta - число;
                  порядок записей по day/date не убывает.
  5. ЗЕРКАЛО:     сверяет value из STATS.json с прозой в STATE.md
                  (раздел «СКРЫТЫЕ СЧЕТЧИКИ» / прозаический дубль), см. MIRROR.

Ошибки (расхождение арифметики, выход за границы) -> exit code 1.
Предупреждения (нет post_id, зеркало разошлось) -> печатаются, exit 0.

Использование:
    python3 stats-check.py arcana          # одна работа
    python3 stats-check.py --all           # все работы дерева со STATS.json
    python3 stats-check.py zodiac --quiet   # только ошибки/предупреждения
"""

import json
import re
import sys
import argparse
from pathlib import Path

TREE = "LITERATURE"
TREE_ROOT = Path("/home/levdanskiy/.gemini/04_LITERATURE")

# Код работы -> папка проекта
WORKS = {
    "arcana": "01_ARCANA",
    "zodiac": "02_ZODIAC",
}

# Зеркальная сверка STATS.json <-> проза STATE.md.
# Ключ - значение поля "project" в STATS.json.
#   state: путь к STATE.md относительно папки проекта.
#   labels: leaf-ключ счётчика -> подпись строки в STATE.md ("Подпись: N").
MIRROR = {
    "ARCANA": {
        "state": "02_SYSTEM/STATE.md",
        "labels": {
            "ragnar_freya": "Рагнар и Фрейя",
            "darian_serena": "Дариан и Серена",
            "lunfei_aikikyz": "Лун-Фей и Айки-Кыз",
            "adebayo_ifaazhe": "Адебайо и Ифа-Аже",
            "zein_nasrin": "Зейн и Насрин",
            "miron_vila": "Мирон и Вила",
        },
    },
}

# ── ANSI (мягко, отключается если не tty) ──
def _c(code, s):
    if sys.stdout.isatty():
        return f"\033[{code}m{s}\033[0m"
    return s

RED = lambda s: _c("31", s)
YEL = lambda s: _c("33", s)
GRN = lambda s: _c("32", s)
DIM = lambda s: _c("2", s)
BOLD = lambda s: _c("1", s)


def is_counter(node):
    return (
        isinstance(node, dict)
        and "value" in node
        and isinstance(node.get("history"), list)
    )


def walk_counters(node, path=""):
    """Возвращает [(path, counter_node)] - не заходя внутрь найденного счётчика."""
    out = []
    if is_counter(node):
        out.append((path, node))
        return out
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            out.extend(walk_counters(v, p))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.extend(walk_counters(v, f"{path}[{i}]"))
    return out


def leaf(path):
    return re.split(r"[.\[]", path)[-1].rstrip("]")


def sort_key(h):
    if "day" in h:
        return (0, h["day"])
    if "date" in h:
        return (1, str(h["date"]))
    return (2, 0)


def check_counter(path, node, errors, warns, infos):
    value = node["value"]
    history = node["history"]

    if not isinstance(value, (int, float)):
        # строковый "value" без истории отсеивается is_counter; сюда почти не попадём
        warns.append(f"{path}: value не число ({value!r}) - пропуск арифметики")
        return

    if "start" in node:
        start = node["start"]
    elif "max" in node:
        start = node["max"]  # ресурс: старт с полного бака
    else:
        start = 0

    total = 0
    for i, h in enumerate(history):
        d = h.get("delta")
        if not isinstance(d, (int, float)):
            errors.append(f"{path}.history[{i}]: delta не число ({d!r})")
            continue
        total += d
        if not (h.get("post_id") or h.get("post")):
            warns.append(f"{path}.history[{i}]: нет post_id")

    expected = round(start + total, 2)
    if round(value, 2) != expected:
        errors.append(
            f"{path}: value={value}, а start({start})+Σδ({total:+g})={expected} - РАСХОЖДЕНИЕ АРИФМЕТИКИ"
        )
    else:
        infos.append(f"{path}: value={value} = start({start})+Σδ({total:+g}) ✓")

    # границы
    if "max" in node and value > node["max"]:
        errors.append(f"{path}: value {value} > max {node['max']}")
    if "min" in node and value < node["min"]:
        errors.append(f"{path}: value {value} < min {node['min']}")
    cap = node.get("cap")
    if cap is not None and value > cap:
        errors.append(f"{path}: value {value} > cap {cap}")
    if cap is not None and value == cap:
        infos.append(f"{path}: застыл на капе {cap} (ждёт кульминации)")
    if "max" in node and value == node["max"] and history:
        infos.append(f"{path}: на максимуме {node['max']}")
    if "min" in node and value == node["min"]:
        infos.append(f"{path}: на минимуме {node['min']}")

    # пороги
    thr = node.get("thresholds")
    if thr:
        keys = thr.keys() if isinstance(thr, dict) else thr
        reached = sorted(
            [float(t) for t in keys if _num(t) is not None and value >= _num(t)],
            key=lambda x: x,
        )
        if reached:
            nice = ", ".join(f"{int(t) if t == int(t) else t}" for t in reached)
            infos.append(f"{path}: достигнуты пороги [{nice}] - сверь unlock-посты")

    # порядок истории
    keyed = [sort_key(h) for h in history]
    if keyed != sorted(keyed):
        warns.append(f"{path}: история не по возрастанию day/date - проверь порядок")


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def mirror_check(project, stats, counters, warns, infos):
    cfg = MIRROR.get(project)
    if not cfg:
        return
    state_path = None
    # найти папку проекта по значению project (обратный поиск в WORKS не нужен -
    # STATS.json уже загружен, путь знаем из вызывающей стороны через infos)
    # проще: cfg["_dir"] проставляется в run()
    state_path = cfg.get("_state_full")
    if not state_path or not Path(state_path).exists():
        warns.append(f"зеркало: STATE.md не найден ({state_path}) - сверка пропущена")
        return
    text = Path(state_path).read_text(encoding="utf-8")
    by_leaf = {leaf(p): n for p, n in counters}
    for key, label in cfg["labels"].items():
        node = by_leaf.get(key)
        if node is None:
            continue
        m = re.search(rf"{re.escape(label)}\s*:\s*(-?\d+)", text)
        if not m:
            warns.append(f"зеркало: в STATE.md не найдена строка «{label}: N»")
            continue
        prose = int(m.group(1))
        if prose != node["value"]:
            warns.append(
                f"зеркало РАСХОЖДЕНИЕ: «{label}» в STATE.md = {prose}, "
                f"а в STATS.json = {node['value']} (обновить прозу!)"
            )
        else:
            infos.append(f"зеркало: «{label}» = {prose} ✓")


def check_work(code, quiet=False):
    if code not in WORKS:
        print(RED(f"❌ Неизвестная работа: {code}. Есть: {', '.join(WORKS)}"))
        return 2
    base = TREE_ROOT / WORKS[code] / "02_SYSTEM"
    stats_path = base / "STATS.json"
    print(BOLD(f"\n═══ {code.upper()} ═══"))
    if not stats_path.exists():
        print(DIM(f"   нет STATS.json ({stats_path}) - работа ещё не запущена, пропуск"))
        return 0

    try:
        stats = json.loads(stats_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(RED(f"   ❌ STATS.json не парсится: {e}"))
        return 1

    project = stats.get("project", code.upper())
    counters = walk_counters(stats)
    errors, warns, infos = [], [], []

    for path, node in counters:
        check_counter(path, node, errors, warns, infos)

    cfg = MIRROR.get(project)
    if cfg:
        cfg["_state_full"] = str(TREE_ROOT / WORKS[code] / cfg["state"])
    mirror_check(project, stats, counters, warns, infos)

    if not quiet:
        for m in infos:
            print(DIM(f"   {m}"))
    for m in warns:
        print(YEL(f"   ⚠ {m}"))
    for m in errors:
        print(RED(f"   ❌ {m}"))

    if errors:
        print(RED(f"   ИТОГ: {len(errors)} ошибок, {len(warns)} предупреждений"))
        return 1
    if warns:
        print(YEL(f"   ИТОГ: ок, но {len(warns)} предупреждений"))
        return 0
    print(GRN(f"   ИТОГ: чисто ({len(counters)} счётчиков)"))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("work", nargs="?", help=f"Код работы: {', '.join(WORKS)}")
    ap.add_argument("--all", action="store_true", help="Все работы дерева")
    ap.add_argument("--quiet", action="store_true", help="Только ⚠/❌")
    args = ap.parse_args()

    rc = 0
    if args.all:
        for code in WORKS:
            rc |= check_work(code, quiet=args.quiet)
    elif args.work:
        rc = check_work(args.work, quiet=args.quiet)
    else:
        ap.print_help()
        return 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
