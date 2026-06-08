# IDEAS BANK CURRENT

Active idea bank for the current Almanac system. Legacy material was preserved in `IDEAS_BANK_LEGACY.md`.

Rules:
- no city, country, or region is a channel anchor;
- every idea needs `rubric`, `cultural_zone`, `coverage_axis`, `source_stack`, and `status`;
- old regional ideas can return only after global rebalance;
- astrology, tarot, horoscopes, oracles, lots, runes, and divination are treated as cultural symbolic systems, not as fortune-telling claims.

Status values: `IDEA`, `RESEARCH`, `DRAFT`, `READY`, `USED`, `LEGACY_REVIEW`.

## Priority Gaps

| Gap | Why It Matters | First Fix |
|-----|----------------|-----------|
| `DIVINATION` missing from active system | Tarot/horoscopes/oracles existed in legacy ideas but not in taxonomy or validators. | Add `DIVINATION` to Theme II. |
| Food coverage too European | Sweet/pastry canon still defaults to Europe unless planned against matrix. | Use `Sugar Atlas` and `Bread Is A Map`. |
| Historical plans are region-heavy | Old May-July plans can pollute new planning. | Rebuild through `MONTHLY_PLANNING_TEMPLATE.md`. |
| Coverage metadata absent in old posts | Globality cannot be audited inside posts. | New posts require metadata; old posts can be backfilled later. |
| V4 style not machine-audited | Checklist exists, but style drift can return. | Future `audit_style.py`. |

---

## Theme II - Myths, Tales, Omens, Superstitions, Divination

### LORE

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Anansi steals stories | Before Anansi, people had events, not stories. Trickster as archive thief. | Africa / African Diaspora | trickster | folktale collection + folklore study | IDEA |
| Coyote creates trouble | Coyote is not a moral villain; he is how the world becomes unstable enough to begin. | Indigenous Americas | trickster / creation myth | tribal/nation source + scholarly context | IDEA |
| Maui slows the sun | Time as something negotiated by force, not received. | Oceania | solar myth | Polynesian source + regional scholarship | IDEA |
| Inanna at seven gates | Descent as controlled stripping of status. | West Asia | underworld/death | primary text + scholarly translation | IDEA |
| Naga as water boundary | Serpent as river/lake/power system, not monster. | South Asia / Southeast Asia | water spirit | primary/ethnographic source | IDEA |
| Kitsune nine tails | Power grows with time, but status never fully becomes divinity. | East Asia | shapeshifter | folklore collection + source note | IDEA |
| Dragon: East/West split | One figure, two social contracts: kill it or learn from it. | Cross-Cultural | monster / power | myth sources + comparison | IDEA |
| World tree beyond Yggdrasil | Ashvattha, Siberian birch, Sephirot: tree as vertical map. | Cross-Cultural | world structure | primary/secondary mix | IDEA |

### SOURCE / PROSE

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Tagore, Gitanjali | Prayer as public language during anti-colonial modernity. | South Asia | literary source | primary text + author context | IDEA |
| Achebe, Things Fall Apart | The title is already a borrowed prophecy. | Africa | literary source | primary text + historical context | IDEA |
| Mahmoud Darwish | Homeland as syntax, not slogan. | West Asia | literary source | primary text + translation note | IDEA |
| Han Kang | Body, refusal, and political memory. | East Asia | literary source | primary text + publisher/context | IDEA |
| Borges, library | Archive as divine joke and administrative horror. | Latin America | literary source | primary text + biography | USED |
| Sei Shonagon, lists | List as attention technology. | East Asia | prose form | primary text + translation | USED |

### OMENS / SUPERSTITIONS

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Black cat in five cultures | Bad sign in some places, good sign in others: omen as local UX. | Cross-Cultural | superstition | folklore collections + comparison | IDEA |
| Salt over shoulder | Expensive material becomes anxiety ritual. | Cross-Cultural | protection | superstition source + food history | IDEA |
| Knife through threshold | Threshold as social firewall. | Cross-Cultural | prohibition | folk-belief source | IDEA |
| Red thread / amulet thread | Protection as wearable boundary. | West Asia / South Asia / Cross-Cultural | charm | tradition-specific sources | IDEA |
| Eye twitching | Stress physiology plus asymmetric cultural interpretation. | Cross-Cultural | body omen | folk source + physiology source | IDEA |
| Birds fly low before rain | Insects, pressure, birds: three-link mechanism. | Cross-Cultural | weather omen | folklore + meteorology | IDEA |
| Dream of teeth falling out | Loss, debt, death, age: one image with many social explanations. | Cross-Cultural | dream omen | dream folklore + psychology history | IDEA |

