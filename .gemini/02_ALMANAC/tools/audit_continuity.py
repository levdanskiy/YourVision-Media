#!/usr/bin/env python3
"""Detect exact and near continuity collisions in the archive."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import timedelta

from almanac_common import iter_posts, normalized_words, split_values


def overlap(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?")
    parser.add_argument("--cooldown", type=int, default=45)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    archive = iter_posts(prefixes={"AL", "SV", "SP"})
    selected = iter_posts(args.target, prefixes={"AL", "SV", "SP"}) if args.target else archive
    selected_paths = {post.path for post in selected}
    errors: list[str] = []
    warnings: list[str] = []

    exact_fields: dict[str, dict[str, list]] = {"post_id": defaultdict(list), "slug": defaultdict(list)}
    for post in archive:
        if post.post_id:
            exact_fields["post_id"][post.post_id.lower()].append(post)
        if post.slug:
            exact_fields["slug"][post.slug.lower()].append(post)
    for field, groups in exact_fields.items():
        for value, posts in groups.items():
            if len(posts) > 1 and any(post.path in selected_paths for post in posts):
                message = f"duplicate {field} `{value}`: " + ", ".join(str(p.path) for p in posts)
                if field == "post_id":
                    errors.append(message)
                else:
                    warnings.append(message)

    explicit: dict[tuple[str, str], list] = defaultdict(list)
    for post in archive:
        if post.canon_id and post.angle_id:
            explicit[(post.canon_id, post.angle_id)].append(post)
    for key, posts in explicit.items():
        if len(posts) > 1 and any(post.path in selected_paths for post in posts):
            errors.append(
                f"duplicate canon angle `{key[0]}/{key[1]}`: " + ", ".join(str(p.path) for p in posts)
            )

    for current in selected:
        current_axes = set(split_values(current.metadata.get("coverage_axis") or current.metadata.get("coverage_axes", "")))
        current_title = normalized_words(current.title)
        for previous in archive:
            if previous.path == current.path or previous.publication_date >= current.publication_date:
                continue
            age = current.publication_date - previous.publication_date
            if age > timedelta(days=args.cooldown):
                continue
            if current.canon_id and previous.canon_id and current.canon_id == previous.canon_id:
                warnings.append(
                    f"canon cooldown {age.days}d `{current.canon_id}`: {previous.path.name} -> {current.path.name}"
                )
                continue
            previous_axes = set(
                split_values(previous.metadata.get("coverage_axis") or previous.metadata.get("coverage_axes", ""))
            )
            axis_score = overlap(current_axes, previous_axes) if current_axes and previous_axes else 0.0
            title_score = overlap(current_title, normalized_words(previous.title))
            if axis_score >= 0.67 and title_score >= 0.25:
                warnings.append(
                    f"near-repeat {age.days}d axes={axis_score:.2f} title={title_score:.2f}: "
                    f"{previous.path.name} -> {current.path.name}"
                )

    for message in sorted(set(errors)):
        print(f"ERROR: {message}")
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(f"CONTINUITY: {len(errors)} errors, {len(set(warnings))} warnings")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
