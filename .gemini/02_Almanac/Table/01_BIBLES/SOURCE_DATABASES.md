# SOURCE DATABASES

This file lists external corpora and databases that Almanac may use for myths, tales, legends, omens, superstitions, calendars, rituals, desserts, baking, bread, and food history.

Do not bulk-download or ingest any source before checking its license, terms, and citation requirements. Prefer reading and citing targeted entries.

## Trust Levels

| Level | Meaning | Use |
|-------|---------|-----|
| `A` | Primary text, official institution, academic catalogue, government/intergovernmental data. | Can support factual claims directly. |
| `B` | Reputable public-domain archive, university/library guide, specialist reference, curated museum/library collection. | Good working source; verify high-stakes claims. |
| `C` | Community-maintained or commercial/crowdsourced database. | Use for discovery, not final authority. Confirm elsewhere. |
| `D` | Blogs, social posts, unsourced summaries, AI-generated pages. | Do not use as evidence. Use only as leads. |

## Citation Rule

Every fact-heavy post should keep a short source note in metadata:

```text
// FACTCHECK: Perseus, Hesiod Theogony lines 116-138; ATU 510A; UNESCO ICH entry checked 2026-05-29
```

Minimum citation data by source type:

| Source Type | Required Citation |
|-------------|-------------------|
| Primary text | Author/work, translator or edition, book/chapter/line/page, URL if digital. |
| Folktale | Collector/editor, tale title, collection, year, ATU type if known, motif number if used. |
| Superstition/omen | Culture/region in source, collector or publication, year, exact wording if quoted. |
| Divination/astrology/tarot | System/deck/text/object, edition or catalogue record, date range, creator/translator if known, institution or scholarly source, access date. |
| Calendar/astronomy | Institution/service, exact date/time, timezone/UTC, access date. |
| Food history | Author/reference, entry title, edition/year, page or URL, claim checked. |
| Food science | Source, temperature/process data, whether it is experimental, professional, or culinary reference. |

## Source Categories

### Myth And Classical Texts

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| Perseus Digital Library | A | https://www.perseus.tufts.edu/ | Greek/Latin primary texts, mythology references, original-language checks. | Use line/book references. Good for `LORE`, `SOURCE`, `ETYMON`. |
| Theoi Greek Mythology | B | https://www.theoi.com/ | Greek myth cross-reference and primary-text snippets. | Use as index; confirm important claims in primary text. |
| Internet Sacred Text Archive | B | https://sacred-texts.com/ | Public-domain religion, mythology, folklore, legends. | Good archive, but editions are old. Cite edition/translator. |
| Wikisource | B/C | https://www.wikisource.org/ | Public-domain primary texts in multiple languages. | Quality varies by text. Check edition notes. |
| Project Gutenberg | B | https://www.gutenberg.org/ | Public-domain myth, folklore, fairy-tale books. | Good for text access; not scholarly apparatus. |

### Folktales, Fairy Tales, Legends

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| ATU / The Types of International Folktales | A | https://www.folklorefellows.fi/ffc-284-286-2024-edition/ | Tale-type classification. | Standard scholarly index. Usually not fully open; cite type numbers from reliable references. |
| Stith Thompson Motif-Index | A/B | https://en.wikisource.org/wiki/Motif-Index_of_Folk-Literature | Motif classification. | Use motif numbers as classification, not as proof that a tale exists in a culture. |
| BARTOC vocabulary records | B | https://bartoc.org/ | Authority records for classification systems. | Useful for confirming terminology. |
| Project Gutenberg Folklore bookshelf | B | https://www.gutenberg.org/ebooks/bookshelf/37 | Public-domain folklore collections. | Good for source discovery and direct texts. |
| Library of Congress American Folklife Center | A | https://www.loc.gov/folklife/ | Field recordings, ethnographic collections, public folklore. | Strong for `HERITAGE`, `OMENS`, modern folklife. |
| Open Folklore / library guides | B | https://openfolklore.org/ | Discovery of folklore scholarship and archives. | Use as gateway, not final citation when a primary source is available. |
| World Oral Literature Project | A/B | https://www.oralliterature.org/ | Endangered oral literatures, field collections, global oral traditions. | Strong global discovery source; cite collection, language, performer/collector, year. |
| Endangered Languages Archive (ELAR) | A | https://www.elararchive.org/ | Oral narratives, songs, ritual speech, endangered-language documentation. | Check access rights per deposit. Preserve language/community metadata. |
| DOBES Archive | A | https://dobes.mpi.nl/ | Endangered language documentation and oral tradition collections. | Use collection metadata carefully; not all materials are open. |
| Pangloss Collection / CNRS Cocoon | A | https://pangloss.cnrs.fr/ | Oral texts, endangered languages, transcriptions/translations. | Strong for underrepresented oral traditions. Cite DOI/record if available. |
| Smithsonian Center for Folklife and Cultural Heritage Archives | A | https://folklife.si.edu/archives | Public folklore, festival documentation, global craft/music/ritual records. | Use finding aids and collection records. |