### DIVINATION

Use `DIVINATION` for tarot, astrology, horoscopes, I Ching, runes, lots, cowrie shells, Ifa, geomancy, coffee grounds, dream books, bibliomancy, palmistry, oracle bones, and similar systems.

The post must explain the system, history, material method, symbolic grammar, and social function. It must not claim to predict the reader's future.

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Tarot before occultism | Tarot began as playing cards; occult meaning was layered later. | Europe | divination / cards | playing-card history + occult history | IDEA |
| The Fool card | Zero as threshold: not stupidity, but unassigned status. | Europe | tarot symbol | tarot history + image source | IDEA |
| The Tower card | Catastrophe as architecture failing, not divine punishment alone. | Europe / Cross-Cultural | tarot symbol | deck history + visual source | IDEA |
| Marseille vs Rider-Waite-Smith | One system changes when minor arcana become illustrated. | Europe / Global Modern | tarot system | deck history + image rights notes | IDEA |
| Pamela Colman Smith | The most-seen tarot images were drawn by a woman many users never name. | Europe / African Diaspora | tarot source | biography + deck history | IDEA |
| Zodiac means animals | `zodiac` is a circle of living figures, not just stars. | Europe / West Asia | astrology / etymology | etymology + astronomy history | IDEA |
| Tropical vs sidereal zodiac | Western seasonal zodiac and Indian sidereal zodiac answer different questions. | Cross-Cultural | astrology system | astronomy + Jyotish source | IDEA |
| Chinese zodiac Great Race | A 12-year animal cycle, not a monthly star sign. | East Asia | astrology / cycle | Chinese calendar source + folktale | IDEA |
| Saturn return | 29.5-year cycle as modern rite-of-passage language. | Global Modern | astrology / life cycle | astronomy + astrology-history source | IDEA |
| Precession and star signs | Astronomy exposes the difference between constellation and horoscope sign. | Cross-Cultural | astrology / astronomy | astronomy source + history of astrology | IDEA |
| Ifa divination | Oracle as trained literary corpus: 256 odu and interpretive discipline. | Africa / African Diaspora | oracle | Yoruba source + academic study | IDEA |
| Cowrie shells | Small objects as randomizer, archive, and social diagnosis. | Africa / African Diaspora | lots / oracle | ethnographic source | IDEA |
| I Ching hexagrams | Change as binary grammar before digital metaphor. | East Asia | oracle / text | primary text + translation note | IDEA |
| Oracle bones | Writing begins partly as a question to power and ancestors. | East Asia | oracle / writing | archaeology source + museum record | IDEA |
| Runes before rune-reading | Alphabet first, oracle later: writing and divination share the act of reading hidden order. | Europe | runes / oracle | runology source + Edda context | IDEA |
| Urim and Thummim | Biblical decision technology: sacred yes/no under uncertainty. | West Asia | lots | primary text + biblical scholarship | IDEA |
| Geomancy | Dots in sand become a portable decision machine across Africa, Arabic worlds, and Europe. | Cross-Cultural | geomancy | history of divination source | IDEA |
| Coffee-ground reading | Domestic residue as social theatre and diagnosis. | West Asia / Europe | household divination | ethnographic source | IDEA |
| Horoscope as media format | Newspaper horoscopes are a 20th-century content invention, not ancient format. | Global Modern | modern astrology | media history + astrology history | IDEA |

---

## Theme I - Desserts, Baking, Bread

### Sweet Branch

| Topic | Rubric | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|--------|-------|---------------|---------------|--------------|--------|
| Gulab jamun | SWEETS | Persian name, South Asian ritual sweet. | South Asia | sugar confection | food history + technique | IDEA |
| Laddu | SWEETS | Spherical sweet as gift, temple food, Diwali object. | South Asia | sugar confection / ritual sweet | food history + source note | IDEA |
| Halva | SWEETS | One word, many materials: sesame, semolina, flour, nut. | West Asia / Cross-Cultural | sugar confection | food history + etymology | IDEA |
| Lokum | SWEETS | Starch and syrup as slow resistance. | West Asia | sugar confection | food history + technique | IDEA |
| Mochi | SWEETS | Rice elasticity plus New Year risk. | East Asia | rice sweet / ritual | food history + safety note | IDEA |
| Wagashi | SWEETS | Season as edible miniature. | East Asia | ceremonial sweet | food history + cultural source | IDEA |
| Halo-halo | DESSERTS | A colonial archive in shaved ice. | Southeast Asia | cold dessert | food history + regional source | IDEA |
| Cendol | DESSERTS | Palm sugar, coconut, ice, green rice strands. | Southeast Asia | cold dessert | food history | IDEA |
| Malva pudding | DESSERTS / CAKES | Warm sponge plus sauce: Cape colonial food history. | Africa | cake / dessert | food history | IDEA |
| Basbousa | DESSERTS / SWEETS | Semolina and syrup: texture before ornament. | Africa / West Asia | syrup dessert | food history + technique | IDEA |
| Tres leches | CAKES | Cake that succeeds by refusing dryness. | Latin America | cake architecture | food history + technique | USED |
| Tiramisu | DESSERTS | Name means "pick me up"; cold architecture, not baked cake. | Europe | cold dessert | food history + technique | IDEA |

