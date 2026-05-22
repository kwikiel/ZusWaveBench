#!/usr/bin/env python3
"""Run ZusWaveBench against an OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYSTEM_PROMPT = ROOT / "prompts" / "system.txt"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
    return rows


def request_chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    timeout: float,
    json_mode: bool,
    max_tokens: int | None,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {exc}") from exc


def build_user_prompt(item: dict[str, Any]) -> str:
    return (
        "Rozwiaz ponizszy przypadek benchmarkowy.\n\n"
        f"ID: {item['id']}\n"
        f"Domena: {item['domain']}\n"
        f"Typ zadania: {item['task_type']}\n"
        f"Przypadek: {item['input']}\n"
    )


def extract_content(raw: dict[str, Any]) -> str:
    choices = raw.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "benchmark.jsonl")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--system-prompt", type=Path, default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--json-mode", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is required", file=sys.stderr)
        return 2

    items = load_jsonl(args.dataset)
    if args.limit is not None:
        items = items[: args.limit]

    done_ids: set[str] = set()
    if args.resume and args.output.exists():
        for row in load_jsonl(args.output):
            if "id" in row:
                done_ids.add(str(row["id"]))

    system_prompt = args.system_prompt.read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    mode = "a" if args.resume else "w"
    with args.output.open(mode, encoding="utf-8") as out:
        for index, item in enumerate(items, 1):
            if item["id"] in done_ids:
                continue
            user_prompt = build_user_prompt(item)
            started = time.time()
            try:
                raw = request_chat_completion(
                    base_url=args.base_url,
                    api_key=api_key,
                    model=args.model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=args.temperature,
                    timeout=args.timeout,
                    json_mode=args.json_mode,
                    max_tokens=args.max_tokens,
                )
                response = extract_content(raw)
                usage = raw.get("usage", {})
                error = None
            except Exception as exc:  # noqa: BLE001 - preserve benchmark progress.
                response = ""
                usage = {}
                error = str(exc)

            row = {
                "id": item["id"],
                "model": args.model,
                "response": response,
                "usage": usage,
                "latency_s": round(time.time() - started, 3),
            }
            if error:
                row["error"] = error
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()

            status = "ERR" if error else "OK"
            print(f"[{status}] {index}/{len(items)} {item['id']}", file=sys.stderr)
            if args.sleep:
                time.sleep(args.sleep)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
