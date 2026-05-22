# ZusWaveBench Report

- Predictions: `results/bielik_11b_q4km_gpu_full.jsonl`
- Items scored: 48
- Weighted score: 0.666
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.521 |
| administration | 8 | 0.567 |
| adversarial | 4 | 0.617 |
| civic | 4 | 0.713 |
| egovernment | 4 | 0.751 |
| procedure | 4 | 0.490 |
| property | 4 | 0.766 |
| registers | 3 | 0.831 |
| style | 3 | 0.537 |
| tax | 6 | 0.729 |
| zus | 5 | 0.839 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.645 |
| deadline_reasoning | 3 | 0.553 |
| document_classification | 5 | 0.640 |
| form_symbol_extraction | 1 | 0.767 |
| organ_competence | 6 | 0.681 |
| remedy_selection | 7 | 0.477 |
| style_transformation | 3 | 0.537 |
| term_disambiguation | 15 | 0.818 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-ADMIN-005 | administration | remedy_selection | 0.200 | document_type, remedy, wniesc odwolanie, za posrednictwem organu ktory wydal decyzje |
| PL-ADMIN-008 | administration | remedy_selection | 0.200 | document_type, remedy, ponowne rozpatrzenie sprawy, nie klasyczne odwolanie |
| PL-PROC-001 | procedure | deadline_reasoning | 0.200 | answer, od dnia doreczenia, nie od daty wydania |
| PL-ADV-002 | adversarial | remedy_selection | 0.200 | answer, document_type, rygor natychmiastowej wykonalnosci, wykonalna mimo nieostatecznosci |
| PL-STYLE-003 | style | style_transformation | 0.270 | document_type, skladka zdrowotna, prosba o wyjasnienie salda |
| PL-PROC-004 | procedure | term_disambiguation | 0.287 | answer, ostatecznosc decyzji, nie to samo |
| PL-CIVIC-003 | civic | organ_competence | 0.317 | organ, gmina, urzad gminy |
| PL-PROPERTY-003 | property | organ_competence | 0.462 | organ, WZ |
| PL-ABBR-003 | abbreviations | abbreviation_expansion | 0.462 | answer, rozne pojecia |
| PL-TAX-005 | tax | abbreviation_expansion | 0.480 | answer, nie zwykly PDF faktury |
