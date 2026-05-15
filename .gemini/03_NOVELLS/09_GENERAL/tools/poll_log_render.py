#!/usr/bin/env python3
"""
poll_log_render.py - Регенерация POLL_LOG.md из POLL_LOG.json

Источник истины - JSON. MD генерируется автоматически для человекочитаемого
просмотра. Любые правки делать в JSON, не в MD.

Использование:
    python3 poll_log_render.py kingmaker
    python3 poll_log_render.py vienna_special
    python3 poll_log_render.py --all
"""

import json
import sys
import argparse
from pathlib import Path

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

PROJECT_DISPLAY = {
    "kingmaker": "👑 KINGMAKER",
    "vienna_special": "🎤 VIENNA SPECIAL",
    "orchid": "🌺 ORCHID",
    "donor": "🩸 DONOR",
    "order": "🌾 ORDER",
    "horizon": "✨ HORIZON",
    "code": "⚡ CODE",
    "anthropos": "🧬 ANTHROPOS",
    "eleyia": "🟠 ELEYIA",
}


def render_options(options):
    """Форматирует список опций как 'A - X% | B - Y%'"""
    parts = []
    for opt in options:
        pct = opt.get("percent")
        if pct is None:
            parts.append(f"{opt['label']} - (открыт)")
        else:
            parts.append(f"{opt['label']} - {pct}%")
    return " | ".join(parts)


def render_poll(poll):
    """Один опрос в markdown"""
    lines = []
    lines.append(f"### День {poll['narrative_day']} ({poll['pub_date']}) - {poll['id']}")
    lines.append("")
    lines.append(f"**Категория:** {poll.get('category', 'live')} / Фаза {poll['phase']}")
    lines.append(f"**Вопрос:** {poll['question']}")
    lines.append(f"**Варианты:** {render_options(poll['options'])}")

    total = poll.get("total_votes")
    if total is not None:
        lines.append(f"**Всего голосов:** {total}")

    winner = poll.get("winner")
    if winner:
        wt = poll.get("winner_type", "")
        lines.append(f"**Победитель:** {winner} ({wt})")

    tie = poll.get("tie_resolution")
    if tie:
        lines.append(f"**Резолюция ничьи:** {tie}")

    if poll.get("impact_scoreboard"):
        lines.append(f"**Влияние на SCOREBOARD:** {poll['impact_scoreboard']}")

    if poll.get("impact_content"):
        lines.append(f"**Влияние на контент:** {poll['impact_content']}")

    deltas = poll.get("stats_deltas", [])
    if deltas:
        lines.append(f"**STATS deltas:**")
        for d in deltas:
            sign = "+" if d["delta"] >= 0 else ""
            lines.append(f"  - {d['character']}.{d['param']} {sign}{d['delta']} ({d['reason']})")

    if poll.get("post_id"):
        lines.append(f"**Пост-источник:** `{poll['post_id']}`")

    if poll.get("notes"):
        lines.append(f"*{poll['notes']}*")

    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def render_project(project_key):
    """Рендерит POLL_LOG.md для проекта"""
    if project_key not in PROJECT_DIRS:
        print(f"❌ Неизвестный проект: {project_key}")
        return False

    project_dir = NOVELLS_ROOT / PROJECT_DIRS[project_key]
    json_path = project_dir / "02_SYSTEM" / "POLL_LOG.json"
    md_path = project_dir / "02_SYSTEM" / "POLL_LOG.md"

    if not json_path.exists():
        print(f"⚠️  Нет JSON для {project_key}: {json_path}")
        return False

    with open(json_path) as f:
        data = json.load(f)

    display_name = PROJECT_DISPLAY.get(data.get("project", project_key), project_key.upper())

    out = []
    out.append(f"# {display_name} - POLL LOG")
    out.append("")
    out.append(f"**Сезон:** {data.get('season', '?')}")
    out.append(f"**Последнее обновление:** {data.get('last_updated', '?')}")
    out.append(f"**Источник истины:** `POLL_LOG.json` (этот файл генерируется автоматически)")
    out.append("")
    out.append(f"Всего опросов: **{len(data.get('polls', []))}**")
    out.append("")
    out.append("Регенерация: `python3 09_GENERAL/tools/poll_log_render.py {project_key}`".replace("{project_key}", project_key))
    out.append("")
    out.append("---")
    out.append("")

    # Group by phase
    polls_by_phase = {}
    for poll in data.get("polls", []):
        phase = poll.get("phase", 0)
        polls_by_phase.setdefault(phase, []).append(poll)

    phase_names = {
        0: "ПРЕДСТАРТ / SETUP",
        1: "ФАЗА 1",
        2: "ФАЗА 2",
        3: "ФАЗА 3",
        4: "ЭПИЛОГ",
    }

    for phase in sorted(polls_by_phase.keys()):
        out.append(f"## {phase_names.get(phase, f'PHASE {phase}')}")
        out.append("")
        for poll in polls_by_phase[phase]:
            out.append(render_poll(poll))

    md_content = "\n".join(out)
    with open(md_path, "w") as f:
        f.write(md_content)

    print(f"✅ Сгенерировано: {md_path} ({len(data.get('polls', []))} опросов)")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", help="Код проекта или --all")
    parser.add_argument("--all", action="store_true", help="Регенерировать для всех проектов с JSON")
    args = parser.parse_args()

    if args.all:
        success_count = 0
        for project_key in ["kingmaker", "vienna_special", "orchid", "donor", "order", "horizon", "code", "anthropos", "eleyia"]:
            if render_project(project_key):
                success_count += 1
        print(f"\nИтого: {success_count} проектов обновлено")
        return

    if not args.project:
        parser.print_help()
        sys.exit(1)

    if not render_project(args.project):
        sys.exit(1)


if __name__ == "__main__":
    main()
