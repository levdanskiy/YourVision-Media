# WORLD COVERAGE MATRIX

Almanac covers the world, not a home region. This matrix defines the minimum coverage system for all three daily themes.

## Cultural Zones

Use these values in metadata as `cultural_zone`. Use the most precise value that is true.

| Zone | Includes |
|------|----------|
| `Africa` | North, West, Central, East, Southern Africa; African urban modernity; pan-African systems. |
| `African Diaspora` | Caribbean, Black Atlantic, African American, Afro-Latin, Afro-European traditions. |
| `Indigenous Americas` | North, Central, South American Indigenous traditions, including Arctic Indigenous Americas. |
| `Latin America` | Spanish/Portuguese/French-speaking Americas and syncretic traditions. |
| `North America` | US/Canada modern, regional, settler, immigrant, and diasporic traditions. |
| `East Asia` | China, Japan, Korea, Taiwan, Mongolia, Sinosphere systems. |
| `South Asia` | India, Pakistan, Bangladesh, Sri Lanka, Nepal, Bhutan, Maldives. |
| `Southeast Asia` | Mainland and island Southeast Asia. |
| `Central Asia` | Turkic, Persianate, steppe, Pamir, Silk Road cultures. |
| `West Asia` | Middle East, Anatolia, Caucasus, Arabian Peninsula, Persianate worlds where relevant. |
| `Oceania` | Polynesia, Micronesia, Melanesia, Australia, Aotearoa/New Zealand, Pacific islands. |
| `Europe` | All European traditions, including Mediterranean, Nordic, Slavic, Celtic, Balkan, Jewish Europe. |
| `Arctic North` | Circumpolar and high-latitude traditions across continents. |
| `Island Cultures` | Island systems where island ecology is central: Pacific, Atlantic, Indian Ocean, Caribbean, Mediterranean islands. |
| `Global Modern` | Internet, commercial, UN, sports, media, technological, diasporic, transnational phenomena. |
| `Cross-Cultural` | Comparative posts where no single zone is primary. Must list secondary zones in notes. |

## Metadata

New posts should include coverage metadata in YAML frontmatter or service comments:

```yaml
cultural_zone: West Asia
coverage_axis: underworld myth
source_type: primary_text
secondary_zones:
  - Europe
```

Legacy comment format:

```text
// CULTURAL_ZONE: West Asia
// COVERAGE_AXIS: underworld myth
// SOURCE_TYPE: primary_text
// SECONDARY_ZONES: Europe, South Asia
```

## Monthly Quotas

Minimum per month:

| Scope | Requirement |
|-------|-------------|
| All posts | Minimum 6 cultural zones total. |
| 10:04 | Minimum 3 cultural zones. |
| 15:04 | Minimum 3 cultural zones. |
| 18:02 | Minimum 3 cultural zones. |
| Non-European coverage | Minimum 50% of posts with known cultural zone should be non-European or cross-cultural with non-European zones. |
| Underrepresented rotation | Each month must include at least one post from `Africa`, `Indigenous Americas`, `Oceania` or `Island Cultures`, and `South Asia` or `Southeast Asia`. |
| Modern/global | Minimum 1 `Global Modern` post per month. |

These are floors, not targets. Exceed them.

## Coverage Axes By Theme

### 10:04 - Myths, Tales, Omens, Divination, Personae

Use one or more as `coverage_axis`:

| Axis | Examples |
|------|----------|
| `creation myth` | World origin, first humans, first fire, first death. |
| `underworld/death` | Descent, ancestors, ghosts, afterlife, psychopomps. |
| `trickster` | Spider, coyote, hare, raven, fox, divine messenger. |
| `flood/catastrophe` | Flood, fire, drought, cosmic reset. |
| `fairy tale type` | ATU-linked tale types, dark originals, variants. |
| `urban legend` | Modern fear story, internet legend, rumor cycle. |
| `omen` | Weather, body, home, road, animal, number. |
| `superstition` | Prohibition, protection, threshold, charm, ritual avoidance. |
| `personae` | Living dossier for a mythic, fairy-tale, saintly, legendary, or folkloric figure. |
| `bestiary` | Creature, monster, helper, animal-spirit, familiar, or boundary being. |
| `ritual_object` | Magical, protective, cursed, sacred, or story-driving object. |
| `divination` | Lots, cards, coffee grounds, dreams, birds, bones. |
| `astrology` | Zodiac, horoscopes, natal charts, sidereal/tropical systems, media astrology. |
| `oracle` | Ifa, I Ching, oracle bones, Urim and Thummim, Delphi, cowrie shells, cleromancy. |
| `word/etymology` | Cultural archaeology through one word. |

### 15:04 - Desserts, Baking, Bread

Use one or more:

| Axis | Examples |
|------|----------|
| `cake architecture` | Layer cake, festive cake, ceremonial cake. |
| `sweet dough` | Bun, brioche, enriched bread, spiral, filled dough. |
| `pastry technique` | Choux, laminated dough, tart, custard pastry. |
| `cold dessert` | Mousse, panna cotta, ice cream, pudding, trifle. |
| `sugar confection` | Halva, lokum, nougat, brittle, praline, fudge. |
| `fermented grain` | Sourdough, injera, dosa, rye, millet, sorghum. |
| `flatbread heat` | Tandoor, saj, comal, stone, griddle, hearth. |
| `savory pie` | Hand pie, festival pie, filled bread, quiche, borek. |
| `street sweet` | Market sweet, festival stall, portable dessert. |
| `diaspora dessert` | Colonial exchange, migration, hybrid dessert. |
| `ceremonial bread` | Sabbath, harvest, funeral, wedding, temple/church bread. |
| `non-wheat staple` | Rice, maize, cassava, millet, sorghum, teff, beans. |

### 18:02 - Calendar, Ritual, Time

Use one or more:

| Axis | Examples |
|------|----------|
| `solar` | Solstice, equinox, light, sun calendar. |
| `lunar` | Moon calendar, Hijri, lunisolar festivals, new moon. |
| `agricultural` | Planting, harvest, rain, herding, fishing, monsoon. |
| `ancestor/death` | Ancestor days, grave visits, memorial cycles. |
| `initiation` | Coming-of-age, status transition, secret societies. |
| `wedding/fertility` | Marriage, fertility rites, family continuity. |
| `fasting/feasting` | Ramadan, Lent, vrata, food prohibition, feast breaking. |
| `pilgrimage` | Road, shrine, sacred route, vow journey. |
| `protest/memorial` | Public memory, trauma, civic mourning, resistance. |
| `commercial modern` | Shopping festivals, marketing calendars, branded rituals. |
| `internet modern` | Meme days, fandom days, platform-origin rituals. |
| `state/national` | National day, official calendar, civic ritual. |
| `diasporic calendar` | Migrant communities maintaining or transforming a calendar. |

## Planning Rule

When planning a month, make a coverage table before writing posts:

```text
Zone / 10:04 / 15:04 / 18:02 / total / debt
Africa / 1 / 1 / 0 / 2 / needs 18:02
Oceania / 0 / 0 / 1 / 1 / needs food + lore
...
```

If a zone has had no post in two consecutive months, it becomes priority debt.

## What 100%+ Means

100% is not “every country.” It means the system actively samples every major cultural zone, every major function, and every major material/ritual axis over time.

100%+ means going beyond default canons: not only Greek myth, French pastry, and European holidays, but also West African tricksters, Andean ritual calendars, Austronesian navigation/time, South Asian sweets, Ethiopian fermentation, Indigenous American omen systems, Caribbean diaspora legends, Central Asian breads, Islamic lunar time, Pacific island ceremonies, and modern global internet rites.
