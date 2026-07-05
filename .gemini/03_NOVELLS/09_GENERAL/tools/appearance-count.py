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
    "eleyia":   ("03_NOVELLS/01_ELEYIA",   ["Микас","Дориан","Феликс","Элиас","Марта","Оэрон","Елена","Страздс","Калейс","Снорри","Вика","Ула","Аня","Симас"]),
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


# Ключевые слова для грубой оценки ТОНА поста (свет/тьма). Не идеально, но даёт %.
LIGHT = ["любов","люблю","поцелу","обня","обни","нежн","тепл","смех","смея","шутк","шути",
         "друж","друг","семь","праздник","танц","радост","улыб","дом","забот","вместе","спас"]
DARK  = ["страх","боит","угроз","приказ","список","куратор","арест","опасн","предат","потер",
         "смерт","убил","кровь","боль","враг","тьма","ужас","паник","изъят","изоляц","контракт"]


def tone_report(project, total, texts, last):
    import re as _re
    light = sum(1 for t in texts if any(_re.search(w, t, _re.I) for w in LIGHT))
    dark  = sum(1 for t in texts if any(_re.search(w, t, _re.I) for w in DARK))
    both  = sum(1 for t in texts if any(_re.search(w, t, _re.I) for w in LIGHT) and any(_re.search(w, t, _re.I) for w in DARK))
    only_dark = dark - both
    print(f"\n🌗 TONE-BALANCE: {project} ({total} постов{' - последние '+str(last) if last else ''})")
    print("─" * 52)
    print(f"  ☀️ есть светлый бит (любовь/дружба/семья/праздник/юмор): {light}/{total} = {light/total*100:.0f}%")
    print(f"  🌑 есть тёмный бит (проблема/угроза/потеря):             {dark}/{total} = {dark/total*100:.0f}%")
    print(f"  ⚖️ и свет, и тьма в одном посте:                        {both}/{total} = {both/total*100:.0f}%")
    print(f"  ⛔ ТОЛЬКО тьма, без света:                              {only_dark}/{total} = {only_dark/total*100:.0f}%")
    print("─" * 52)
    if light/total < 0.5:
        print("⚠ светлых битов < 50% - перекос в проблемы. В БУДУЩИХ постах добавить любовь/дружбу/праздник/юмор.")
    else:
        print("✓ светлые биты присутствуют широко. Держать баланс.")
    print("(груба́я keyword-оценка; точный учёт - в TONE_LEDGER работы по Главам.)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--last", type=int, default=0, help="только последние N постов")
    ap.add_argument("--names", default="", help="список имён через запятую")
    ap.add_argument("--tone", action="store_true", help="вместо героев - баланс ТОНА (свет/тьма) по постам")
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

    if args.tone:
        tone_report(args.project, total, texts, args.last)
        return

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
