"""Trend due module stub."""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent

def is_due(day: date) -> bool:
    # Example logic: true every 5 days or similar
    return day.day % 5 == 0

def report_path(day: date) -> Path:
    return ROOT / "03_REPORTS" / "trends" / f"TREND-{day.isoformat()}.md"
