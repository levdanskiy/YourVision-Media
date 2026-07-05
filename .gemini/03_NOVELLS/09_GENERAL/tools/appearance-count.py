#!/usr/bin/env python3
"""
appearance-count.py - счётчик экранного времени героев по постам работы.

Считает, в скольких постах (и в скольком % от всех) встречается каждое имя из
списка героев работы. Помогает держать РАВНОПРАВНОЕ раскрытие (feedback_character_appearance_parity):
фавориты/LI не должны доминировать; обделённых поднимать в БУДУЩИХ постах.

Использование:
    python3 appearance-count.py eleyia              # весь контент проекта
    python3 appearance-count.py eleyia --last 21     # только последние N постов
    python3 appearance-count.py eleyia --names Микас,Дориан,Феликс,Элиас

Список имён берётся из --names, иначе из авто-словаря ниже (по проекту).
Работает по любому дереву - путь к контенту задаётся автопоиском 04_CONTENT/03_CONTENT.
"""
import sys, argparse, re
from pathlib import Path

GEMINI = Path("/home/levdanskiy/.gemini")

# Папка проекта + имена по умолчанию (дополнять по мере надобности).
PROJECTS = {
    "eleyia":   ("03_NOVELLS/01_ELEYIA",   ["Микас","Дориан","Феликс","Элиас","Марта","Оэрон","Елена","Страздс","Калейс","Снорри"]),
    "kingmaker":("03_NOVELLS/02_KINGMAKER", []),
    "orchid":   ("03_NOVELLS/05_ORCHID",    []),
    "arcana":   ("04_LITERATURE/01_ARCANA", ["Рагнар","Фрейя","Дариан","Серена","Лун-Фей","Айки-Кыз","Адебайо","Ифа-Аже","Зейн","Насрин","Мирон","Вила"]),
    "zodiac":   ("04_LITERATURE/02_ZODIAC",  []),
    "tower":    ("03.5_CHRONICLES/01_TOWER", ["Алан","Делрой","Хейз","Саймон"]),
}


def find_posts(base: Path):
    for cdir in ("04_CONTENT", "03_CONTENT"):
        d = base / cdir
        if d.exists():
            return sorted(p for p in d.rglob("*.md"))
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--last", type=int, default=0, help="только последние N постов")
    ap.add_argument("--names", default="", help="список имён через запятую")
    args = ap.parse_args()

    if args.project not in PROJECTS:
        print(f"Проекты: {', '.join(PROJECTS)}"); sys.exit(1)
    rel, default_names = PROJECTS[args.project]
    base = GEMINI / rel
    names = [n.strip() for n in args.names.split(",") if n.strip()] or default_names
    if not names:
        print(f"Нет списка имён для {args.project} - задай --names"); sys.exit(1)

    posts = find_posts(base)
    if args.last:
        posts = posts[-args.last:]
    total = len(posts) or 1
    texts = [p.read_text(encoding="utf-8", errors="ignore") for p in posts]

    print(f"\n👥 APPEARANCE-COUNT: {args.project} ({total} постов{' - последние '+str(args.last) if args.last else ''})")
    print("─" * 52)
    rows = []
    for n in names:
        cnt = sum(1 for t in texts if re.search(re.escape(n), t))
        rows.append((n, cnt, cnt / total * 100))
    rows.sort(key=lambda r: -r[1])
    top = rows[0][2] if rows else 0
    for n, cnt, pct in rows:
        bar = "█" * round(pct / 4)
        flag = "  ⚠ обделён" if top - pct >= 30 else ""
        print(f"  {n:<12} {cnt:>3}/{total}  {pct:>4.0f}%  {bar}{flag}")
    print("─" * 52)
    print("⚠ = отстаёт от лидера ≥30 п.п. -> поднять в БУДУЩИХ постах (написанное не переписываем).")


if __name__ == "__main__":
    main()
