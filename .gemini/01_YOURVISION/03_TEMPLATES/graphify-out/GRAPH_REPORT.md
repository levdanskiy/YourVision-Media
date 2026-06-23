# Graph Report - 03_TEMPLATES  (2026-06-23)

## Corpus Check
- Corpus is ~1,203 words - fits in a single context window. You may not need a graph.

## Summary
- 25 nodes · 24 edges · 4 communities
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `Chart Post Format` - 10 edges
2. `YOURVISION_OS.md` - 5 edges
3. `LONGREAD Post Format` - 3 edges
4. `YOURVISION_OS.md` - 2 edges
5. `DNA Post Format` - 2 edges
6. `Vienna Index` - 2 edges
7. `YOURVISION_OS` - 2 edges
8. `YOURVISION_OS` - 2 edges
9. `VERDICT Post Format` - 2 edges
10. `Vienna Index (Live)` - 2 edges

## Surprising Connections (you probably didn't know these)
- `YOURVISION_OS` --semantically_similar_to--> `YOURVISION_OS.md`  [INFERRED] [semantically similar]
  01_YOURVISION/03_TEMPLATES/post_longread.md → 01_YOURVISION/03_TEMPLATES/post_standard.md
- `YOURVISION_OS` --semantically_similar_to--> `YOURVISION_OS.md`  [INFERRED] [semantically similar]
  01_YOURVISION/03_TEMPLATES/post_verdict.md → 01_YOURVISION/03_TEMPLATES/post_standard.md
- `YOURVISION_OS.md` --semantically_similar_to--> `YOURVISION_OS.md`  [INFERRED] [semantically similar]
  01_YOURVISION/03_TEMPLATES/post_flash.md → 01_YOURVISION/03_TEMPLATES/post_standard.md
- `YOURVISION_OS` --semantically_similar_to--> `YOURVISION_OS.md`  [INFERRED] [semantically similar]
  01_YOURVISION/03_TEMPLATES/post_poll.md → 01_YOURVISION/03_TEMPLATES/post_standard.md
- `Vienna Index` --semantically_similar_to--> `Vienna Index (Live)`  [INFERRED] [semantically similar]
  01_YOURVISION/03_TEMPLATES/post_longread.md → 01_YOURVISION/03_TEMPLATES/post_verdict.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **YourVision Post Formats** — 03_templates_post_chart_chart_format, 03_templates_post_flash_flash_format, 03_templates_post_longread_longread_format, 03_templates_post_poll_poll_format, 03_templates_post_standard_standard_format, 03_templates_post_verdict_verdict_format [INFERRED 0.95]

## Communities (4 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.18
Nodes (11): AllMix, Chart Post Format, EuroGroove, Phase 1 - ANNOUNCE, Phase 2 - NOMINEES DETAIL, Phase 3 - REMINDER, Phase 4 - RESULTS, RuTop (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (6): FLASH Post Format, YOURVISION_OS.md, POLL Post Format, YOURVISION_OS, STANDARD Post Format, YOURVISION_OS.md

### Community 2 - "Community 2"
Cohesion: 0.40
Nodes (5): DNA Post Format, Vienna Index, VERDICT Post Format, Vienna Index (Live), YOURVISION_OS

### Community 3 - "Community 3"
Cohesion: 0.67
Nodes (3): LONGREAD Post Format, VISION Post Format, YOURVISION_OS

## Knowledge Gaps
- **14 isolated node(s):** `Phase 1 - ANNOUNCE`, `Phase 2 - NOMINEES DETAIL`, `Phase 3 - REMINDER`, `Phase 4 - RESULTS`, `WorldSound` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `YOURVISION_OS.md` connect `Community 1` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `YOURVISION_OS` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `YOURVISION_OS.md` (e.g. with `YOURVISION_OS.md` and `YOURVISION_OS`) actually correct?**
  _`YOURVISION_OS.md` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Phase 1 - ANNOUNCE`, `Phase 2 - NOMINEES DETAIL`, `Phase 3 - REMINDER` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._