### Omens, Superstitions, Folk Belief

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| Library of Congress American Folklife Center | A | https://www.loc.gov/folklife/ | Folk belief, oral histories, field collections. | Cite collection, informant if available, date/place. |
| Internet Sacred Text Archive | B | https://sacred-texts.com/ | Older public-domain superstition and folk-belief books. | Treat as historical records, not universal facts. |
| HathiTrust / Internet Archive | B/C | https://www.hathitrust.org/ / https://archive.org/ | Digitized older folklore books. | Check copyright/access; cite scan edition. |
| Regional folklore journals and university repositories | A/B | varies | Local omens, prohibitions, protective gestures. | Prefer peer-reviewed or institutional repositories. |
| World Oral Literature Project | A/B | https://www.oralliterature.org/ | Oral belief narratives and community knowledge. | Good for global coverage; cite community and collector. |
| Endangered Language Alliance Archive | A/B | https://www.elalliance.org/our-work/research/archive | Diaspora oral histories, folktales, recipes, songs, minority languages. | Especially useful for diaspora/global city coverage. |

Use for `OMENS` only when the exact wording or behavior can be traced. If the source says “people believed,” identify who, where, and when. Avoid universal claims like “all Slavs believed...”.

### Divination, Astrology, Tarot, Oracles

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| Museum and library catalogues for historical decks | A/B | varies | Tarot decks, card objects, makers, dating, iconography. | Prefer institution records for object claims. Check image rights before visuals. |
| Beinecke, BnF Gallica, British Library, Europeana, Library of Congress | A/B | varies | Manuscripts, printed fortune-telling books, almanacs, ephemera, astrology tables. | Cite object ID, shelfmark, scan page, institution. |
| Chinese Text Project | B | https://ctext.org/ | Classical Chinese texts including I Ching-related material. | Use as text access; verify translation and edition for final claims. |
| Scholarly I Ching translations and commentaries | A/B | print/academic | Hexagram structure, transmission, commentary history. | Cite translator/edition/page. |
| Oracle bone archives and academic catalogues | A/B | varies | Shang oracle bones, inscription corpora, divination objects. | Use catalogue number and scholarly interpretation. |
| Academic history of astrology | A/B | print/academic | Zodiac systems, tropical/sidereal distinction, precession, transmission history. | Astronomy facts should be checked against astronomy sources too. |
| NASA / astronomy education sources | A | https://science.nasa.gov/ | Precession, ecliptic, solstice/equinox astronomy. | Use for sky mechanics, not cultural interpretation. |
| Media-history sources and newspaper archives | A/B | varies | Newspaper horoscopes, mass-media astrology, advice-column formats. | Cite publication, issue date, column author if known. |
| Ifa and Yoruba religion scholarship | A/B | print/academic/institutional | Ifa corpus, divination procedure, oral literary structure. | Avoid flattening living religion into “fortune telling”. |
| Folklore/anthropology studies of cowrie shells, lots, geomancy, dream books, coffee-ground reading | A/B | academic/institutional | Social function, material procedure, local practice. | Name community/source context exactly. |

