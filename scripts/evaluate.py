#!/usr/bin/env python3
"""Deterministic evaluator for ZusWaveBench predictions."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WEIGHTS = {
    "labels": 0.45,
    "required_concepts": 0.35,
    "forbidden_penalty": 0.15,
    "json_validity": 0.05,
}

# Keys the model is actually instructed to emit (see prompts/system.txt).
# Gold labels outside this set (e.g. requires_action, is_decision) cannot be
# scored fairly by free-text matching, so they are excluded from label scoring.
SCHEMA_KEYS = {
    "document_type",
    "legal_effect",
    "remedy",
    "organ",
    "answer",
    "next_steps",
    "risk_flags",
    "key_terms",
}

# Negation cues (normalized, diacritics stripped). Used to make concept and
# forbidden-claim matching polarity-aware: "REGON nie jest numerem podatkowym"
# must NOT count as asserting the forbidden claim "REGON to numer podatkowy".
NEGATIONS = {
    "nie", "ani", "bez", "nieprawda", "blednie", "falszywie", "wbrew",
    "not", "never", "nor", "without", "cannot", "isnt", "arent",  # models sometimes answer in English
}

# Short Polish function words to ignore when picking "content" tokens. Anything
# short that is NOT here (e.g. WZ, A1, PIT, ZUS, NIP, KW, UPO) is kept, because
# those codes are exactly the disambiguators the benchmark cares about.
SHORT_STOP = {
    "od", "to", "na", "sie", "czy", "lub", "ani", "do", "za", "po", "te", "ta",
    "ten", "tym", "tej", "tych", "jej", "ich", "nas", "was", "jak", "gdy", "bo",
    "co", "aby", "juz", "tez", "oraz", "albo", "nad", "pod", "przy", "bez", "dla",
    "nie", "ma", "sa", "by", "im", "mu", "go", "ja", "my", "wy", "on", "ona",
    "ono", "oni", "one", "w", "z", "i", "a", "o", "u", "ze", "we", "do",
}


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


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = str(value).lower()
    replacements = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ź": "z",
        "ż": "z",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_response(value: Any) -> tuple[Any, bool, str]:
    if isinstance(value, (dict, list)):
        return value, True, normalize(value)
    if value is None:
        return "", False, ""
    raw = str(value).strip()
    if not raw:
        return "", False, ""

    cleaned = raw
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        parsed = json.loads(cleaned)
        return parsed, True, normalize(parsed)
    except json.JSONDecodeError:
        return raw, False, normalize(raw)


def prediction_by_id(path: Path) -> dict[str, dict[str, Any]]:
    rows = load_jsonl(path)
    predictions: dict[str, dict[str, Any]] = {}
    for row in rows:
        if "id" not in row:
            continue
        predictions[str(row["id"])] = row
    return predictions


def value_matches(parsed: Any, text: str, key: str, expected: Any) -> bool:
    if expected is None:
        return True
    if isinstance(expected, bool):
        expected_words = ["true", "tak", "yes"] if expected else ["false", "nie", "no"]
        if isinstance(parsed, dict) and key in parsed:
            candidate = parsed[key]
            if isinstance(candidate, bool):
                return candidate is expected
            return normalize(candidate) in expected_words
        return any(word in text for word in expected_words)

    expected_text = normalize(expected)
    if isinstance(parsed, dict) and key in parsed:
        candidate = normalize(parsed[key])
        if expected_text and (expected_text in candidate or candidate in expected_text):
            return True
    return expected_text in text


def _tokens(value: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", value) if t]


def _tok_match(a: str, b: str) -> bool:
    """Loose token equality tolerant of Polish inflection (decyzja/decyzji)."""
    if a == b:
        return True
    if len(a) >= 5 and len(b) >= 5 and a[:5] == b[:5]:
        return True
    return False


def _negated(text_tokens: list[str], lo: int, hi: int) -> bool:
    """True if a negation cue sits inside or just before the [lo, hi] span.

    Polish negation can sit a few words ahead of the phrase
    ("nie przysluguje od niego odwolanie"), so we look back several tokens.
    """
    segment = text_tokens[max(0, lo - 5): hi + 1]
    return any(t in NEGATIONS for t in segment)


def _content_tokens(phrase_tokens: list[str]) -> list[str]:
    """Distinctive tokens: long words, plus short codes that aren't stopwords."""
    return [t for t in phrase_tokens if len(t) >= 4 or (len(t) >= 2 and t not in SHORT_STOP)]


