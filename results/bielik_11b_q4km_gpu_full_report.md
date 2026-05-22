# ZusWaveBench Report

- Predictions: `results/bielik_11b_q4km_gpu_full.jsonl`
- Items scored: 48
- Weighted score: 0.628
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.492 |
| administration | 8 | 0.559 |
| adversarial | 4 | 0.603 |
| civic | 4 | 0.642 |
| egovernment | 4 | 0.767 |
| procedure | 4 | 0.510 |
| property | 4 | 0.806 |
| registers | 3 | 0.791 |
| style | 3 | 0.389 |
| tax | 6 | 0.618 |
| zus | 5 | 0.762 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.605 |
| deadline_reasoning | 3 | 0.623 |
| document_classification | 5 | 0.623 |
| form_symbol_extraction | 1 | 0.483 |
| organ_competence | 6 | 0.666 |
| remedy_selection | 7 | 0.449 |
| style_transformation | 3 | 0.389 |
| term_disambiguation | 15 | 0.784 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-PROC-004 | procedure | term_disambiguation | 0.150 | answer, ostatecznosc decyzji, prawomocnosc, wyrok sadu |
| PL-ADMIN-005 | administration | remedy_selection | 0.200 | document_type, remedy, wniesc odwolanie, za posrednictwem organu ktory wydal decyzje |
| PL-ADMIN-008 | administration | remedy_selection | 0.200 | document_type, remedy, ponowne rozpatrzenie sprawy, nie klasyczne odwolanie |
| PL-ADV-002 | adversarial | remedy_selection | 0.200 | answer, document_type, rygor natychmiastowej wykonalnosci, wykonalna mimo nieostatecznosci |
| PL-STYLE-003 | style | style_transformation | 0.270 | document_type, requires_action, skladka zdrowotna, prosba o wyjasnienie salda |
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-PROC-001 | procedure | deadline_reasoning | 0.317 | answer, nie od daty wydania, sprawdzic reguly liczenia terminu |
| PL-TAX-005 | tax | abbreviation_expansion | 0.340 | answer, miesieczny, kwartalny |
| PL-TAX-006 | tax | remedy_selection | 0.425 | remedy, zlozyc wyjasnienie, dolaczyc potwierdzenie przelewu |
| PL-STYLE-002 | style | style_transformation | 0.425 | requires_action, interes prawny, interes faktyczny |