Use for `DIVINATION` only as cultural history, material system, symbolic grammar, media format, or anthropology of uncertainty. TikTok tarot, apps, memes, and personal readings may be modern examples, but never final evidence for historical claims.

### Calendar, Ritual, Heritage, Modern Observances

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| United Nations International Days | A | https://www.un.org/en/observances/list-days-weeks | UN observance dates and official framing. | Good for `CALENDAR`, `MODERN`. |
| UNESCO Intangible Cultural Heritage | A | https://ich.unesco.org/en/lists | Inscribed practices, safeguarding status, official descriptions. | Good for `HERITAGE`; do not treat inscription as “origin”. |
| UNESCO DataHub ICH dataset | A | https://data.unesco.org/explore/dataset/ich001/ | Structured ICH data. | Useful for audits and coverage maps. |
| NASA Science | A | https://science.nasa.gov/ | Eclipses, equinox/solstice explanations, sky events. | Use for astronomy facts; exact local times may need another source. |
| timeanddate | B | https://www.timeanddate.com/ | Local solstice/equinox times, moon phases, daylight duration. | Good operational source; cite timezone and access date. |
| Official national calendars | A | varies | Public holidays and movable observances. | Prefer official government/ministry/source pages. |
| Religious institutional calendars | A/B | varies | Liturgical dates and local observance rules. | Use tradition-specific sources; avoid flattening denominations. |
| Smithsonian Folklife Festival Archives | A | https://folklife.si.edu/archives | Living ritual, craft, festival, performance, and heritage documentation. | Strong for modern living heritage and diaspora practice. |
| Endangered Languages Archive / DOBES / Pangloss | A | varies | Ritual speech, ceremonial songs, oral calendar knowledge. | Use only when metadata supports ritual/calendar claims. |

### Global Coverage Discovery

Use these to find underrepresented zones. They are gateways, not automatic authorities.

| Zone | Starting Points |
|------|-----------------|
| `Africa` | World Oral Literature Project; African Storybook for open educational story leads; university African studies repositories; national museums/libraries. |
| `African Diaspora` | Library of Congress Folklife; Smithsonian Folklife; Caribbean and Black Atlantic archives; oral history collections. |
| `Indigenous Americas` | Library of Congress Folklife; tribal/nation cultural centers; museum archives; university Indigenous studies repositories. |
| `Latin America` | National libraries, Biblioteca Digital Hispánica, Biblioteca Nacional Digital Brasil, folklore journals, UNESCO ICH. |
| `East Asia` | National Diet Library, Chinese Text Project for classical texts, Korean/Japanese cultural heritage portals, UNESCO ICH. |
| `South Asia` | Digital Library of India where available, Sanskrit/Prakrit/Tamil text archives, university folklore departments, UNESCO ICH. |
| `Southeast Asia` | National libraries, SEAlang, university repositories, UNESCO ICH, oral literature collections. |
| `Central Asia` | Endangered language archives, Turkic/Pamir oral literature repositories, national academies. |
| `West Asia` | Sacred Texts, national manuscript libraries, Islamic/Persian/Arabic text archives, UNESCO ICH. |
| `Oceania` | Australian Institute of Aboriginal and Torres Strait Islander Studies (AIATSIS), Pacific manuscript/oral history repositories, UNESCO ICH. |
| `Global Modern` | UN, UNESCO, official organizers, platform archives, commerce/statistics sources, media-history sources. |

### Food History, Desserts, Baking, Bread

