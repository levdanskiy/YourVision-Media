#!/usr/bin/env python3
"""Download approved small Almanac source datasets and build local manifests."""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "04_DATABASES"
DOWNLOADS = DB / "downloads"
INDEXES = DB / "indexes"
NOTES = DB / "notes"


@dataclass
class DownloadRecord:
    id: str
    title: str
    url: str
    path: str
    status: str
    bytes: int
    note: str
    downloaded_at: str


def ensure_dirs() -> None:
    for path in [
        DOWNLOADS / "unesco_ich",
        DOWNLOADS / "nager_date",
        DOWNLOADS / "usda_fdc",
        INDEXES,
        NOTES,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def fetch(url: str, dest: Path, timeout: int = 90) -> DownloadRecord:
    req = urllib.request.Request(url, headers={"User-Agent": "AlmanacResearchBot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
        dest.write_bytes(data)
        return DownloadRecord(
            id=dest.stem,
            title=dest.name,
            url=url,
            path=str(dest.relative_to(ROOT)),
            status="downloaded",
            bytes=len(data),
            note="",
            downloaded_at=date.today().isoformat(),
        )
    except urllib.error.HTTPError as exc:
        return DownloadRecord(
            id=dest.stem,
            title=dest.name,
            url=url,
            path=str(dest.relative_to(ROOT)),
            status=f"http_{exc.code}",
            bytes=0,
            note=str(exc),
            downloaded_at=date.today().isoformat(),
        )
    except Exception as exc:  # noqa: BLE001
        return DownloadRecord(
            id=dest.stem,
            title=dest.name,
            url=url,
            path=str(dest.relative_to(ROOT)),
            status="failed",
            bytes=0,
            note=str(exc),
            downloaded_at=date.today().isoformat(),
        )


def download_unesco() -> list[DownloadRecord]:
    url = "https://data.unesco.org/api/explore/v2.1/catalog/datasets/ich001/exports/json?lang=en&timezone=UTC"
    return [fetch(url, DOWNLOADS / "unesco_ich" / "ich001.json")]


def download_usda() -> list[DownloadRecord]:
    url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip"
    return [fetch(url, DOWNLOADS / "usda_fdc" / "FoodData_Central_foundation_food_csv_2026-04-30.zip")]


def download_nager(year: int) -> list[DownloadRecord]:
    records: list[DownloadRecord] = []
    countries_path = DOWNLOADS / "nager_date" / "available_countries.json"
    countries_record = fetch("https://date.nager.at/api/v3/AvailableCountries", countries_path)
    records.append(countries_record)
    if countries_record.status != "downloaded":
        return records

    countries = json.loads(countries_path.read_text(encoding="utf-8"))
    holidays: dict[str, object] = {"year": year, "countries": {}}
    for country in countries:
        code = country.get("countryCode")
        if not code:
            continue
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{code}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AlmanacResearchBot/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                holidays["countries"][code] = json.loads(response.read().decode("utf-8"))
            time.sleep(0.05)
        except Exception as exc:  # noqa: BLE001
            holidays["countries"][code] = {"error": str(exc)}

    holidays_path = DOWNLOADS / "nager_date" / f"public_holidays_{year}.json"
    holidays_path.write_text(json.dumps(holidays, ensure_ascii=False, indent=2), encoding="utf-8")
    records.append(
        DownloadRecord(
            id=f"public_holidays_{year}",
            title=f"Nager.Date public holidays {year}",
            url="https://date.nager.at/api/v3/PublicHolidays/{year}/{countryCode}",
            path=str(holidays_path.relative_to(ROOT)),
            status="downloaded",
            bytes=holidays_path.stat().st_size,
            note=f"{len(holidays['countries'])} country payloads",
            downloaded_at=date.today().isoformat(),
        )
    )
    return records


def write_source_cards() -> None:
    path = INDEXES / "source_cards.csv"
    rows = [
        {
            "id": "unesco_ich_ich001",
            "rubric_group": "calendar_heritage_rites_modern",
            "source_title": "UNESCO Intangible Heritage List dataset ich001",
            "source_type": "institutional_dataset",
            "trust_level": "A",
            "url": "https://data.unesco.org/explore/dataset/ich001/",
            "license_or_rights": "UNESCO DataHub terms; cite entry and access date",
            "citation_rule": "Entry title, UNESCO ICH, inscription/listing year, dataset id, access date",
            "used_in": "",
            "notes": "Discovery and metadata. Inscription is not origin.",
            "last_checked": date.today().isoformat(),
        },
        {
            "id": "nager_date_public_holidays_2026",
            "rubric_group": "calendar_modern",
            "source_title": "Nager.Date public holidays API export 2026",
            "source_type": "calendar_discovery",
            "trust_level": "B/C",
            "url": "https://date.nager.at/api",
            "license_or_rights": "Open-source/community API; verify culturally loaded claims elsewhere",
            "citation_rule": "Use as discovery only; confirm with official national or religious source",
            "used_in": "",
            "notes": "Not final authority for ritual meaning.",
            "last_checked": date.today().isoformat(),
        },
        {
            "id": "usda_fdc_foundation_food_2026_04",
            "rubric_group": "food_science",
            "source_title": "USDA FoodData Central Foundation Foods April 2026",
            "source_type": "food_composition",
            "trust_level": "A",
            "url": "https://fdc.nal.usda.gov/download-datasets/",
            "license_or_rights": "USDA public data; cite dataset/release date",
            "citation_rule": "FoodData Central, data type, release, food id if used",
            "used_in": "",
            "notes": "Food composition, not food-history origin evidence.",
            "last_checked": date.today().isoformat(),
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def write_notes() -> None:
    (NOTES / "country_and_region_names.md").write_text(
        """# Country And Region Names

Country, city, region, language, and community names are allowed when they support evidence or comparison.

Allowed:
- origin of a dish, text, deck, ritual, object, or ingredient;
- comparison between versions, dates, calendars, techniques, names, or source traditions;
- institutional source context: museum, library, archive, government, religious calendar;
- route or diffusion history, when sourced.

Not allowed:
- writing as if one place is the channel's natural home;
- default phrases like "у нас", "наш регион", "здесь принято" without source context;
- repeated use of one region as the lens for unrelated subjects.
""",
        encoding="utf-8",
    )


def write_manifest(records: list[DownloadRecord]) -> None:
    manifest = {
        "generated_at": date.today().isoformat(),
        "records": [asdict(record) for record in records],
    }
    (DB / "download_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    records: list[DownloadRecord] = []
    records.extend(download_unesco())
    records.extend(download_nager(2026))
    records.extend(download_usda())
    write_source_cards()
    write_notes()
    write_manifest(records)

    from build_database_indexes import main as build_indexes  # noqa: PLC0415

    build_indexes()

    failed = [record for record in records if record.status != "downloaded"]
    print("# Almanac database download")
    print()
    for record in records:
        print(f"- {record.status}: {record.path} ({record.bytes} bytes)")
        if record.note:
            print(f"  note: {record.note}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