### Savory Branch

| Topic | Rubric | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|--------|-------|---------------|---------------|--------------|--------|
| Injera | FLATBREAD | Teff fermentation turns bread into plate and utensil. | Africa | fermented grain / flatbread heat | food history + technique | IDEA |
| Dosa | FLATBREAD | Fermented rice/urad batter as crisp timekeeping. | South Asia | fermented grain / flatbread heat | food science + food history | IDEA |
| Tortilla nixtamal | FLATBREAD | Lime-treated maize as ancient technology. | Latin America / Indigenous Americas | non-wheat staple | food history + food science | IDEA |
| Sangak | FLATBREAD | Bread baked on stones; surface becomes method. | West Asia | flatbread heat | food history | IDEA |
| Uzbek non | FLATBREAD | Two minutes on a tandoor wall. | Central Asia | flatbread heat | food history + technique | IDEA |
| Lavash | FLATBREAD | Thin bread as storage technology and shared object. | West Asia | flatbread heat / ceremonial bread | UNESCO + food history | IDEA |
| Empanada | PIES | Edge crimp as regional signature. | Latin America | savory pie | food history | IDEA |
| Samosa | PIES | Persian route into South Asian street food. | South Asia / West Asia | hand pie | food history + etymology | IDEA |
| Börek | PIES | Phyllo families as Ottoman food technology. | West Asia / Europe | savory pie | food history | IDEA |
| Jamaican patty | PIES | Colonial pastry, turmeric crust, portable heat. | African Diaspora / Island Cultures | hand pie / diaspora food | food history | IDEA |
| Khachapuri | PIES / FLATBREAD | Bread, cheese, boat, and regional identity. | West Asia | filled bread | food history | IDEA |
| Lammas loaf | BREAD | First grain becomes protective bread. | Europe | ceremonial bread | calendar source + food history | USED |

### Technique / RECIPE

| Topic | Rubric | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|--------|-------|---------------|---------------|--------------|--------|
| Gelatin vs agar | RECIPE | Same visual result, different temperature logic. | Cross-Cultural | food science | food science source | IDEA |
| Sugar stages | RECIPE | Thread, soft ball, hard crack: sugar becomes different materials. | Cross-Cultural | food science | professional baking source | IDEA |
| Hydration | RECIPE | 60% and 90% doughs are different species. | Cross-Cultural | fermented grain | professional baking source | IDEA |
| Steam in bread | RECIPE | Crust is controlled humidity. | Cross-Cultural | bread technique | food science | IDEA |

---

## Theme III - Calendar, Ritual, Time

### CYCLES

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Japanese 72 ko | Five-day microseasons as attention system. | East Asia | microseason | calendar source + cultural source | USED |
| Bengali six seasons | Monsoon as a full season, not weather. | South Asia | agricultural / monsoon | calendar source | IDEA |
| Sami eight seasons | Reindeer life makes the year more than four parts. | Arctic North | ecological time | Indigenous/cultural source | IDEA |
| Nyoongar six seasons | Local ecology as calendar; colonial four-season model fails. | Oceania | ecological time | Indigenous source | IDEA |
| Ethiopian 13 months | Time, church year, and civil date drift. | Africa | calendar system | official/cultural source | IDEA |
| Maya Tzolkin + Haab | Two calendars interlock into a 52-year round. | Indigenous Americas | calendar system | scholarly source | IDEA |
| Hijri lunar drift | Ramadan moves through every solar season in 33 years. | West Asia / Cross-Cultural | lunar | religious calendar source | IDEA |
| Metonic cycle | 19-year repair between moon and sun. | Europe / West Asia | lunar/solar | astronomy source | IDEA |

### CALENDAR / HERITAGE

