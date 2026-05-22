#!/usr/bin/env python3
"""LLM-as-judge cross-check for ZusWaveBench.

Scores each model's answer 0..1 against the gold rubric using an ensemble of
NEUTRAL judges (no vendor shared with any contestant) to avoid self-preference.
Judges are blind to which model produced the answer. Deterministic rules
(scripts/evaluate.py) remain the primary score; this is a secondary signal.

Usage:
    set -a; . ./.env; set +a
    python3 scripts/judge_llm.py --output results/judge_scores.jsonl --resume
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "benchmark.jsonl"

# Contestant models -> their prediction files. Keys match build_site.py.
CONTESTANTS = {
    "opus47": "openrouter_opus_4_7_full.jsonl",
    "gpt55": "openrouter_gpt_5_5_full.jsonl",
    "gemma": "openrouter_gemma_4_26b_full.jsonl",
    "bielik": "bielik_11b_q4km_gpu_full.jsonl",
    "pllum": "pllum_12b_q4km_gpu_full.jsonl",
}

# Neutral judges: different vendors than every contestant
# (contestants: OpenAI, Anthropic, Google, SpeakLeash, PLLuM consortium).
DEFAULT_JUDGES = ["deepseek/deepseek-v3.2", "qwen/qwen3-max", "x-ai/grok-4.3"]

SYSTEM = (
    "Jestes surowym, bezstronnym egzaminatorem. Oceniasz, czy ODPOWIEDZ KANDYDATA "
    "na polska sprawe urzedowa (administracja, podatki, ZUS, e-government, rejestry) "
    "jest merytorycznie poprawna i bezpieczna wzgledem WZORCA. "
    "Nie wiesz, ktory model wygenerowal odpowiedz; oceniaj wylacznie tresc.\n"
    "Kryteria: (1) poprawna identyfikacja pisma/skutku/srodka/organu; "
    "(2) obecnosc kluczowych pojec wzorca; (3) brak niebezpiecznych lub blednych "
    "twierdzen (mocna kara); (4) nie nagradzaj samej formy ani rozwleklosci.\n"
    "Zwroc WYLACZNIE JSON: {\"score\": <liczba 0..1>, \"reason\": \"<krotko po polsku>\"}. "
    "1.0 = w pelni poprawna i bezpieczna; 0.5 = czesciowo; 0.0 = bledna lub mylaca."
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_prompt(item: dict[str, Any], candidate: str) -> str:
    exp = item["expected"]
    return (
        f"PRZYPADEK:\n{item['input']}\n\n"
        f"WZORZEC (gold):\n"
        f"- etykiety: {json.dumps(exp.get('labels', {}), ensure_ascii=False)}\n"
        f"- wymagane pojecia: {json.dumps(exp.get('required_concepts', []), ensure_ascii=False)}\n"
        f"- zakazane twierdzenia: {json.dumps(exp.get('forbidden_claims', []), ensure_ascii=False)}\n"
        f"- uzasadnienie wzorca: {exp.get('notes', '')}\n\n"
        f"ODPOWIEDZ KANDYDATA:\n{candidate}\n\n"
        "Oceń odpowiedz kandydata wedlug kryteriow i zwroc sam JSON."
    )


def call_judge(base_url: str, api_key: str, model: str, prompt: str, timeout: float) -> dict[str, Any]:
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_score(content: str) -> tuple[float | None, str]:
    raw = content.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        obj = json.loads(raw)
        score = float(obj.get("score"))
        return max(0.0, min(1.0, score)), str(obj.get("reason", ""))[:300]
    except Exception:
        m = re.search(r'"score"\s*:\s*([01](?:\.\d+)?)', raw)
        if m:
            return max(0.0, min(1.0, float(m.group(1)))), raw[:200]
        m = re.search(r"\b(0?\.\d+|1\.0|0|1)\b", raw)
        if m:
            return max(0.0, min(1.0, float(m.group(1)))), raw[:200]
    return None, raw[:200]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=ROOT / "results" / "judge_scores.jsonl")
    ap.add_argument("--judges", default=",".join(DEFAULT_JUDGES))
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--models", default=",".join(CONTESTANTS))
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--sleep", type=float, default=0.0)
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY required", file=sys.stderr)
        return 2

    judges = [j.strip() for j in args.judges.split(",") if j.strip()]
    model_keys = [m.strip() for m in args.models.split(",") if m.strip()]
    items = load_jsonl(DATA)
    if args.limit:
        items = items[: args.limit]

    done: set[tuple[str, str, str]] = set()
    if args.resume and args.output.exists():
        for r in load_jsonl(args.output):
            done.add((r["model"], r["id"], r["judge"]))

    preds = {
        key: {r["id"]: r for r in load_jsonl(ROOT / "results" / CONTESTANTS[key])}
        for key in model_keys
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.resume else "w"
    total = len(items) * len(model_keys) * len(judges)
    n = 0
    with args.output.open(mode, encoding="utf-8") as out:
        for item in items:
            for key in model_keys:
                candidate = str(preds[key].get(item["id"], {}).get("response", "")).strip()
                prompt = build_prompt(item, candidate)
                for judge in judges:
                    n += 1
                    if (key, item["id"], judge) in done:
                        continue
                    started = time.time()
                    try:
                        raw = call_judge(args.base_url, api_key, judge, prompt, args.timeout)
                        content = (raw.get("choices") or [{}])[0].get("message", {}).get("content", "")
                        score, reason = parse_score(content if isinstance(content, str) else json.dumps(content))
                        cost = float(raw.get("usage", {}).get("cost", 0.0) or 0.0)
                        err = None if score is not None else "unparseable"
                    except Exception as exc:  # noqa: BLE001
                        score, reason, cost, err = None, str(exc)[:200], 0.0, str(exc)[:200]
                    out.write(json.dumps({
                        "model": key, "id": item["id"], "judge": judge,
                        "score": score, "reason": reason, "cost": cost,
                        "latency_s": round(time.time() - started, 2),
                    }, ensure_ascii=False) + "\n")
                    out.flush()
                    print(f"[{n}/{total}] {key} {item['id']} {judge.split('/')[-1]} -> {score}", file=sys.stderr)
                    if args.sleep:
                        time.sleep(args.sleep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
