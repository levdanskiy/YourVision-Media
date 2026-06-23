#!/usr/bin/env python3
"""Build machine-readable canon and visual-history indexes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from almanac_common import DATABASES, ROOT, iter_posts, split_values, visual_prompt


def fallback_canon_id(rubric: str, metadata: dict[str, str], slug: str) -> str:
    axes = split_values(metadata.get("coverage_axis") or metadata.get("coverage_axes", ""))
    anchor = axes[0] if axes else slug or "unclassified"
    clean = "-".join(anchor.lower().replace("_", "-").split())
    return f"{rubric.lower()}:{clean}"


def main() -> int:
    registry: list[dict[str, object]] = []
    visual_rows: list[dict[str, str]] = []
    for post in iter_posts(prefixes={"AL", "SV", "SP"}):
        relative = str(post.path.relative_to(ROOT))
        canon_id = post.canon_id or fallback_canon_id(post.rubric, post.metadata, post.slug)
        entry = {
            "post_id": post.post_id,
            "date": post.publication_date.isoformat(),
            "slot": post.slot,
            "kind": post.prefix,
            "rubric": post.rubric,
            "title": post.title,
            "slug": post.slug,
            "canon_id": canon_id,
            "canon_id_explicit": bool(post.canon_id),
            "angle_id": post.angle_id,
            "series_id": post.series_id,
            "continuity_notes": post.metadata.get("continuity_notes", ""),
            "cultural_zone": post.metadata.get("cultural_zone", ""),
            "secondary_zones": split_values(post.metadata.get("secondary_zones", "")),
            "coverage_axes": split_values(
                post.metadata.get("coverage_axis") or post.metadata.get("coverage_axes", "")
            ),
            "source_types": split_values(
                post.metadata.get("source_type") or post.metadata.get("source_types", "")
            ),
            "status": post.metadata.get("status", ""),
            "path": relative,
        }
        registry.append(entry)
        prompt = visual_prompt(post.text)
        if prompt:
            visual_rows.append(
                {
                    "date": post.publication_date.isoformat(),
                    "post_id": post.post_id,
                    "rubric": post.rubric,
                    "prompt": prompt,
                    "path": relative,
                }
            )

    DATABASES.mkdir(parents=True, exist_ok=True)
    indexes = DATABASES / "indexes"
    indexes.mkdir(parents=True, exist_ok=True)
    output = DATABASES / "CANON_REGISTRY.json"
    output.write_text(
        json.dumps({"schema_version": 1, "posts": registry}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    visual_path = indexes / "visual_history.csv"
    with visual_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "post_id", "rubric", "prompt", "path"])
        writer.writeheader()
        writer.writerows(visual_rows)
    print(f"CANON: {len(registry)} posts -> {output}")
    print(f"VISUALS: {len(visual_rows)} prompts -> {visual_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
