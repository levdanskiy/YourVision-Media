# Graph Report - 09_CHARTS  (2026-06-23)

## Corpus Check
- Corpus is ~11,774 words - fits in a single context window. You may not need a graph.

## Summary
- 42 nodes · 44 edges · 16 communities (7 shown, 9 thin omitted)
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 8 edges
2. `clean_typography()` - 4 edges
3. `generate_cards()` - 4 edges
4. `main()` - 4 edges
5. `clean_typography()` - 3 edges
6. `get_scheduled_slots()` - 3 edges
7. `main()` - 3 edges
8. `generate_svg()` - 3 edges
9. `main()` - 3 edges
10. `sync_to_hub()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `main()` --implements--> `Reach Threshold`  [INFERRED]
  tools/yv_allmix_sync.py → 01_YOURVISION/09_CHARTS/YV_Charts_Manual.md
- `main()` --implements--> `Hit-Maker Scoring System`  [INFERRED]
  tools/yv_allmix_sync.py → 01_YOURVISION/09_CHARTS/YV_Charts_Manual.md
- `main()` --conceptually_related_to--> `Generated Cards (Vibe Shift)`  [INFERRED]
  tools/yv_allmix_sync.py → 01_YOURVISION/09_CHARTS/tools/generated_cards.txt
- `generate_svg()` --conceptually_related_to--> `Energy Arc Balance`  [INFERRED]
  tools/yv_energy_visualizer.py → 01_YOURVISION/09_CHARTS/YV_Charts_Manual.md
- `generate_cards()` --implements--> `Reach Threshold`  [INFERRED]
  tools/yv_card_generator.py → 01_YOURVISION/09_CHARTS/YV_Charts_Manual.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **YV Chart Directions** — 09_charts_yv_charts_manual_eurogroove, 09_charts_yv_charts_manual_worldsound, 09_charts_yv_charts_manual_allmix, 09_charts_yv_charts_manual_rutop [EXTRACTED 1.00]
- **YV Chart Processing Tools** — tools_yv_allmix_sync_main, tools_yv_card_generator_main, tools_yv_hub_sync_main, tools_yv_qc_validator_validate_tracklist [INFERRED 0.85]

## Communities (16 total, 9 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (7): AllMix: Vibe Shift 2026, Hit-Maker Scoring System, Generated Cards (Vibe Shift), clean_typography(), get_flag_url(), main(), parse_votes()

### Community 1 - "Community 1"
Cohesion: 0.53
Nodes (5): Reach Threshold, clean_typography(), generate_cards(), main(), parse_excel_results()

### Community 2 - "Community 2"
Cohesion: 0.60
Nodes (4): StrawPoll Voting, check_plans(), get_scheduled_slots(), main()

### Community 3 - "Community 3"
Cohesion: 0.67
Nodes (3): Energy Arc Balance, lint_typography(), validate_tracklist()

### Community 4 - "Community 4"
Cohesion: 0.83
Nodes (3): generate_svg(), main(), parse_tracklist()

### Community 5 - "Community 5"
Cohesion: 0.83
Nodes (3): get_country_code(), main(), sync_to_hub()

## Knowledge Gaps
- **12 isolated node(s):** `Eurogroove`, `WorldSound`, `AllMix`, `RuTop`, `Joker Rule` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `clean_typography()` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `lint_typography()` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `main()` (e.g. with `Hit-Maker Scoring System` and `Reach Threshold`) actually correct?**
  _`main()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `clean_typography()` (e.g. with `clean_typography()` and `lint_typography()`) actually correct?**
  _`clean_typography()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Eurogroove`, `WorldSound`, `AllMix` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._