# ZusWaveBench Report

- Predictions: `results/openrouter_gpt_5_5_full.jsonl`
- Items scored: 48
- Weighted score: 0.763
- JSON-valid rate: 100.0%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.521 |
| administration | 8 | 0.767 |
| adversarial | 4 | 0.807 |
| civic | 4 | 0.819 |
| egovernment | 4 | 0.738 |
| procedure | 4 | 0.831 |
| property | 4 | 0.852 |
| registers | 3 | 0.860 |
| style | 3 | 0.463 |
| tax | 6 | 0.687 |
| zus | 5 | 0.925 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.705 |
| deadline_reasoning | 3 | 0.805 |
| document_classification | 5 | 0.678 |
| form_symbol_extraction | 1 | 0.883 |
| organ_competence | 6 | 0.689 |
| remedy_selection | 7 | 0.746 |
| style_transformation | 3 | 0.463 |
| term_disambiguation | 15 | 0.896 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-STYLE-003 | style | style_transformation | 0.340 | document_type, prosba o wyjasnienie salda, okres rozliczeniowy |
| PL-STYLE-001 | style | style_transformation | 0.350 | document_type, data platnosci, symbol formularza |
| PL-EGOV-004 | egovernment | document_classification | 0.375 | document_type, remedy, sprawdzic albo sprostowac dane, nie klasyczne odwolanie |
| PL-CIVIC-003 | civic | organ_competence | 0.433 | organ, gmina |
| PL-TAX-004 | tax | organ_competence | 0.462 | organ, KAS |
| PL-ABBR-001 | abbreviations | abbreviation_expansion | 0.462 | answer, wojewodzki sad administracyjny |
| PL-TAX-005 | tax | abbreviation_expansion | 0.480 | answer, nie zwykly PDF faktury |
| PL-ADMIN-003 | administration | document_classification | 0.513 | remedy, zaswiadczenie potwierdza dane, nie klasyczne odwolanie |
| PL-TAX-006 | tax | remedy_selection | 0.513 | document_type, zlozyc wyjasnienie, wskazac wlasciwy okres i formularz |
| PL-PROPERTY-003 | property | organ_competence | 0.550 | organ |
