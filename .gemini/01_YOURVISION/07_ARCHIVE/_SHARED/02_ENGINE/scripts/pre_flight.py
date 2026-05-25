#!/usr/bin/env python3
import sys
import subprocess
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_check(command, label):
    with console.status(f"[bold blue]Checking {label}...", spinner="dots"):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[bold red]✗[/bold red] {label} FAILED")
            return False
        console.print(f"[bold green]✓[/bold green] {label} PASSED")
        return True

def main(file_path):
    if not os.path.exists(file_path):
        sys.exit(1)

    fn = os.path.basename(file_path).upper()
    console.print(Panel(f"[bold cyan]ALMANAC PRE-FLIGHT CHECK[/bold cyan]\n[dim]Target: {file_path}[/dim]", border_style="cyan"))

    checks = [
        (f"bash .gemini/system/scripts/fix_punctuation.sh {file_path}", "Punctuation & Typos"),
        (f"python3 .gemini/system/scripts/ALMANAC_SHIELD.py {file_path}", "Persona & AR Shield"),
        (f"python3 .gemini/system/scripts/ALMANAC_UX_guard.py {file_path}", "UX & Sensory Guard")
    ]

    # Логика синхронизации Лора
    if "YV-" in fn:
        checks.append((f"python3 .gemini/system/scripts/auto_lore.py < {file_path}", "YV Event Lore Sync"))
    else:
        checks.append((f"python3 .gemini/system/scripts/almanac_lore_sync.py {file_path}", "Almanac Wisdom Lore Sync"))

    success = True
    for cmd, label in checks:
        if not run_check(cmd, label):
            success = False
            break

    if success:
        console.print("\n[bold green]🚀 MISSION READY. LORE SYNCHRONIZED.[/bold green]\n")
    else:
        console.print("\n[bold red]⛔ DEPLOYMENT ABORTED.[/bold red]\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    main(sys.argv[1])