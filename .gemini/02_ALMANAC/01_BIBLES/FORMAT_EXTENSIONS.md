# FORMAT EXTENSIONS

These are lenses, subtypes, and service formats that use the existing slots.
They are not filename rubrics unless `RUBRIC_TAXONOMY.md` explicitly lists them
as a core rubric.

`FERMENT` and `PRESERVE` were promoted from lenses to core 15:04 rubrics. Use
them in filenames when the living culture or preservation process is the object.

## Accepted As Lenses

| Proposed Label | Use As | Slot | Rule |
|----------------|--------|------|------|
| `TABLE` | `FOODWAYS` or `FEAST` | `15:04` / `18:02` | How people eat together: order, seating, refusal, sharing, silence, service. |
| `STREET` | `FOODWAYS`, sometimes `PIES`, `FLATBREAD`, `CONDIMENTS` | `15:04` | Food without a formal table: stall, wrapper, queue, hand, street heat. |
| `STAPLE` | `FOODWAYS`, `BREAD`, `FLATBREAD`, `SOUP` | `15:04` | Base food as cultural axis: rice, maize, teff, millet, cassava, oil. |
| `MARKET` | `FOODWAYS`, `CONDIMENTS`, `PANTRY` | `15:04` | Bazaar/market as food route, bargaining, season, public abundance. |
| `FASTING_FOOD` | `FOODWAYS`, `SOUP`, `FEAST` | `15:04` / `18:02` | Food made by restriction: fast, abstinence, substitutions, breaking fast. |
| `SACRED_FOOD` | `FOODWAYS`, `FEAST`, `BREAD`, `SOUP` | `15:04` / `18:02` | Kosher/halal/prasad/communion/offering/purity boundary. |
| `FOOD_POWER` | `FOODWAYS`, `PANTRY`, `CONDIMENTS` | `15:04` | Class, status, empire, trade, scarcity, hunger, luxury, control. |
| `FOOD_ROUTE` | `FOODWAYS`, `CONDIMENTS`, `DRINKS`, `PANTRY` | `15:04` | Ingredient migration through trade, colonization, diaspora, climate, ports. |
| `SWEET_BREAD` | `BUNS` | `15:04` | Sweet yeasted festive bread; do not file as `BREAD`. |
| `SUGAR_STAGE` | `SWEETS`, `RECIPE`, `PATISSERIE` | `15:04` | Syrup stages, caramel, crystallization, praline, brittle, sugar chemistry. |
| `GESTURE` | `OMENS` or `RITES` | `10:04` / `18:02` | A body action: knock, spit, cross threshold, cover mirror, throw salt. |
| `LOST` | `SOURCE`, `ETYMON`, `FRAGMENT`, sometimes `HERITAGE` | `10:04` | Lost texts, fragments, vanished languages, burned libraries, missing versions. |
| `TABOO` | `OMENS`, `LORE`, `RITES`, `FEAST` | `10:04` / `18:02` | Absolute prohibition, purity boundary, forbidden act/food/name. |
| `DREAM` | `DIVINATION`, `OMENS`, `SOURCE`, `LORE` | `10:04` | Dream books, incubation, prophetic dreams, inner sign systems. |
| `COSMOGONY` | `LORE`, `SOURCE` | `10:04` | Origin of world/humans/order: egg, body, flood, demiurge, chaos fight. |
| `ESCHATOLOGY` | `LORE`, `CYCLES`, `SOURCE` | `10:04` / `18:02` | End of world, afterlife, final age, catastrophe, renewal. |
| `TRICKSTER` | `LORE`, `PERSONAE` | `10:04` | Rule-breaking mediator across cultures; not a generic funny character. |
| `THRESHOLD` | `OMENS`, `OBJECTS`, `CHRONOS`, `RITES` | `10:04` / `18:02` | Door, bridge, crossroads, well, shore, mirror, liminal place. |
| `RITUAL_ACTION` | `RITES`, `FEAST`, `OMENS`, `OBJECTS` | `10:04` / `18:02` | Repeated action as a score: order, gesture, object, mistake, repair. |
| `FOLK_HERO` | `PERSONAE`, `LORE` | `10:04` | Historical or semi-historical figure turned social myth. |
| `PLACE` | `LORE`, `SOURCE`, `HERITAGE` | `10:04` / `18:02` | Mythic or unreachable place: Avalon, Shambhala, El Dorado, hidden city. |
| `CURSE_BLESSING` | `OMENS`, `SOURCE`, `LORE` | `10:04` | Speech act with power: curse, blessing, vow, malediction, benediction. |
| `WORD_TABOO` | `ETYMON`, `OMENS`, `SOURCE` | `10:04` / `18:02` | Unsaid names, euphemisms, divine names, replacement speech. |
| `MEDIATOR` | `PERSONAE`, `RITES`, `DIVINATION` | `10:04` / `18:02` | Shaman, mudang, curandero, oracle specialist, between-world profession. |
| `SACRED_PROFANE` | `LORE`, `OBJECTS`, `RITES`, `HERITAGE` | `10:04` / `18:02` | Sacred space, axis mundi, hierophany, ordinary object becoming charged. |
| `ANIMAL_ANCESTOR` | `BESTIARY`, `LORE`, `OMENS` | `10:04` | Real animal as ancestor, creator, sacred kin, clan sign. |
| `CULTURE_HERO` | `PERSONAE`, `LORE` | `10:04` | Bringer of fire, writing, agriculture, craft, death, law. |
| `FEAST_TABLE` | `FEAST` | `18:02` | Holiday table as ritual map: foods, exclusions, order, offerings, changes. |
| `LIMINAL` | `CHRONOS`, `CALENDAR`, `RITES`, `CYCLES` | `18:02` | Eve, interval, between-days, charged waiting period. |
| `FAST` | `FEAST`, `RITES`, `CALENDAR` | `18:02` | Abstinence as calendar structure, not diet advice. |
| `BIOGRAPHICAL_DATE` | `MODERN`, `CALENDAR`, `SOURCE` | `18:02` | Birth/death/publication/action anniversary that became a cultural ritual. |

