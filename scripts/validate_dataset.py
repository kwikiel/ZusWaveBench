#!/usr/bin/env python3
"""Validate ZusWaveBench dataset invariants without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TASK_TYPES = {
    "document_classification",
    "remedy_selection",
    "term_disambiguation",
    "form_symbol_extraction",
    "organ_competence",
    "abbreviation_expansion",
    "deadline_reasoning",
    "style_transformation",
}
ID_PATTERN = re.compile(r"^PL-[A-Z]+-[0-9]{3}$")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            row["_line_no"] = line_no
            rows.append(row)
    return rows


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_item(row: dict[str, Any], source_ids: set[str], errors: list[str]) -> None:
    line = row.get("_line_no", "?")
    prefix = f"line {line}"
    required = ["id", "domain", "task_type", "difficulty", "weight", "input", "expected"]
    for key in required:
        require(key in row, f"{prefix}: missing {key}", errors)
    if any(key not in row for key in required):
        return

    require(isinstance(row["id"], str) and bool(ID_PATTERN.match(row["id"])), f"{prefix}: bad id", errors)
    require(row["task_type"] in ALLOWED_TASK_TYPES, f"{prefix}: bad task_type {row['task_type']}", errors)
    require(isinstance(row["difficulty"], int) and 1 <= row["difficulty"] <= 5, f"{prefix}: bad difficulty", errors)
    require(isinstance(row["weight"], (int, float)) and row["weight"] > 0, f"{prefix}: bad weight", errors)
    require(isinstance(row["input"], str) and len(row["input"]) >= 10, f"{prefix}: input too short", errors)

    expected = row["expected"]
    require(isinstance(expected, dict), f"{prefix}: expected must be object", errors)
    if not isinstance(expected, dict):
        return
    for key in ["labels", "required_concepts", "forbidden_claims", "notes"]:
        require(key in expected, f"{prefix}: expected missing {key}", errors)
    require(isinstance(expected.get("labels"), dict), f"{prefix}: labels must be object", errors)
    require(isinstance(expected.get("required_concepts"), list), f"{prefix}: required_concepts must be array", errors)
    require(isinstance(expected.get("forbidden_claims"), list), f"{prefix}: forbidden_claims must be array", errors)
    require(bool(expected.get("required_concepts")), f"{prefix}: required_concepts should not be empty", errors)

    for source_id in row.get("sources", []):
        require(source_id in source_ids, f"{prefix}: unknown source {source_id}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "benchmark.jsonl")
    parser.add_argument("--sources", type=Path, default=ROOT / "data" / "sources.json")
    args = parser.parse_args()

    sources = json.loads(args.sources.read_text(encoding="utf-8"))
    source_ids = set(sources.keys())
    rows = load_jsonl(args.dataset)
    errors: list[str] = []

    ids = [row.get("id") for row in rows]
    for item_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate id: {item_id}")

    for row in rows:
        validate_item(row, source_ids, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    by_task = Counter(row["task_type"] for row in rows)
    by_domain = Counter(row["domain"] for row in rows)
    print(f"OK: {len(rows)} items, {len(by_domain)} domains, {len(by_task)} task types")
    for task, count in sorted(by_task.items()):
        print(f"- {task}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
