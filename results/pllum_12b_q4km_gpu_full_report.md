# ZusWaveBench Report

- Predictions: `results/pllum_12b_q4km_gpu_full.jsonl`
- Items scored: 48
- Weighted score: 0.577
- JSON-valid rate: 83.3%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.511 |
| administration | 8 | 0.530 |
| adversarial | 4 | 0.453 |
| civic | 4 | 0.632 |
| egovernment | 4 | 0.648 |
| procedure | 4 | 0.722 |
| property | 4 | 0.586 |
| registers | 3 | 0.565 |
| style | 3 | 0.395 |
| tax | 6 | 0.550 |
| zus | 5 | 0.740 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.518 |
| deadline_reasoning | 3 | 0.705 |
| document_classification | 5 | 0.449 |
| form_symbol_extraction | 1 | 0.317 |
| organ_competence | 6 | 0.661 |
| remedy_selection | 7 | 0.519 |
| style_transformation | 3 | 0.395 |
| term_disambiguation | 15 | 0.682 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-ADMIN-004 | administration | document_classification | 0.200 | document_type, answer, dowod zlozenia albo doreczenia, nie rozstrzyga sprawy |
| PL-STYLE-002 | style | style_transformation | 0.200 | document_type, interes prawny, interes faktyczny |
| PL-STYLE-001 | style | style_transformation | 0.250 | document_type, uprzejmie prosze, potwierdzenie przelewu |
| PL-TAX-005 | tax | abbreviation_expansion | 0.270 | answer, VAT, miesieczny |
| PL-TAX-001 | tax | form_symbol_extraction | 0.317 | document_type, 2025, 20109,00 zl |
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-ADMIN-005 | administration | remedy_selection | 0.350 | document_type, organ, wniesc odwolanie, za posrednictwem organu ktory wydal decyzje |
| PL-EGOV-004 | egovernment | document_classification | 0.375 | document_type, remedy, sprawdzic albo sprostowac dane, nie klasyczne odwolanie |
| PL-ID-003 | registers | abbreviation_expansion | 0.375 | answer, AML, nie ewidencja JDG |
| PL-ADV-001 | adversarial | term_disambiguation | 0.375 | document_type, wszczecie postepowania, nie rozstrzyga meritum |
