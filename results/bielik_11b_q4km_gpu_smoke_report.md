# ZusWaveBench Report

- Predictions: `results/bielik_11b_q4km_gpu_smoke.jsonl`
- Items scored: 48
- Weighted score: 0.065
- JSON-valid rate: 10.4%

## By Domain

| Domain | Items | Weighted Score |
|---|---:|---:|
| abbreviations | 3 | 0.000 |
| administration | 8 | 0.355 |
| adversarial | 4 | 0.000 |
| civic | 4 | 0.000 |
| egovernment | 4 | 0.000 |
| procedure | 4 | 0.000 |
| property | 4 | 0.000 |
| registers | 3 | 0.000 |
| style | 3 | 0.000 |
| tax | 6 | 0.000 |
| zus | 5 | 0.000 |

## By Task

| Task | Items | Weighted Score |
|---|---:|---:|
| abbreviation_expansion | 8 | 0.000 |
| deadline_reasoning | 3 | 0.000 |
| document_classification | 5 | 0.518 |
| form_symbol_extraction | 1 | 0.000 |
| organ_competence | 6 | 0.000 |
| remedy_selection | 7 | 0.036 |
| style_transformation | 3 | 0.000 |
| term_disambiguation | 15 | 0.000 |

## Weakest Items

| ID | Domain | Task | Score | Main Missing |
|---|---|---|---:|---|
| PL-ADMIN-006 | administration | remedy_selection | 0.000 | remedy, document_type, ponaglenie, bezczynnosc |
| PL-ADMIN-007 | administration | remedy_selection | 0.000 | document_type, remedy, nie na kazde postanowienie, zazalenie gdy przepis przewiduje |
| PL-ADMIN-008 | administration | remedy_selection | 0.000 | document_type, remedy, ponowne rozpatrzenie sprawy, nie klasyczne odwolanie |
| PL-TAX-001 | tax | form_symbol_extraction | 0.000 | document_type, tax_form, PIT-28, 2025 |
| PL-TAX-002 | tax | term_disambiguation | 0.000 | answer, od przychodu, nie od dochodu |
| PL-TAX-003 | tax | term_disambiguation | 0.000 | answer, nadplata, zwrot |
| PL-TAX-004 | tax | organ_competence | 0.000 | organ, urzad skarbowy, KAS |
| PL-TAX-005 | tax | abbreviation_expansion | 0.000 | answer, VAT, JPK |
| PL-TAX-006 | tax | remedy_selection | 0.000 | document_type, remedy, zlozyc wyjasnienie, dolaczyc potwierdzenie przelewu |
| PL-ZUS-001 | zus | term_disambiguation | 0.000 | answer, ulga na start, skladka zdrowotna |
