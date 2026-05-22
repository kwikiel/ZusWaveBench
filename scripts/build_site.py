#!/usr/bin/env python3
"""Compile ZusWaveBench results into a single self-contained index.html.

Reads the benchmark dataset, the full prediction files and the full score
files, recomputes the same weighted aggregates that scripts/evaluate.py
produces, and injects everything as JSON into scripts/site_template.html.

Usage:
    python3 scripts/build_site.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "benchmark.jsonl"
RESULTS = ROOT / "results"
TEMPLATE = ROOT / "scripts" / "site_template.html"
OUTPUT = ROOT / "index.html"

WEIGHTS = {
    "labels": 0.45,
    "required_concepts": 0.35,
    "forbidden_penalty": 0.15,
    "json_validity": 0.05,
}

# Display order and metadata for each model. `predictions` and `scores`
# point at the full-benchmark files in results/.
MODELS = [
    {
        "key": "gemma",
        "name": "Gemma 4 26B A4B IT",
        "short": "Gemma 4 26B",
        "runtime": "OpenRouter API",
        "quant": "cloud bf16",
        "predictions": "openrouter_gemma_4_26b_full.jsonl",
        "scores": "openrouter_gemma_4_26b_full_scores.jsonl",
    },
    {
        "key": "bielik",
        "name": "Bielik 11B v3 Q4_K_M",
        "short": "Bielik 11B v3",
        "runtime": "local GPU (llama.cpp)",
        "quant": "Q4_K_M",
        "predictions": "bielik_11b_q4km_gpu_full.jsonl",
        "scores": "bielik_11b_q4km_gpu_full_scores.jsonl",
    },
    {
        "key": "pllum",
        "name": "PLLuM 12B Q4_K_M",
        "short": "PLLuM 12B",
        "runtime": "local GPU (llama.cpp)",
        "quant": "Q4_K_M",
        "predictions": "pllum_12b_q4km_gpu_full.jsonl",
        "scores": "pllum_12b_q4km_gpu_full_scores.jsonl",
    },
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_response(value: Any) -> tuple[Any, bool]:
    """Return (parsed_object_or_raw_string, is_json)."""
    if isinstance(value, (dict, list)):
        return value, True
    if value is None:
        return "", False
    raw = str(value).strip()
    cleaned = raw
    if cleaned.startswith("```"):
        cleaned = cleaned.lstrip("`")
        if cleaned[:4].lower() == "json":
            cleaned = cleaned[4:]
        cleaned = cleaned.strip().rstrip("`").strip()
    try:
        return json.loads(cleaned), True
    except json.JSONDecodeError:
        return raw, False


def weighted_average(rows: list[dict[str, Any]]) -> float:
    denom = sum(float(r.get("weight", 1.0)) for r in rows)
    if denom == 0:
        return 0.0
    return sum(float(r["weighted_score"]) for r in rows) / denom


def main() -> int:
    items = load_jsonl(DATA)
    item_by_id = {it["id"]: it for it in items}

    domains = sorted({it["domain"] for it in items})
    tasks = sorted({it["task_type"] for it in items})

    models_out: list[dict[str, Any]] = []
    domain_scores: dict[str, dict[str, float]] = {}
    task_scores: dict[str, dict[str, float]] = {}
    # item id -> model key -> per-item result
    item_models: dict[str, dict[str, Any]] = defaultdict(dict)

    for model in MODELS:
        scores = {r["id"]: r for r in load_jsonl(RESULTS / model["scores"])}
        preds = {r["id"]: r for r in load_jsonl(RESULTS / model["predictions"])}
        scored_rows = [scores[it["id"]] for it in items if it["id"] in scores]

        overall = weighted_average(scored_rows)
        json_valid = sum(1 for r in scored_rows if r.get("json_valid"))

        # runtime stats from the prediction file
        latencies = [float(p["latency_s"]) for p in preds.values() if "latency_s" in p]
        total_tokens = sum(
            int(p.get("usage", {}).get("total_tokens", 0)) for p in preds.values()
        )
        costs = [
            float(p.get("usage", {}).get("cost", 0.0) or 0.0) for p in preds.values()
        ]
        total_cost = sum(costs)
        is_cloud = "API" in model["runtime"]

        by_domain: dict[str, list] = defaultdict(list)
        by_task: dict[str, list] = defaultdict(list)
        for r in scored_rows:
            it = item_by_id[r["id"]]
            by_domain[it["domain"]].append(r)
            by_task[it["task_type"]].append(r)

        domain_scores[model["key"]] = {
            d: round(weighted_average(by_domain[d]), 4) for d in domains
        }
        task_scores[model["key"]] = {
            t: round(weighted_average(by_task[t]), 4) for t in tasks
        }

        # per-item, with parsed model response for the drill-down
        for it in items:
            sr = scores.get(it["id"], {})
            pr = preds.get(it["id"], {})
            parsed, is_json = parse_response(pr.get("response"))
            item_models[it["id"]][model["key"]] = {
                "score": round(float(sr.get("score", 0.0)), 3),
                "json_valid": bool(sr.get("json_valid", False)),
                "missing_labels": sr.get("missing_labels", []),
                "missing_concepts": sr.get("missing_concepts", []),
                "forbidden_hits": sr.get("forbidden_hits", []),
                "response": parsed,
                "response_is_json": is_json,
            }

        models_out.append(
            {
                "key": model["key"],
                "name": model["name"],
                "short": model["short"],
                "runtime": model["runtime"],
                "quant": model["quant"],
                "score": round(overall, 3),
                "json_valid": json_valid,
                "json_total": len(scored_rows),
                "latency": round(sum(latencies) / len(latencies), 2) if latencies else None,
                "tokens": total_tokens,
                "cost": "local" if not is_cloud else f"${total_cost:.4f}",
                "errors": 0,
            }
        )

    models_out.sort(key=lambda m: m["score"], reverse=True)

    items_out = []
    for it in items:
        exp = it["expected"]
        items_out.append(
            {
                "id": it["id"],
                "domain": it["domain"],
                "task": it["task_type"],
                "difficulty": it["difficulty"],
                "weight": it["weight"],
                "input": it["input"],
                "expected": {
                    "labels": exp.get("labels", {}),
                    "required_concepts": exp.get("required_concepts", []),
                    "forbidden_claims": exp.get("forbidden_claims", []),
                    "notes": exp.get("notes", ""),
                },
                "sources": it.get("sources", []),
                "models": item_models[it["id"]],
            }
        )

    data = {
        "meta": {
            "items": len(items),
            "models": len(MODELS),
            "domains": len(domains),
            "tasks": len(tasks),
            "generated": "2026-05-22",
        },
        "weights": WEIGHTS,
        "models": models_out,
        "domains": domains,
        "tasks": tasks,
        "domainScores": domain_scores,
        "taskScores": task_scores,
        "items": items_out,
    }

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Keep the JSON safe inside a <script> block (only escape the angle bracket).
    payload = payload.replace("<", "\\u003c")

    template = TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("__ZWB_DATA__", payload)
    OUTPUT.write_text(html, encoding="utf-8")

    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(html):,} bytes)")
    print("Overall weighted scores:")
    for m in models_out:
        print(
            f"  {m['short']:<16} {m['score']:.3f}  "
            f"json {m['json_valid']}/{m['json_total']}  "
            f"lat {m['latency']}s  cost {m['cost']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
