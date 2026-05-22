# ZusWaveBench Report

- Predictions: `results/openrouter_gemma_4_26b_full.jsonl`
- Items scored: 48
- Weighted score: 0.746
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.492 |
| administration | 8 | 0.745 |
| adversarial | 4 | 0.807 |
| civic | 4 | 0.725 |
| egovernment | 4 | 0.751 |
| procedure | 4 | 0.671 |
| property | 4 | 0.792 |
| registers | 3 | 0.813 |
| style | 3 | 0.735 |
| tax | 6 | 0.771 |
| zus | 5 | 0.808 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.605 |
| deadline_reasoning | 3 | 0.623 |
| document_classification | 5 | 0.692 |
| form_symbol_extraction | 1 | 0.883 |
| organ_competence | 6 | 0.689 |
| remedy_selection | 7 | 0.768 |
| style_transformation | 3 | 0.735 |
| term_disambiguation | 15 | 0.856 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-PROC-001 | procedure | deadline_reasoning | 0.317 | answer, od dnia doreczenia, sprawdzic reguly liczenia terminu |
| PL-TAX-005 | tax | abbreviation_expansion | 0.340 | answer, miesieczny, kwartalny |
| PL-ABBR-003 | abbreviations | abbreviation_expansion | 0.375 | answer, wiazaca informacja stawkowa, rozne pojecia |
| PL-PROPERTY-003 | property | organ_competence | 0.462 | organ, WZ |
| PL-ADMIN-003 | administration | document_classification | 0.513 | remedy, zaswiadczenie potwierdza dane, nie klasyczne odwolanie |
| PL-ZUS-002 | zus | abbreviation_expansion | 0.550 | answer |
| PL-ABBR-001 | abbreviations | abbreviation_expansion | 0.550 | answer |
| PL-ABBR-002 | abbreviations | abbreviation_expansion | 0.550 | answer |
| PL-EGOV-004 | egovernment | document_classification | 0.600 | remedy, sprawdzic albo sprostowac dane, nie klasyczne odwolanie |
