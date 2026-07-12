#!/usr/bin/env python3
"""Detect visually repetitive prompts in a rolling archive window."""

from __future__ import annotations

import argparse
from datetime import timedelta

from almanac_common import iter_posts, normalized_words, visual_prompt


BOILERPLATE = normalized_words(
    "contemporary editorial photography documentary still life shot film kodak portra no text logos people"
)


def tokens(text: str) -> set[str]:
    return normalized_words(text) - BOILERPLATE


def similarity(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?")
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--threshold", type=float, default=0.52)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    archive = iter_posts(prefixes={"AL", "SV", "SP"})
    selected = iter_posts(args.target, prefixes={"AL", "SV", "SP"}) if args.target else archive
    warnings: list[str] = []
    missing: list[str] = []
    for current in selected:
        current_prompt = visual_prompt(current.text)
        if current.prefix == "AL" and not current_prompt:
            missing.append(str(current.path))
            continue
        current_tokens = tokens(current_prompt)
        for previous in archive:
            if previous.path == current.path or previous.publication_date >= current.publication_date:
                continue
            age = current.publication_date - previous.publication_date
            if age > timedelta(days=args.window):
                continue
            previous_prompt = visual_prompt(previous.text)
            if not previous_prompt:
                continue
            score = similarity(current_tokens, tokens(previous_prompt))
            if score >= args.threshold:
                warnings.append(
                    f"visual similarity {score:.2f} ({age.days}d): {previous.path.name} -> {current.path.name}"
                )
    for path in missing:
        print(f"ERROR: missing Visual Prompt: {path}")
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(f"VISUAL CONTINUITY: {len(missing)} errors, {len(set(warnings))} warnings")
    return 1 if missing or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
