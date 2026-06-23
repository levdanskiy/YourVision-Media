#!/usr/bin/env python3
"""Render the visible pre-writing brief required for every requested day."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import timedelta

from almanac_common import DATABASES, REPORTS, iter_posts, parse_date_target, split_values
from daily_improvement import report_path as improvement_path, status as improvement_status
from trend_due import is_due as trend_is_due, report_path as trend_path


def render(target: str) -> str:
    day = parse_date_target(target)
    month = day.strftime("%Y-%m")
    month_posts = iter_posts(month, prefixes={"AL", "SV", "SP"})
    previous = [post for post in month_posts if post.publication_date < day and post.prefix == "AL"]
    recent = [post for post in previous if post.publication_date >= day - timedelta(days=14)]
    rubric_counts = Counter(post.rubric for post in previous)
    recent_rubrics = Counter(post.rubric for post in recent)
    zones = Counter(post.metadata.get("cultural_zone", "missing") for post in previous)
    services = Counter(post.prefix for post in month_posts if post.publication_date <= day)
    current_week_services = [
        post for post in month_posts
        if post.prefix == "SV" and post.publication_date.isocalendar()[:2] == day.isocalendar()[:2]
    ]
    weekly_oracle = sum(1 for post in current_week_services if "ORACLE-NOTE" in post.path.name)
    weekly_radar = sum(1 for post in current_week_services if "CALENDAR-RADAR" in post.path.name)

    registry = json.loads((DATABASES / "SERIES_REGISTRY.json").read_text(encoding="utf-8"))
    due_series = [
        item["series_id"] for item in registry.get("series", [])
        if item.get("next_due") and item["next_due"] <= target and item.get("status") in {"active", "pilot"}
    ]
    improvement = improvement_path(day)
    improvement_state = improvement_status(improvement.read_text(encoding="utf-8")) if improvement.exists() else "missing"
    publications_path = DATABASES / "PUBLICATION_REGISTRY.json"
    publications = json.loads(publications_path.read_text(encoding="utf-8")) if publications_path.exists() else {"posts": []}
    publication_counts = Counter(item.get("publication_status", "missing") for item in publications.get("posts", []))
    assets_path = DATABASES / "ASSET_REGISTRY.json"
    assets = json.loads(assets_path.read_text(encoding="utf-8")) if assets_path.exists() else {"assets": []}
    evidence_path = DATABASES / "EVIDENCE_REGISTRY.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8")) if evidence_path.exists() else {"posts": []}
    experiments_path = DATABASES / "EXPERIMENT_REGISTRY.json"
    experiments = json.loads(experiments_path.read_text(encoding="utf-8")) if experiments_path.exists() else {"experiments": []}
    running_experiments = [item for item in experiments.get("experiments", []) if item.get("status") == "running"]
    due_experiments = [item["experiment_id"] for item in running_experiments if item.get("end_date", "9999-12-31") <= target]
    incidents_path = DATABASES / "EDITORIAL_INCIDENTS.json"
    incidents = json.loads(incidents_path.read_text(encoding="utf-8")) if incidents_path.exists() else {"incidents": []}
    open_incidents = [item for item in incidents.get("incidents", []) if item.get("status") == "open"]
    zero_or_low = [name for name, count in sorted(rubric_counts.items(), key=lambda item: (item[1], item[0])) if count <= 1]
    recent_axes = Counter(
        axis
        for post in recent
        for axis in split_values(post.metadata.get("coverage_axis") or post.metadata.get("coverage_axes", ""))
    )

    lines = [
        f"# Editorial Brief - {target}",
        "",
        "## Rotation",
        f"- Prepared AL before date: {len(previous)}; recent 14 days: {len(recent)}.",
        f"- Recent rubrics: {', '.join(f'{k}={v}' for k, v in recent_rubrics.most_common()) or 'none'}.",
        f"- Low-frequency queue: {', '.join(zero_or_low[:10]) or 'derive from monthly plan'}.",
        f"- Cultural zones: {', '.join(f'{k}={v}' for k, v in zones.most_common()) or 'none'}.",
        f"- Repeated recent axes to avoid: {', '.join(k for k, v in recent_axes.most_common(8) if v > 1) or 'none'}.",
        "",
        "## Service And Series",
        f"- Month service load: SV={services['SV']}; SP={services['SP']}.",
        f"- Required weekly pair: ORACLE-NOTE={weekly_oracle}/1; CALENDAR-RADAR={weekly_radar}/1.",
        f"- Due series: {', '.join(due_series) or 'none'}.",
        "",
        "## Operational State",
        f"- Publication registry: {', '.join(f'{k}={v}' for k, v in publication_counts.most_common()) or 'missing'}.",
        f"- Real assets registered: {len(assets.get('assets', []))}; evidence-reviewed posts: {len(evidence.get('posts', []))}.",
        f"- Running experiments: {', '.join(item['experiment_id'] for item in running_experiments) or 'none'}.",
        f"- Experiment reviews due: {', '.join(due_experiments) or 'none'}; open incidents: {len(open_incidents)}.",
        "- Semantic memory: search before approving a reused entity, holiday, dish or central claim.",
        "",
        "## Change Control",
        f"- Five-day trend review: {'DUE' if trend_is_due(day) else 'not due'}; report: {'ready' if trend_path(day).exists() else 'missing'}.",
        f"- Daily improvement: {improvement_state}; record: {improvement}.",
        "- Before delivery: show this report, name the chosen experiment, and state what was applied.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = render(args.target)
    print(report, end="")
    if args.write:
        path = REPORTS / "briefs" / f"BRIEF-{args.target}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
        print(f"WROTE: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