def concept_present(text: str, concept: str, *, require_polarity: bool = True) -> bool:
    """Polarity-, proximity- and inflection-aware presence check.

    A phrase counts as present only when its content words appear close together.
    With require_polarity (default) the local polarity must also match: an
    affirmative phrase ("X to Y") is not credited inside a negation
    ("X nie jest Y"). Pass require_polarity=False to detect a mention regardless
    of polarity (used to find negated mentions of a forbidden claim).
    """
    nphrase = normalize(concept)
    if not nphrase:
        return False
    ptokens = _tokens(nphrase)
    phrase_neg = any(t in NEGATIONS for t in ptokens)
    content = _content_tokens(ptokens)
    ttokens = _tokens(text)

    def polarity_ok(lo: int, hi: int) -> bool:
        return not require_polarity or phrase_neg == _negated(ttokens, lo, hi)

    # No distinctive content words: fall back to exact substring + polarity.
    if not content:
        idx = text.find(nphrase)
        if idx < 0:
            return False
        pre = len(_tokens(text[:idx]))
        return polarity_ok(pre, pre + len(ptokens))

    # Map each content token to the text positions it (inflection-tolerantly) hits.
    hits = {t: [i for i, u in enumerate(ttokens) if _tok_match(t, u)] for t in content}
    if any(not pos for pos in hits.values()):
        return False

    if len(content) == 1:
        return any(polarity_ok(i, i) for i in hits[content[0]])

    # Multiple content tokens: require them within a tight window.
    limit = 4 * len(content) + 4
    rarest = min(content, key=lambda t: len(hits[t]))
    for anchor in hits[rarest]:
        lo = hi = anchor
        ok = True
        for t in content:
            near = [i for i in hits[t] if abs(i - anchor) <= limit]
            if not near:
                ok = False
                break
            lo, hi = min(lo, min(near)), max(hi, max(near))
        if ok and (hi - lo) <= limit and polarity_ok(lo, hi):
            return True
    return False


def assertive_prose(parsed: Any) -> str | None:
    """Concatenate the model's free-text claim fields (not its keyword lists).

    Forbidden claims are about what the model *asserts*, so we ignore enumerated
    fields like key_terms/risk_flags where merely listing a term is not a claim.
    """
    if not isinstance(parsed, dict):
        return None
    fields = [
        parsed.get(k) for k in ("document_type", "legal_effect", "remedy", "organ", "answer")
    ]
    prose = ". ".join(v for v in fields if isinstance(v, str) and v.strip())
    return normalize(prose) if prose else ""


def claim_asserted(parsed: Any, text: str, claim: str) -> bool:
    """True only if the model affirmatively asserts the forbidden claim.

    Checks the prose fields clause by clause so a clause-local negation
    ("MPZP nie jest decyzja WZ") prevents a false hit.
    """
    prose = assertive_prose(parsed)
    haystack = prose if prose is not None else text
    if not haystack:
        return False
    claim_neg = any(t in NEGATIONS for t in _tokens(normalize(claim)))

    aligned = opposite = False
    for clause in re.split(r"[.,;:!?]", haystack):
        if not clause.strip() or not concept_present(clause, claim, require_polarity=False):
            continue
        clause_neg = any(t in NEGATIONS for t in _tokens(clause))
        if clause_neg == claim_neg:
            aligned = True
        else:
            opposite = True
    # Asserted only if stated with the claim's polarity and never with the
    # opposite one: "X nie jest Y ... Y to ..." (correct distinction) is not a hit.
    return aligned and not opposite


