# Graph Report - .  (2026-06-23)

## Corpus Check
- Corpus is ~7,625 words - fits in a single context window. You may not need a graph.

## Summary
- 11 nodes · 7 edges · 5 communities (2 shown, 3 thin omitted)
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_H1 Roadmap & Tactics|H1 Roadmap & Tactics]]
- [[_COMMUNITY_Skeleton 2026 Narrative|Skeleton 2026 Narrative]]
- [[_COMMUNITY_June Workflows|June Workflows]]
- [[_COMMUNITY_Alert Keywords|Alert Keywords]]
- [[_COMMUNITY_ESC History Database|ESC History Database]]

## God Nodes (most connected - your core abstractions)
1. `Q1: The Spark` - 3 edges
2. `Skeleton 2026 Narrative` - 3 edges
3. `H1 2026 Roadmap` - 2 edges
4. `Q2: The Vibration` - 1 edges
5. `Q1 Tactical Focus` - 1 edges
6. `Year of the Fire Horse` - 1 edges
7. `Depth over Surface` - 1 edges
8. `YV Master Plan June` - 1 edges
9. `Daily Plan 09.06` - 1 edges
10. `Alert Keywords System` - 0 edges

## Surprising Connections (you probably didn't know these)
- `Skeleton 2026 Narrative` --semantically_similar_to--> `Q1: The Spark`  [INFERRED] [semantically similar]
  01_YOURVISION/06_TIMELINE/strategy/2026/SKELETON_2026.md → 01_YOURVISION/06_TIMELINE/strategy/2026/H1_ROADMAP.md
- `Q1 Tactical Focus` --semantically_similar_to--> `Q1: The Spark`  [INFERRED] [semantically similar]
  01_YOURVISION/06_TIMELINE/strategy/2026/Q1_TACTICAL.md → 01_YOURVISION/06_TIMELINE/strategy/2026/H1_ROADMAP.md
- `YV Master Plan June` --conceptually_related_to--> `Daily Plan 09.06`  [INFERRED]
  01_YOURVISION/06_TIMELINE/master_plans/06/YV_Plan_06.md → 01_YOURVISION/06_TIMELINE/daily_workflow/daily_plan_09.06.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Q1 2026 Strategic Alignment** — 2026_h1_roadmap_q1_the_spark, 2026_q1_tactical_tactical_plan, 2026_skeleton_2026_narrative [INFERRED 0.85]

## Communities (5 total, 3 thin omitted)

### Community 0 - "H1 Roadmap & Tactics"
Cohesion: 0.50
Nodes (4): Q1: The Spark, Q2: The Vibration, H1 2026 Roadmap, Q1 Tactical Focus

### Community 1 - "Skeleton 2026 Narrative"
Cohesion: 0.67
Nodes (3): Depth over Surface, Year of the Fire Horse, Skeleton 2026 Narrative

## Knowledge Gaps
- **7 isolated node(s):** `Alert Keywords System`, `ESC History Database`, `Q2: The Vibration`, `Q1 Tactical Focus`, `Year of the Fire Horse` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Q1: The Spark` connect `H1 Roadmap & Tactics` to `Skeleton 2026 Narrative`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Why does `Skeleton 2026 Narrative` connect `Skeleton 2026 Narrative` to `H1 Roadmap & Tactics`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Q1: The Spark` (e.g. with `Q1 Tactical Focus` and `Skeleton 2026 Narrative`) actually correct?**
  _`Q1: The Spark` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Alert Keywords System`, `ESC History Database`, `Q2: The Vibration` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._