| Source | Level | URL | Use For | Notes |
|--------|-------|-----|---------|-------|
| Oxford Companion to Food | A/B | https://www.oxfordreference.com/ | Food history entries, terminology, global food context. | Usually paywalled. Cite edition/page when available. |
| Food Timeline | B | https://www.foodtimeline.org/ | Food history leads, historical recipes, source trails. | Use as a research gateway; confirm major claims. |
| Europeana | B | https://www.europeana.eu/ | Digitized cultural heritage objects, old cookbooks, images, ephemera. | Check object license and institution record. |
| Gallica / BnF | A/B | https://gallica.bnf.fr/ | French historical cookbooks and pastry sources. | Strong for French food history. Cite scan/page. |
| Library of Congress / Internet Archive cookbooks | B | https://www.loc.gov/ / https://archive.org/ | Historical cookbooks and manuals. | Cite exact edition, year, page. |
| USDA FoodData Central | A | https://fdc.nal.usda.gov/ | Nutrient data, ingredient composition. | Not food history. Good for chemistry/nutrition claims. |
| Open Food Facts | C | https://world.openfoodfacts.org/ | Modern product labels, ingredients, NOVA/category leads. | Crowdsourced. Confirm before factual publication. |

### Food Science And Technique

| Source | Level | Use For | Notes |
|--------|-------|---------|-------|
| Harold McGee, On Food and Cooking | A/B | Food chemistry, heat, proteins, starch, sugar, fermentation. | Cite edition/page. |
| Professional baking textbooks | A/B | Hydration, fermentation, temperatures, pastry technique. | Prefer named textbook/edition. |
| USDA / EFSA / FDA resources | A | Food safety temperatures, storage safety. | Use for safety claims. |
| Peer-reviewed food science papers | A | Specific chemical or process claims. | Required for unusual claims. |

## Download Policy

Do not download a full corpus unless all are true:

1. License allows local use.
2. Corpus is needed for repeated work, not a one-off post.
3. Storage location and update plan are defined.
4. Source metadata is preserved.
5. Copyrighted text is not reproduced in generated posts beyond short quotations.

Suggested local structure if approved later:

```text
04_DATABASES/
  SOURCE_REGISTRY.md
  folklore/
  mythology/
  calendars/
  food_history/
  food_science/
  README.md
```

Current local policy and candidate registry live in `04_DATABASES/README.md` and `04_DATABASES/SOURCE_REGISTRY.md`.

## Preferred Source Stack By Rubric

| Rubric | Primary Stack |
|--------|---------------|
| `LORE` | Primary text or collector edition + ATU/Motif if tale-type analysis is needed + one scholarly reference for context. |
| `SOURCE` | Primary text/edition + author context source + original language if relevant. |
| `OMENS` | Folk-belief collection or field record + second source for cross-cultural comparison + mechanism source if physical claim. |
| `DIVINATION` | Primary object/text/deck/catalogue + scholarly history/anthropology source + astronomy/media-history source when relevant. |
| `ETYMON` | Specialist dictionary or philological source + corpus/first-use source + cognate check. |
| `CALENDAR` | Official calendar/UN/religious institution + historical source. |
| `WHEEL` | NASA/timeanddate for astronomy + historical/ritual source. |
| `HERITAGE` | UNESCO/institutional archive/fieldwork source + current status source. |
| `CYCLES` | Calendar-system source + cultural/anthropological source. |
| `MODERN` | Official origin/source + current scale/statistics + critical/context source. |
| `RITES` | Anthropological source + tradition-specific source + current practice source. |
| `CAKES/BUNS/PATISSERIE/DESSERTS/SWEETS` | Food history source + technique source + optional historical cookbook. |
| `BREAD/FLATBREAD/PIES` | Food history source + regional technique source + food safety/science source if temperatures are claimed. |

## Red Flags

- No named collector, edition, translator, institution, or date.
- “Ancient people believed...” without culture and source.
- “In all cultures...” without comparative evidence.
- Food origin claims based on restaurant marketing.
- Holiday origin claims based only on tourism pages.
- TikTok tarot, apps, personal readings, or horoscope columns used as historical evidence.
- Divination posts that give medical, financial, legal, romantic, or personal predictions.
- Etymology from unsourced blogs or folk etymology.
- AI-generated summaries used as sources.
- Exact astronomical or calendar times without timezone.

## Quotation Limits

- Quote only the minimum needed.
- Prefer paraphrase with citation.
- For primary literary texts, keep quoted passages short and cite edition/translator.
- For copyrighted modern works, use brief excerpts only and never reproduce full poems, chapters, recipes, or articles.