def score_item(item: dict[str, Any], prediction: dict[str, Any] | None) -> dict[str, Any]:
    if not prediction:
        return {
            "id": item["id"],
            "score": 0.0,
            "weighted_score": 0.0,
            "json_valid": False,
            "label_score": 0.0,
            "required_score": 0.0,
            "forbidden_hits": [],
            "missing_labels": [k for k in item["expected"].get("labels", {}) if k in SCHEMA_KEYS],
            "missing_concepts": item["expected"].get("required_concepts", []),
        }

    parsed, json_valid, text = parse_response(prediction.get("response"))
    expected = item["expected"]
    # Only score label keys the model is actually asked to emit. Keys like
    # requires_action / is_decision are not in the output schema, so judging
    # them by free text is noise; their intent is covered by required_concepts.
    labels = {k: v for k, v in expected.get("labels", {}).items() if k in SCHEMA_KEYS}
    missing_labels = [
        key
        for key, expected_value in labels.items()
        if not value_matches(parsed, text, key, expected_value)
    ]
    label_score = 1.0 if not labels else (len(labels) - len(missing_labels)) / len(labels)

    required = expected.get("required_concepts", [])
    missing_concepts = [concept for concept in required if not concept_present(text, concept)]
    required_score = 1.0 if not required else (len(required) - len(missing_concepts)) / len(required)

    forbidden = expected.get("forbidden_claims", [])
    forbidden_hits = [claim for claim in forbidden if claim_asserted(parsed, text, claim)]
    forbidden_score = 1.0 - (len(forbidden_hits) / len(forbidden) if forbidden else 0.0)

    score = (
        DEFAULT_WEIGHTS["labels"] * label_score
        + DEFAULT_WEIGHTS["required_concepts"] * required_score
        + DEFAULT_WEIGHTS["forbidden_penalty"] * forbidden_score
        + DEFAULT_WEIGHTS["json_validity"] * (1.0 if json_valid else 0.0)
    )
    score = max(0.0, min(1.0, score))
    weight = float(item.get("weight", 1.0))
    return {
        "id": item["id"],
        "score": score,
        "weighted_score": score * weight,
        "weight": weight,
        "json_valid": json_valid,
        "label_score": label_score,
        "required_score": required_score,
        "forbidden_score": forbidden_score,
        "forbidden_hits": forbidden_hits,
        "missing_labels": missing_labels,
        "missing_concepts": missing_concepts,
    }


def weighted_average(rows: list[dict[str, Any]]) -> float:
    denom = sum(float(row.get("weight", 1.0)) for row in rows)
    if denom == 0:
        return 0.0
    return sum(float(row["weighted_score"]) for row in rows) / denom


def build_report(items: list[dict[str, Any]], scored: list[dict[str, Any]], predictions_path: Path) -> str:
    item_by_id = {item["id"]: item for item in items}
    aggregate = weighted_average(scored)
    json_rate = sum(1 for row in scored if row["json_valid"]) / len(scored) if scored else 0.0

    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        item = item_by_id[row["id"]]
        by_domain[item["domain"]].append(row)
        by_task[item["task_type"]].append(row)

    lines = [
        "# ZusWaveBench Report",
        "",
        f"- Predictions: `{predictions_path}`",
        f"- Items scored: {len(scored)}",
        f"- Weighted score: {aggregate:.3f}",
        f"- JSON-valid rate: {json_rate:.1%}",
        "",
        "## By Domain",
        "",
        "| Domain | Items | Weighted Score |",
        "|---|---:|---:|",
    ]
    for domain, rows in sorted(by_domain.items()):
        lines.append(f"| {domain} | {len(rows)} | {weighted_average(rows):.3f} |")

    lines.extend(["", "## By Task", "", "| Task | Items | Weighted Score |", "|---|---:|---:|"])
    for task, rows in sorted(by_task.items()):
        lines.append(f"| {task} | {len(rows)} | {weighted_average(rows):.3f} |")

    worst = sorted(scored, key=lambda row: row["score"])[:10]
    lines.extend(["", "## Weakest Items", "", "| ID | Domain | Task | Score | Main Missing |", "|---|---|---|---:|---|"])
    for row in worst:
        item = item_by_id[row["id"]]
        missing = row["missing_labels"][:2] + row["missing_concepts"][:2] + row["forbidden_hits"][:2]
        lines.append(
            f"| {row['id']} | {item['domain']} | {item['task_type']} | "
            f"{row['score']:.3f} | {', '.join(missing)[:160]} |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "benchmark.jsonl")
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--scores-jsonl", type=Path)
    args = parser.parse_args()

    items = load_jsonl(args.dataset)
    predictions = prediction_by_id(args.predictions)
    scored = [score_item(item, predictions.get(item["id"])) for item in items]

    report = build_report(items, scored, args.predictions)
    print(report)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")

    if args.scores_jsonl:
        args.scores_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with args.scores_jsonl.open("w", encoding="utf-8") as handle:
            for row in scored:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