| Topic | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|-------|---------------|---------------|--------------|--------|
| Diwali | Rows of lamps as infrastructure of light. | South Asia | fasting/feasting / light | religious/cultural source | IDEA |
| Eid al-Fitr sweets | Sweetness after a month of altered time. | West Asia / Cross-Cultural | fasting/feasting | religious calendar + food history | IDEA |
| Obon | Ancestors return through lanterns, dance, water. | East Asia | ancestor/death | cultural calendar source | IDEA |
| Día de los Muertos | Ofrenda as domestic architecture for the dead. | Latin America | ancestor/death | cultural source + UNESCO | IDEA |
| Yam Festival | New harvest forbidden until ritually released. | Africa | agricultural | cultural source | IDEA |
| Kwanzaa | A modern ritual openly invented in 1966. | African Diaspora / Global Modern | modern ritual | origin source + critical context | IDEA |
| Hula kahiko | Body as archive; chant and gesture under preservation pressure. | Oceania / Island Cultures | living heritage | cultural/UNESCO source | USED |
| Pansori | One singer, one drummer, one archive in the throat. | East Asia | living heritage | UNESCO + cultural source | IDEA |

### MODERN / RITES

| Topic | Rubric | Angle | cultural_zone | coverage_axis | source_stack | Status |
|-------|--------|-------|---------------|---------------|--------------|--------|
| Black Friday | MODERN | Shopping day as invented ritual with logistics and anxiety. | Global Modern | commercial modern | commerce stats + history | IDEA |
| Singles Day | MODERN | Anti-Valentine becomes biggest shopping ritual. | East Asia / Global Modern | commercial modern | commerce stats + history | IDEA |
| Earth Day | MODERN | Civic ritual invented in 1970, scaled globally. | Global Modern | protest/memorial | official history + context | IDEA |
| Apollo 11 | MODERN | A state ritual of technological awe and long pause. | Global Modern | technological anniversary | NASA + context | IDEA |
| Quinceanera | RITES | Fifteen as visible status change. | Latin America | initiation | cultural/anthropology source | IDEA |
| Bar/Bat Mitzvah | RITES | Reading becomes adulthood. | West Asia / Jewish diaspora | initiation | religious source + anthropology | IDEA |
| Coming of Age Day | RITES | State calendar turns age into public visibility. | East Asia | initiation/state | official source + cultural source | IDEA |
| Wedding anniversaries | RITES | Repetition of a rite, not the rite itself. | Global Modern | wedding/fertility | history + commerce/context | USED |
| 9/40 days mourning | RITES | Death as a sequence, not a single event. | Cross-Cultural | ancestor/death | tradition-specific sources | IDEA |

---

## Cross-Theme ETYMON

| Word | Slot | Angle | cultural_zone | coverage_axis | source_stack | Status |
|------|------|-------|---------------|---------------|--------------|--------|
| zodiac | 10:04 / 18:02 | "Circle of living beings" before horoscope industry. | Europe / West Asia | astrology / etymology | etymology + astronomy history | IDEA |
| tarot | 10:04 | Word history uncertain; uncertainty itself is part of the object. | Europe | divination / cards | specialist history | IDEA |
| oracle | 10:04 | From speaking to institution: a voice becomes a system. | Europe / Cross-Cultural | divination / etymology | etymology + classical source | IDEA |
| fate | 10:04 | Latin `fatum` means "what has been spoken." | Europe | fate / etymology | specialist dictionary | IDEA |
| karma | 10:04 | Not punishment, but action and consequence. | South Asia | word/etymology | Sanskrit source + context | IDEA |
| horoscope | 18:02 | Greek "hour watcher": originally a time-marker, now media format. | Europe / Global Modern | astrology / media | etymology + media history | IDEA |
| solstice | 18:02 | The sun does not stop; our description does. | Europe / Cross-Cultural | solar / etymology | etymology + astronomy | USED |
| bread | 15:04 | Five languages show bread as piece, food, loaf, struggle, offering. | Cross-Cultural | food etymology | specialist dictionaries | IDEA |
| halva | 15:04 | "Sweet" becomes a food family across languages. | West Asia / Cross-Cultural | sugar confection / etymology | etymology + food history | IDEA |

---

## Deprecated / Legacy Handling

Use `IDEAS_BANK_LEGACY.md` only for raw mining.

Before moving a legacy idea into this file:

1. Remove any "regional debt" framing.
2. Assign `cultural_zone`.
3. Assign `coverage_axis`.
4. Assign `source_stack`.
5. Choose current rubric from `RUBRIC_TAXONOMY.md`.
6. Rewrite hook using `CONTEMPORARY_STYLE_GUIDE.md`.
7. Check the month against `MONTHLY_PLANNING_TEMPLATE.md`.
