#!/usr/bin/env python3
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import json
import subprocess
from datetime import datetime

console = Console()

def get_trend_status():
    try:
        with open("/home/levdanskiy/.gemini/CORE/knowledge/TREND_STATUS.json", "r") as f:
            return json.load(f)
    except: return {}

def display_genesis_master_hud():
    trends = get_trend_status()
    last_audit = trends.get('LAST_AUDIT', {}).get('MJ_PROMPTS', 'N/A')
    
    # Сетка
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1); grid.add_column(ratio=1)
    
    # Блок 1: Системный статус
    sys_t = Table(show_header=False, box=None)
    sys_t.add_row("[cyan]📡 TREND AUDIT[/]", f"[yellow]{last_audit}[/]")
    sys_t.add_row("[cyan]🧬 BOOST[/]", "[green]100+ ACTIVE[/]")
    sys_t.add_row("[cyan]🚦 ENGINE[/]", "[green]GOD-EYE V10[/]")
    
    # Блок 2: Тренды
    tr_t = Table(show_header=False, box=None)
    tr_t.add_row("[magenta]📸 VISUAL[/]", "Phase One 150MP")
    tr_t.add_row("[magenta]🖋️ TEXT[/]", "Tier-1 Tier-1 Monocle")
    tr_t.add_row("[magenta]🎨 MOOD[/]", "Winter Chic")

    grid.add_row(
        Panel(sys_t, title="[bold white]SYSTEM INTEGRITY[/]", border_style="blue"),
        Panel(tr_t, title="[bold white]CURRENT TRENDS[/]", border_style="magenta")
    )

    main_panel = Panel(
        grid,
        title="[bold white]GEMINI GENESIS MASTER CONTROL V13.0[/bold white]",
        subtitle="[bold red]TREND WATCHDOG ACTIVE[/bold red]",
        border_style="bright_blue"
    )
    
    console.print(main_panel)

if __name__ == "__main__":
    display_genesis_master_hud()