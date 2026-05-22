# ZusWaveBench

ZusWaveBench is a benchmark for checking whether an LLM understands Polish administrative, tax, ZUS, civic, and e-government cases well enough to give practical next-step guidance.

It is not a vocabulary quiz. Each item is a short real-world style case where the model must identify the document or situation, legal/practical effect, remedy, competent institution, next action, and common traps.

## What It Tests

- Polish administrative procedure: decisions, postanowienia, wezwania, zaswiadczenia, ponaglenie, WSA.
- Tax-office cases: PIT symbols, mikrorachunek, advance-payment mismatches, korekta vs wyjasnienie.
- ZUS cases: PUE/eZUS, ZUS DRA/ZUA/ZZA/ZWUA, ulga na start, preferencyjne skladki, A1.
- E-government: Profil Zaufany, ePUAP, e-Doreczenia, UPO/UPP, ESP.
- Registers and identifiers: PESEL, NIP, REGON, KRS, CEIDG, BDO, CRBR.
- Local-government and property cases: meldunek, USC, WZ, MPZP, EGiB, KW.
- Deadline and remedy reasoning: what to file, where, and what not to assume.
- Style transformation: rewriting emotional citizen letters into usable official correspondence without hallucinating legal bases.

## Repository Layout

```text
data/benchmark.jsonl       benchmark items
data/schema.json           item schema
data/sources.json          official source anchors used by item families
docs/benchmark_design.md   design notes and scoring rationale
prompts/system.txt         model instruction used by the runner
scripts/run_openai_compat.py
scripts/evaluate.py
scripts/validate_dataset.py
results/.gitkeep
```

## Validate The Dataset

```bash
python3 scripts/validate_dataset.py
```

## Run A Model

The runner works with OpenAI-compatible chat-completions APIs.

```bash
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-4.1-mini"
# Optional for OpenRouter, vLLM, LM Studio, etc.
export OPENAI_BASE_URL="https://api.openai.com/v1"

python3 scripts/run_openai_compat.py \
  --dataset data/benchmark.jsonl \
  --output results/predictions.jsonl
```

For OpenRouter:

```bash
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export OPENAI_MODEL="openai/gpt-4.1-mini"
python3 scripts/run_openai_compat.py --output results/openrouter.jsonl
```

## Evaluate

```bash
python3 scripts/evaluate.py \
  --dataset data/benchmark.jsonl \
  --predictions results/predictions.jsonl \
  --report results/report.md
```

The evaluator prints aggregate scores and writes a per-domain/per-task report.

## Prediction Format

Each prediction line should contain at least:

```json
{"id": "PL-ADMIN-001", "response": {"document_type": "...", "legal_effect": "..."}}
```

`response` can also be a string. Structured JSON is rewarded because production use needs parsable answers.

## Score

Each item is scored from 0 to 1:

- `labels`: exact match on key fields such as `document_type`, `remedy`, `organ`, or `answer`.
- `required_concepts`: expected concepts must appear in the response.
- `forbidden_claims`: dangerous or misleading claims reduce the score.
- `json_validity`: response is valid JSON or already parsed as an object.

The aggregate score is a weighted mean. Harder items and high-risk domains carry more weight.

## Important Caveat

This benchmark checks local reasoning and terminology, not legal advice quality. It should be refreshed against current official sources before being used for compliance or production legal-risk decisions.
