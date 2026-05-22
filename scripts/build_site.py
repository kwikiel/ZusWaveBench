#!/usr/bin/env python3
"""Compile ZusWaveBench results into a single self-contained index.html.

Reads the benchmark dataset, the full prediction files and the full score
files, recomputes the same weighted aggregates that scripts/evaluate.py
produces, and injects everything as JSON into scripts/site_template.html.

Usage:
    python3 scripts/build_site.py
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "benchmark.jsonl"
RESULTS = ROOT / "results"
TEMPLATE = ROOT / "scripts" / "site_template.html"
OUTPUT = ROOT / "index.html"

# SEO consolidates on codesota; the GitHub Pages copy points its canonical here too.
CANONICAL = "https://www.codesota.com/zuswavebench"
VERCEL_ANALYTICS = '<script defer src="/_vercel/insights/script.js"></script>'

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
        "key": "opus47",
        "name": "Claude Opus 4.7",
        "short": "Opus 4.7",
        "runtime": "OpenRouter API",
        "quant": "frontier",
        "predictions": "openrouter_opus_4_7_full.jsonl",
        "scores": "openrouter_opus_4_7_full_scores.jsonl",
    },
    {
        "key": "gpt55",
        "name": "GPT-5.5",
        "short": "GPT-5.5",
        "runtime": "OpenRouter API",
        "quant": "frontier",
        "predictions": "openrouter_gpt_5_5_full.jsonl",
        "scores": "openrouter_gpt_5_5_full_scores.jsonl",
    },
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


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs) ** 0.5
    vy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (vx * vy) if vx and vy else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=OUTPUT)
    ap.add_argument("--canonical", default=CANONICAL)
    ap.add_argument("--analytics", choices=["none", "vercel"], default="none")
    ap.add_argument("--write-comparison", action="store_true", default=False,
                    help="also (re)write results/model_comparison_full.md")
    args = ap.parse_args()

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
        if not (RESULTS / model["scores"]).exists() or not (RESULTS / model["predictions"]).exists():
            print(f"  skip {model['short']}: result files not found yet")
            continue
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

    # ---- LLM-judge ensemble (secondary, neutral cross-check) ----
    judge_path = RESULTS / "judge_scores.jsonl"
    judges: list[str] = []
    judge_meta: dict[str, Any] = {}
    has_judge = judge_path.exists()
    if has_judge:
        jrows = load_jsonl(judge_path)
        judges = sorted({r["judge"] for r in jrows})
        jscore: dict[tuple, dict] = defaultdict(dict)
        jreason: dict[tuple, dict] = defaultdict(dict)
        for r in jrows:
            if r.get("score") is not None:
                jscore[(r["model"], r["id"])][r["judge"]] = float(r["score"])
            if r.get("reason"):
                jreason[(r["model"], r["id"])][r["judge"]] = r["reason"]

        def ensemble(mkey, iid):
            vals = list(jscore.get((mkey, iid), {}).values())
            return sum(vals) / len(vals) if vals else None

        for it in items:
            for m in MODELS:
                k = m["key"]
                if k not in item_models[it["id"]]:
                    continue
                ens = ensemble(k, it["id"])
                item_models[it["id"]][k]["judge"] = {
                    "ensemble": round(ens, 3) if ens is not None else None,
                    "scores": {j: round(s, 2) for j, s in jscore.get((k, it["id"]), {}).items()},
                    "reasons": jreason.get((k, it["id"]), {}),
                }

        all_rules: list[float] = []
        all_judge: list[float] = []
        for m in models_out:
            k = m["key"]
            num = den = 0.0
            rules_pts: list[float] = []
            judge_pts: list[float] = []
            for it in items:
                ens = ensemble(k, it["id"])
                if ens is None or k not in item_models[it["id"]]:
                    continue
                w = float(it["weight"])
                num += ens * w
                den += w
                rules_pts.append(item_models[it["id"]][k]["score"])
                judge_pts.append(ens)
            all_rules += rules_pts
            all_judge += judge_pts
            m["judge"] = round(num / den, 3) if den else None
            m["judge_corr"] = round(pearson(rules_pts, judge_pts), 3) if len(rules_pts) > 2 else None
            m["judge_mad"] = (
                round(sum(abs(a - b) for a, b in zip(rules_pts, judge_pts)) / len(rules_pts), 3)
                if rules_pts else None
            )
            m["judge_delta"] = round(m["judge"] - m["score"], 3) if m["judge"] is not None else None

        # global rules-vs-judge agreement (across all model x item points)
        if all_rules:
            rules_order = [x["key"] for x in sorted(models_out, key=lambda z: -z["score"])]
            judge_order = [x["key"] for x in sorted(models_out, key=lambda z: -(z["judge"] or 0))]
            judge_meta = {
                "globalCorr": round(pearson(all_rules, all_judge), 3),
                "meanDelta": round(sum(j - r for r, j in zip(all_rules, all_judge)) / len(all_rules), 3),
                "mad": round(sum(abs(j - r) for r, j in zip(all_rules, all_judge)) / len(all_rules), 3),
                "n": len(all_rules),
                "sameRanking": rules_order == judge_order,
            }
        else:
            judge_meta = {}

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
        "hasJudge": has_judge,
        "judges": judges,
        "judgeMeta": judge_meta,
    }

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Keep the JSON safe inside a <script> block (only escape the angle bracket).
    payload = payload.replace("<", "\\u003c")

    template = TEMPLATE.read_text(encoding="utf-8")
    html = (
        template
        .replace("__ZWB_DATA__", payload)
        .replace("__CANONICAL__", args.canonical)
        .replace("__ANALYTICS__", VERCEL_ANALYTICS if args.analytics == "vercel" else "")
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")

    # Keep the markdown comparison table in sync with the site (default build only).
    if args.write_comparison or args.output == OUTPUT:
        comp = [
            "# Model Comparison Full Benchmark",
            "",
            "| Model | Items | Weighted score | JSON valid | Avg latency | Total tokens | Cost | Errors |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for m in models_out:
            lat = f"{m['latency']:.2f}s" if m["latency"] is not None else "—"
            comp.append(
                f"| {m['name']} | {m['json_total']} | {m['score']:.3f} | "
                f"{m['json_valid']}/{m['json_total']} | {lat} | {m['tokens']} | {m['cost']} | {m['errors']} |"
            )
        (RESULTS / "model_comparison_full.md").write_text("\n".join(comp) + "\n", encoding="utf-8")

    print(f"Wrote {args.output} ({len(html):,} bytes) canonical={args.canonical} analytics={args.analytics}")
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
