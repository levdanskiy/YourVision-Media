"""Daily improvement module stub."""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent

def report_path(day: date) -> Path:
    return ROOT / "03_REPORTS" / "improvements" / f"IMPROVE-{day.isoformat()}.md"

def status(content: str) -> str:
    if "✅" in content or "done" in content.lower():
        return "completed"
    return "pending"
