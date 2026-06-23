#!/usr/bin/env python3
"""Build searchable semantic memory and detect meaning-level repetition."""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
from collections import Counter
from datetime import timedelta

from almanac_common import DATABASES, ROOT, iter_posts, normalized_words, split_values


DB = DATABASES / "indexes" / "semantic_memory.sqlite"
STOP = {
    "это", "как", "для", "что", "его", "она", "они", "или", "уже", "ещё", "еще", "под", "над", "без",
    "при", "где", "когда", "потом", "только", "так", "тот", "эта", "этот", "был", "была", "были", "есть",
    "the", "and", "for", "with", "from", "this", "that", "into", "shot", "film", "kodak", "portra",
    "visual", "prompt", "grade", "almanac", "publicaton", "timezone", "готов", "status", "rubric",
}


def clean_body(text: str) -> str:
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"^//.*$", "", text, flags=re.M)
    text = re.sub(r"\*\*Visual Prompt:\*\*.*\Z", "", text, flags=re.S | re.I)
    text = re.sub(r"[`*_#>|]", " ", text)
    return text


def weighted_tokens(post) -> Counter[str]:
    body = normalized_words(clean_body(post.text)) - STOP
    title = normalized_words(post.title) - STOP
    axes = set(split_values(post.metadata.get("coverage_axis") or post.metadata.get("coverage_axes", "")))
    result = Counter(body)
    for token in title:
        result[token] += 4
    for axis in axes:
        for token in normalized_words(axis.replace("_", " ")) - STOP:
            result[token] += 3
    result[post.rubric.lower()] += 2
    return result


def cosine(left: Counter[str], right: Counter[str]) -> float:
    shared = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / max(left_norm * right_norm, 1.0)


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def build() -> int:
    with connect() as database:
        database.executescript(
            """
            DROP TABLE IF EXISTS posts;
            DROP TABLE IF EXISTS posts_fts;
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY, date TEXT, rubric TEXT, title TEXT, path TEXT, body TEXT, tokens TEXT
            );
            CREATE VIRTUAL TABLE posts_fts USING fts5(post_id UNINDEXED, title, body, tokenize='unicode61');
            """
        )
        for post in iter_posts(prefixes={"AL", "SV", "SP"}):
            body = clean_body(post.text)
            tokens = json.dumps(weighted_tokens(post), ensure_ascii=False)
            row = (
                post.post_id, post.publication_date.isoformat(), post.rubric, post.title,
                str(post.path.relative_to(ROOT)), body, tokens,
            )
            database.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)", row)
            database.execute("INSERT INTO posts_fts VALUES (?, ?, ?)", (post.post_id, post.title, body))
    print(f"SEMANTIC MEMORY: {len(iter_posts(prefixes={'AL', 'SV', 'SP'}))} posts -> {DB}")
    return 0


def search(query: str, limit: int) -> int:
    if not DB.exists():
        build()
    safe_query = " OR ".join(sorted(normalized_words(query) - STOP))
    if not safe_query:
        print("ERROR: query has no searchable terms")
        return 1
    with connect() as database:
        rows = database.execute(
            """
            SELECT p.post_id, p.date, p.rubric, p.title, p.path, bm25(posts_fts) AS rank
            FROM posts_fts JOIN posts p USING(post_id)
            WHERE posts_fts MATCH ? ORDER BY rank LIMIT ?
            """,
            (safe_query, limit),
        ).fetchall()
    for post_id, day, rubric, title, path, rank in rows:
        print(f"- {day} [{rubric}] {title or post_id} | score={rank:.3f} | {path}")
    return 0


def audit(target: str | None, strict: bool, threshold: float, window: int) -> int:
    archive = iter_posts(prefixes={"AL", "SV", "SP"})
    selected = iter_posts(target, prefixes={"AL", "SV", "SP"}) if target else archive
    vectors = {post.path: weighted_tokens(post) for post in archive}
    warnings: list[str] = []
    for current in selected:
        current_vector = vectors[current.path]
        for previous in archive:
            if previous.publication_date >= current.publication_date:
                continue
            age = current.publication_date - previous.publication_date
            if age > timedelta(days=window):
                continue
            shared = set(current_vector) & set(vectors[previous.path])
            if len(shared) < 8:
                continue
            score = cosine(current_vector, vectors[previous.path])
            if score >= threshold:
                warnings.append(
                    f"semantic similarity {score:.2f} ({age.days}d): {previous.path.name} -> {current.path.name}"
                )
    for message in sorted(set(warnings)):
        print(f"WARN: {message}")
    print(f"SEMANTIC AUDIT: 0 errors, {len(set(warnings))} warnings")
    return 1 if strict and warnings else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    search_parser = sub.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("target", nargs="?")
    audit_parser.add_argument("--strict", action="store_true")
    audit_parser.add_argument("--threshold", type=float, default=0.72)
    audit_parser.add_argument("--window", type=int, default=180)
    args = parser.parse_args()
    if args.command == "build":
        return build()
    if args.command == "search":
        return search(args.query, args.limit)
    return audit(args.target, args.strict, args.threshold, args.window)


if __name__ == "__main__":
    raise SystemExit(main())
