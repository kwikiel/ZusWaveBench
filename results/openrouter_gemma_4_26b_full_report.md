# ZusWaveBench Report

- Predictions: `results/openrouter_gemma_4_26b_full.jsonl`
- Items scored: 48
- Weighted score: 0.711
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.462 |
| administration | 8 | 0.730 |
| adversarial | 4 | 0.794 |
| civic | 4 | 0.716 |
| egovernment | 4 | 0.787 |
| procedure | 4 | 0.617 |
| property | 4 | 0.787 |
| registers | 3 | 0.797 |
| style | 3 | 0.471 |
| tax | 6 | 0.765 |
| zus | 5 | 0.731 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.583 |
| deadline_reasoning | 3 | 0.606 |
| document_classification | 5 | 0.659 |
| form_symbol_extraction | 1 | 0.771 |
| organ_competence | 6 | 0.718 |
| remedy_selection | 7 | 0.787 |
| style_transformation | 3 | 0.471 |
| term_disambiguation | 15 | 0.815 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-PROC-001 | procedure | deadline_reasoning | 0.267 | answer, od dnia doreczenia, sprawdzic reguly liczenia terminu, od daty wydania |
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-TAX-005 | tax | abbreviation_expansion | 0.340 | answer, miesieczny, kwartalny |
| PL-ABBR-003 | abbreviations | abbreviation_expansion | 0.375 | answer, wiazaca informacja stawkowa, rozne pojecia |
| PL-STYLE-001 | style | style_transformation | 0.425 | requires_action, uprzejmie prosze, wyjasnienie sprawy |
| PL-PROPERTY-003 | property | organ_competence | 0.462 | organ, WZ |
| PL-ABBR-001 | abbreviations | abbreviation_expansion | 0.462 | answer, administracja |
| PL-STYLE-002 | style | style_transformation | 0.495 | requires_action, interes faktyczny, wniosek o informacje albo dopuszczenie do udzialu |
| PL-STYLE-003 | style | style_transformation | 0.495 | requires_action, skladka zdrowotna, prosba o wyjasnienie salda |
| PL-ZUS-002 | zus | abbreviation_expansion | 0.550 | answer |
