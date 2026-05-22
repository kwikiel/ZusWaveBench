# ZusWaveBench Report

- Predictions: `results/pllum_12b_q4km_gpu_full.jsonl`
- Items scored: 48
- Weighted score: 0.581
- JSON-valid rate: 83.3%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.482 |
| administration | 8 | 0.543 |
| adversarial | 4 | 0.562 |
| civic | 4 | 0.611 |
| egovernment | 4 | 0.662 |
| procedure | 4 | 0.670 |
| property | 4 | 0.584 |
| registers | 3 | 0.572 |
| style | 3 | 0.305 |
| tax | 6 | 0.573 |
| zus | 5 | 0.740 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.508 |
| deadline_reasoning | 3 | 0.708 |
| document_classification | 5 | 0.456 |
| form_symbol_extraction | 1 | 0.429 |
| organ_competence | 6 | 0.638 |
| remedy_selection | 7 | 0.570 |
| style_transformation | 3 | 0.305 |
| term_disambiguation | 15 | 0.686 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-ADMIN-004 | administration | document_classification | 0.200 | document_type, is_decision, dowod zlozenia albo doreczenia, nie rozstrzyga sprawy |
| PL-STYLE-002 | style | style_transformation | 0.200 | document_type, requires_action, interes prawny, interes faktyczny |
| PL-STYLE-001 | style | style_transformation | 0.212 | document_type, requires_action, uprzejmie prosze, potwierdzenie przelewu, media |
| PL-TAX-005 | tax | abbreviation_expansion | 0.270 | answer, VAT, miesieczny |
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-ID-003 | registers | abbreviation_expansion | 0.375 | answer, AML, nie ewidencja JDG |
| PL-CIVIC-004 | civic | organ_competence | 0.375 | organ, answer, wojewoda, nie PUP |
| PL-ADV-001 | adversarial | term_disambiguation | 0.375 | document_type, wszczecie postepowania, nie rozstrzyga meritum |
| PL-PROPERTY-003 | property | organ_competence | 0.412 | organ, WZ, ZUS |
| PL-ADMIN-001 | administration | document_classification | 0.425 | document_type, requires_action, nie jest decyzja, uzupelnic braki |
