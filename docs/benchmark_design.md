# Benchmark Design

## Goal

The goal is to judge whether an LLM can handle Polish institutional pragmatics: what a document means, what action follows, what remedy applies, and which local term must not be confused with a superficially similar one.

The benchmark intentionally avoids simple "define X" questions. Most items are short cases that require deciding between similar paths:

- decision vs wezwanie,
- zaswiadczenie vs decyzja,
- odwolanie vs zazalenie vs ponaglenie,
- zameldowanie vs zamieszkanie,
- ePUAP vs e-Doreczenia,
- PESEL vs NIP vs REGON,
- ulga na start vs preferencyjny ZUS,
- WZ vs pozwolenie na budowe.

## Task Families

1. `document_classification`
   Classify the official document and its practical effect.

2. `remedy_selection`
   Pick the correct procedural next step or remedy.

3. `term_disambiguation`
   Separate pairs that models often merge.

4. `form_symbol_extraction`
   Extract Polish form symbols, periods, amounts, deadlines, and requested action.

5. `organ_competence`
   Identify the competent institution.

6. `abbreviation_expansion`
   Expand local abbreviations and state what they are not.

7. `deadline_reasoning`
   Interpret time limits and procedural consequences without overclaiming.

8. `style_transformation`
   Rewrite citizen text into usable official correspondence while avoiding invented law.

## Scoring Rationale

The benchmark uses hybrid deterministic scoring because the target is practical reliability, not prose beauty.

- Exact labels catch whether the model chose the right path.
- Required concepts catch whether it understood the core reason.
- Forbidden claims penalize advice that would mislead a citizen or company.
- JSON validity rewards production-readiness.

Default weights:

```json
{
  "labels": 0.45,
  "required_concepts": 0.35,
  "forbidden_penalty": 0.15,
  "json_validity": 0.05
}
```

Forbidden claims are deliberately strong. A fluent answer that says "file an appeal" to a non-decision, or "pay immediately" when the letter only asks for explanations, should lose heavily.

## Dataset Format

Each JSONL row has:

```json
{
  "id": "PL-ADMIN-001",
  "domain": "administration",
  "task_type": "document_classification",
  "difficulty": 2,
  "weight": 1.2,
  "input": "Case text...",
  "expected": {
    "labels": {"document_type": "wezwanie", "requires_action": true},
    "required_concepts": ["not a decision", "deadline"],
    "forbidden_claims": ["file an appeal"],
    "notes": "Short gold rationale."
  },
  "sources": ["kpa"]
}
```

The official-source anchors are in `data/sources.json`.

## How To Extend

Add new JSONL rows with stable IDs. Prefer adversarial near-misses:

- same surface wording, different legal effect,
- misleading document title,
- false friend between common and legal meaning,
- missing fact that should make the model hedge,
- local Polish form or register name.

Keep the answer schema stable so old model runs remain comparable.
