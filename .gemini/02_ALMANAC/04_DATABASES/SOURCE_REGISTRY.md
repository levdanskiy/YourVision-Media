# SOURCE REGISTRY

This registry separates sources that are worth downloading from sources that should remain API/query based.

## Download First

| Source | Trust | Local Use | Rubrics | Access | Rule |
|--------|-------|-----------|---------|--------|------|
| UNESCO Intangible Cultural Heritage dataset | A | Small structured index of living heritage practices, inscription years, countries/communities, domains. | `HERITAGE`, `CALENDAR`, `RITES`, `MODERN` | API/export | Good local download. Do not treat inscription as origin. Cite entry and access date. |
| USDA FoodData Central downloads | A | Ingredient composition and food-science checks. | `RECIPE`, `BREAD`, `FLATBREAD`, `PIES`, `CAKES`, `DESSERTS` | CSV/JSON downloads | Good local download for chemistry/nutrition facts. Not a food-history source. |
| Met Museum Open Access CSV | A/B | Object metadata for material culture, cards, amulets, ritual objects, food vessels, textile motifs. | `DIVINATION`, `LORE`, `HERITAGE`, visual research | GitHub CSV, CC0 metadata | Useful local download if object search becomes regular. Images require separate rights checks. |

## API Or Targeted Query

| Source | Trust | Use | Rubrics | Access | Rule |
|--------|-------|-----|---------|--------|------|
| Library of Congress loc.gov API | A | Folklife records, digitized books, images, newspapers, ephemera. | `SOURCE`, `OMENS`, `HERITAGE`, `DIVINATION`, `MODERN` | JSON/YAML API | Query per post or per theme. Preserve item URL, collection, date, rights. |
| Europeana APIs | B | Cultural heritage metadata across European institutions. | `SOURCE`, `HERITAGE`, `DIVINATION`, food-history object leads | API key | Use for discovery and records; verify final claims at holding institution. |
| Nager.Date | B/C | Public-holiday discovery and rough monthly scanning. | `CALENDAR`, `MODERN` | REST API / self-host | Use as a discovery layer only. Confirm culturally loaded dates with official/religious sources. |
| Wikidata | C/B for discovery | Entity discovery, alternate names, dates, identifiers. | All rubrics | SPARQL/API | Do not download full dump. Use as lead generator, then cite primary/institutional source. |
| Open Food Facts | C | Modern packaged-food labels, ingredient trends, product examples. | `MODERN`, occasional `SWEETS`/`DESSERTS` | API/data exports | Use for modern product culture only, not origin/history claims. |

## Targeted Text Sources

| Source | Trust | Use | Rubrics | Rule |
|--------|-------|-----|---------|------|
| Perseus Digital Library | A | Greek/Latin primary texts. | `LORE`, `SOURCE`, `ETYMON` | Cite work, book/line, translator/edition. |
| Project Gutenberg | B | Public-domain folklore, cookbooks, literary texts. | `SOURCE`, `LORE`, food history leads | Save exact title/edition URL in source card; do not bulk mirror. |
| Internet Sacred Text Archive | B | Public-domain religion, folklore, myth texts. | `LORE`, `OMENS`, `DIVINATION` | Old editions only; verify major claims elsewhere. |
| Chinese Text Project | B | Classical Chinese texts and I Ching-related material. | `DIVINATION`, `SOURCE`, `ETYMON` | Verify translations/editions before strong claims. |

## Almanac Source Card Index

The most useful project-specific database is not a huge corpus. It is a small verified source index:

```csv
id,rubric_group,source_title,source_type,trust_level,url,license_or_rights,citation_rule,used_in,notes,last_checked
```

Every time a post uses a strong source, add a card. This gradually becomes the project's real research memory.
