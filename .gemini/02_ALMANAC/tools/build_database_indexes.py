#!/usr/bin/env python3
"""Build small searchable CSV indexes from approved Almanac raw datasets."""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "04_DATABASES"
DOWNLOADS = DB / "downloads"
INDEXES = DB / "indexes"


def text_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item is not None)
    return str(value)


def build_unesco_index() -> int:
    source = DOWNLOADS / "unesco_ich" / "ich001.json"
    if not source.exists():
        return 0
    rows = json.loads(source.read_text(encoding="utf-8"))
    out = INDEXES / "unesco_ich_index.csv"
    fields = [
        "uuid",
        "ich_public_ref",
        "inscription_year",
        "title_en",
        "countries",
        "type_acronym",
        "type_of_element_en",
        "concepts_primary_names",
        "concepts_secondary_names",
        "http_url_en",
    ]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: text_value(row.get(field)) for field in fields})
    return len(rows)


def build_nager_index() -> int:
    source = DOWNLOADS / "nager_date" / "public_holidays_2026.json"
    if not source.exists():
        return 0
    payload = json.loads(source.read_text(encoding="utf-8"))
    out = INDEXES / "nager_public_holidays_2026_index.csv"
    fields = ["date", "countryCode", "localName", "name", "global", "types", "counties", "launchYear"]
    count = 0
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rows in payload.get("countries", {}).values():
            if not isinstance(rows, list):
                continue
            for row in rows:
                writer.writerow({field: text_value(row.get(field)) for field in fields})
                count += 1
    return count


def build_usda_index() -> int:
    source = DOWNLOADS / "usda_fdc" / "FoodData_Central_foundation_food_csv_2026-04-30.zip"
    if not source.exists():
        return 0
    out = INDEXES / "usda_foundation_food_2026_index.csv"
    with zipfile.ZipFile(source) as archive:
        with archive.open("FoodData_Central_foundation_food_csv_2026-04-30/food.csv") as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig"))
            rows = list(reader)
    fields = ["fdc_id", "data_type", "description", "food_category_id", "publication_date"]
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    return len(rows)


def main() -> int:
    INDEXES.mkdir(parents=True, exist_ok=True)
    counts = {
        "unesco_ich_index.csv": build_unesco_index(),
        "nager_public_holidays_2026_index.csv": build_nager_index(),
        "usda_foundation_food_2026_index.csv": build_usda_index(),
    }
    print("# Almanac database indexes")
    print()
    for name, count in counts.items():
        print(f"- {name}: {count} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