Use the visible rubric in the filename. The lens may appear in metadata:

```text
// FORMAT_LENS: DREAM
```

For `DIVINATION`, use subtypes rather than new rubrics:

```text
// FORMAT_SUBTYPE: ASTRAL
```

Allowed divination subtypes: `ASTRAL`, `CARD`, `TEXT_ORACLE`,
`LOT_GEOMANTIC`, `BODY`, `NATURE_SIGN`, `NUMBER`, `MODERN_MEDIA`.

## Not Core Rubrics

Do not add these as `AL-*` rubrics unless the validator and full system are updated:
- `VOICE`
- `ARCHIVE`
- `QUESTION`
- `COLLAB`
- `VISUAL_ESSAY`

Use them as `SV` service types or external distribution formats.

## Cross-Theme Rule

Cross-theme posts are allowed when the slot object remains clear:

| Cross Theme | Correct Slot | Example |
|-------------|--------------|---------|
| Myth + Food | `15:04` if food is the object; `10:04` if myth is the object. | Lammas loaf as bread vs Lugh as personae. |
| Food + Holiday | `18:02 FEAST` if table/date is the object; `15:04 FOODWAYS` if eating practice is the object. | Iftar table vs date technique. |
| Myth + Holiday | `18:02 CALENDAR/WHEEL` if the date is the object; `10:04 LORE` if the story is the object. | Kupala date split vs Gogol's Kupala text. |
| Text + Food | `15:04` only if the food technique remains central. | Croissant etymology inside PATISSERIE. |

## Quality Guard

The lens must add a mechanism. If it only adds aesthetic flavor, remove it.

Good:
- `TABLE`: who sits, who serves, what is refused, what changed.
- `STREET`: wrapper, stall, queue, hand, body position, no formal table.
- `GESTURE`: body action, social anxiety, protective logic.
- `LOST`: what survives, what is missing, who copied or destroyed it.
- `DREAM`: source of dream grammar, where dream appears, what it authorizes.
- `TABOO`: exact prohibition, boundary, consequence, who enforces it.
- `FAST`: what is refused, for how long, who is exempt, how the fast ends.

Bad:
- `TABLE`: "people gathered together".
- `STREET`: "colorful street food".
- `GESTURE`: "symbolic gesture".
- `LOST`: vague nostalgia for lost knowledge.
- `DREAM`: "your dream means".
- `TABOO`: "ancient rules were strict".
