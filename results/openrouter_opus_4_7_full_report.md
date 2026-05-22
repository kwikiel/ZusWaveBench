# ZusWaveBench Report

- Predictions: `results/openrouter_opus_4_7_full.jsonl`
- Items scored: 48
- Weighted score: 0.750
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.521 |
| administration | 8 | 0.809 |
| adversarial | 4 | 0.807 |
| civic | 4 | 0.787 |
| egovernment | 4 | 0.792 |
| procedure | 4 | 0.713 |
| property | 4 | 0.800 |
| registers | 3 | 0.866 |
| style | 3 | 0.424 |
| tax | 6 | 0.704 |
| zus | 5 | 0.851 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.684 |
| deadline_reasoning | 3 | 0.693 |
| document_classification | 5 | 0.715 |
| form_symbol_extraction | 1 | 0.825 |
| organ_competence | 6 | 0.681 |
| remedy_selection | 7 | 0.790 |
| style_transformation | 3 | 0.424 |
| term_disambiguation | 15 | 0.870 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-STYLE-002 | style | style_transformation | 0.270 | document_type, interes faktyczny, wniosek o informacje albo dopuszczenie do udzialu |
| PL-STYLE-003 | style | style_transformation | 0.340 | document_type, prosba o wyjasnienie salda, okres rozliczeniowy |
| PL-CIVIC-003 | civic | organ_competence | 0.433 | organ, gmina |
| PL-PROC-001 | procedure | deadline_reasoning | 0.433 | answer, sprawdzic reguly liczenia terminu |
| PL-EGOV-004 | egovernment | document_classification | 0.462 | document_type, remedy, sprawdzic albo sprostowac dane |
| PL-ABBR-003 | abbreviations | abbreviation_expansion | 0.462 | answer, rozne pojecia |
| PL-TAX-005 | tax | abbreviation_expansion | 0.480 | answer, nie zwykly PDF faktury |
| PL-ADMIN-003 | administration | document_classification | 0.513 | remedy, zaswiadczenie potwierdza dane, nie klasyczne odwolanie |
| PL-TAX-004 | tax | organ_competence | 0.550 | organ |
| PL-ZUS-002 | zus | abbreviation_expansion | 0.550 | answer |
