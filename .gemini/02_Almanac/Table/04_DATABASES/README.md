# LOCAL DATABASES

This folder is for small, licensed, source-preserving datasets that support repeated Almanac planning and factchecking.

Do not bulk-download cultural corpora just because they exist. Almanac needs traceable citations, not a private shadow library.

## Policy

Download locally only when all are true:

- license or terms allow local reuse;
- the dataset will be used repeatedly across rubrics;
- original source metadata can be preserved;
- update cadence is known;
- generated posts will cite source records, not copy large text passages.

Use APIs or targeted source pages when:

- the source is very large;
- an API is maintained by the institution;
- copyright/access rights vary per item;
- the project only needs one record for one post.

## Structure

```text
04_DATABASES/
  README.md
  SOURCE_REGISTRY.md
  PUBLICATION_REGISTRY.json
  ASSET_REGISTRY.json
  EVIDENCE_REGISTRY.json
  EXPERIMENT_REGISTRY.json
  EDITORIAL_INCIDENTS.json
  downloads/       # raw downloaded files, if approved
  indexes/         # small derived indexes created from approved data
  notes/           # source-specific usage notes
```

## Current Commands

Download approved datasets and rebuild indexes:

```bash
python3 tools/download_databases.py
```

Rebuild indexes from already downloaded files:

```bash
python3 tools/build_database_indexes.py
```

Current generated indexes:

- `indexes/unesco_ich_index.csv`
- `indexes/nager_public_holidays_2026_index.csv`
- `indexes/usda_foundation_food_2026_index.csv`
- `indexes/source_cards.csv`
- `indexes/semantic_memory.sqlite`
- `CANON_REGISTRY.json`
- `PUBLICATION_REGISTRY.json`
- `ASSET_REGISTRY.json`

Operational registries are maintained through `python3 tools/almanac ...`; do not hand-edit generated canon, publication, asset or semantic indexes unless repairing corruption.

## Recommended Local Layer

1. `UNESCO ICH` structured metadata for heritage and living-practice discovery.
2. `Nager.Date` or another public-holiday API export for rough calendar discovery, never as final religious/cultural authority.
3. `USDA FoodData Central` selected food-composition data for ingredient and technique checks.
4. `Met Open Access` metadata when object/deck/material culture search is useful.
5. A hand-built `Almanac source card index`: one row per verified source used in posts.

## Not Recommended As Bulk Downloads

- Full Library of Congress collections.
- Full Europeana records.
- Full Wikidata dumps.
- Internet Archive or HathiTrust bulk books.
- Random folklore/recipe GitHub datasets without clear source lineage.

For these, use targeted queries and cite exact records.
