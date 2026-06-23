# Graph Report - 08_HUB  (2026-06-23)

## Corpus Check
- 13 files · ~62,537 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 34 nodes · 32 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.91)
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

## God Nodes (most connected - your core abstractions)
1. `sync()` - 6 edges
2. `DATA` - 5 edges
3. `rebuild()` - 4 edges
4. `render` - 4 edges
5. `index.html structure` - 4 edges
6. `get_telegram_news()` - 3 edges
7. `Heart-Shape Flags Rule` - 3 edges
8. `Eurovision Song Contest Asia 2026 Graphic` - 3 edges
9. `Eurovision Song Contest Asia 2026` - 3 edges
10. `parse_poll()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `rebuild()` --references--> `index.html structure`  [EXTRACTED]
  tools/rebuild_perfect.py → 08_HUB/index.html
- `Cooperative Sync Workflow` --conceptually_related_to--> `sync()`  [EXTRACTED]
  08_HUB/tools/README.md → tools/yv_tg_sync.py
- `sync()` --references--> `DATA`  [EXTRACTED]
  tools/yv_tg_sync.py → 08_HUB/data.js
- `sync()` --calls--> `normalize_title`  [EXTRACTED]
  tools/yv_tg_sync.py → 08_HUB/tools/yv_tg_sync.py
- `render` --references--> `DATA`  [EXTRACTED]
  08_HUB/index.html → 08_HUB/data.js

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hub Content Pipeline** — tools_yv_tg_sync_sync, tools_rebuild_perfect_rebuild, 08_hub_data_data, 08_hub_index_html_structure [INFERRED 0.95]
- **Hub Layout Patchers** — tools_fix_hub_layout_news_render_new, tools_restore_render_new_render_js [INFERRED 0.85]

## Communities (13 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.47
Nodes (5): Cooperative Sync Workflow, get_telegram_news(), normalize_title, parse_poll(), sync()

### Community 1 - "Community 1"
Cohesion: 0.40
Nodes (4): DATA, data.js data model rules, update_odds, rebuild()

### Community 2 - "Community 2"
Cohesion: 0.50
Nodes (5): getHeartUrl, linkify, render, replaceFlags, Heart-Shape Flags Rule

### Community 3 - "Community 3"
Cohesion: 0.83
Nodes (4): 14 November 2026, Eurovision Song Contest Asia 2026, Eurovision Song Contest Asia 2026 Graphic, Bangkok

### Community 4 - "Community 4"
Cohesion: 1.00
Nodes (3): index.html structure, news_render_new, new_render_js

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): 70th Anniversary Design, United by Music 70th Anniversary Logo, United by Music Slogan

## Knowledge Gaps
- **7 isolated node(s):** `update_odds`, `normalize_title`, `Vienna 2026 Insider Hub`, `linkify`, `White Heart Icon` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `sync()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `DATA` connect `Community 1` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `rebuild()` connect `Community 1` to `Community 0`, `Community 4`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **What connects `update_odds`, `normalize_title`, `Vienna 2026 Insider Hub` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._