# FAERS Replication Test - Propranolol VigiAccess Spike

Snapshot date / تاريخ اللقطة: **2026-06-23**

OpenFDA `meta.last_updated` / آخر تحديث OpenFDA: **2026-04-28**

This is a reproducible, hypothesis-generating comparison of annual FAERS report counts for propranolol, atenolol, and metoprolol. It is intended as a cross-check for a visible 2025 VigiAccess propranolol spike.

هذا فحص قابل للإعادة يقارن أعداد بلاغات FAERS السنوية لـ propranolol و atenolol و metoprolol كاختبار مستقل لقفزة propranolol الظاهرة في VigiAccess سنة 2025.

## Source Evidence / أدلة المصدر

Supplied VigiAccess screenshots are stored in:

- `assets/vigiaccess/propranolol.jpeg`
- `assets/vigiaccess/atenolol.jpeg`
- `assets/vigiaccess/metoprolol.jpeg`

Manual screenshot observations are stored in `data/vigiaccess_screenshot_observations.csv`.

## Method / المنهجية

- API endpoint: `https://api.fda.gov/drug/event.json`
- Date field: `receivedate`, the date FDA received the report.
- Primary drug field: `patient.drug.openfda.generic_name`
- Sanity-check drug field: `patient.drug.medicinalproduct`
- For each drug, year, and field, the script issues one query and reads `meta.results.total`; it does not paginate.
- Total FAERS baseline uses the same annual `receivedate` ranges with no drug filter.

## Caveats / تنبيهات

- Counts are raw spontaneous-report counts, not incidence rates and not risk estimates.
- الأرقام هي أعداد بلاغات خام، وليست معدلات حدوث أو تقديرا للخطر.
- No exposed-patient denominator is available.
- لا يوجد مقام لعدد المرضى المعرضين.
- Recent FAERS years can keep changing because of reporting lag; 2025 is near-final but not frozen as of `meta.last_updated`.
- سنة 2025 قد تتغير لاحقا بسبب تأخر البلاغات.
- The `openfda` normalized fields are absent on unmatched reports; the gap versus `medicinalproduct` is a data-quality signal.

## FAERS Counts / أعداد FAERS

| drug | field | 2022 | 2023 | 2024 | 2025 |
| --- | --- | --- | --- | --- | --- |
| propranolol | openfda_generic_name | 5,486 | 5,819 | 6,680 | 5,858 |
| propranolol | medicinalproduct | 4,623 | 5,055 | 5,695 | 4,978 |
| atenolol | openfda_generic_name | 4,325 | 3,681 | 3,472 | 3,288 |
| atenolol | medicinalproduct | 4,228 | 3,593 | 3,284 | 3,181 |
| metoprolol | openfda_generic_name | 21,443 | 20,502 | 19,793 | 20,245 |
| metoprolol | medicinalproduct | 20,543 | 19,676 | 19,018 | 19,643 |

## Growth Summary / ملخص النمو

| drug | 2023 | 2024 | 2025 | 2024 YoY | 2025 YoY | 2025/2024 | 2025/2023 | 2025 excess vs total FAERS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| propranolol | 5,819 | 6,680 | 5,858 | +14.8% | -12.3% | 0.88x | 1.01x | -11.4% |
| atenolol | 3,681 | 3,472 | 3,288 | -5.7% | -5.3% | 0.95x | 0.89x | -4.4% |
| metoprolol | 20,502 | 19,793 | 20,245 | -3.5% | +2.3% | 1.02x | 0.99x | +3.2% |

## Total FAERS Baseline / خط أساس FAERS

| year | total reports | YoY |
| --- | --- | --- |
| 2022 | 1,523,664 | n/a |
| 2023 | 1,368,572 | -10.2% |
| 2024 | 1,319,103 | -3.6% |
| 2025 | 1,307,331 | -0.9% |

## 2025 Field Gap / فجوة الحقول في 2025

| drug | openfda_generic_name | medicinalproduct | medicinalproduct - generic |
| --- | --- | --- | --- |
| propranolol | 5,858 | 4,978 | -880 |
| atenolol | 3,288 | 3,181 | -107 |
| metoprolol | 20,245 | 19,643 | -602 |

## Neutral Interpretation / قراءة محايدة

English: In this FAERS snapshot, the VigiAccess propranolol 2025 spike does **not** clearly replicate in the independent US FAERS sample. Propranolol decreases in 2025 on the normalized FAERS field while total FAERS is roughly flat.

العربية: في لقطة FAERS هذه، لا تتكرر قفزة propranolol الظاهرة في VigiAccess بوضوح داخل العينة الأمريكية المستقلة. في الحقل الموحد داخل FAERS ينخفض propranolol في 2025 بينما إجمالي FAERS شبه مستقر.

This does not prove absence of a safety issue; it only says that this specific raw-count spike is not reproduced in this second spontaneous-reporting system.

## Exact API Query URLs / روابط الاستعلام

- ALL_FAERS | receivedate | 2022: `https://api.fda.gov/drug/event.json?search=receivedate:[20220101+TO+20221231]&limit=1`
- ALL_FAERS | receivedate | 2023: `https://api.fda.gov/drug/event.json?search=receivedate:[20230101+TO+20231231]&limit=1`
- ALL_FAERS | receivedate | 2024: `https://api.fda.gov/drug/event.json?search=receivedate:[20240101+TO+20241231]&limit=1`
- ALL_FAERS | receivedate | 2025: `https://api.fda.gov/drug/event.json?search=receivedate:[20250101+TO+20251231]&limit=1`
- propranolol | openfda_generic_name | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:propranolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- propranolol | openfda_generic_name | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:propranolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- propranolol | openfda_generic_name | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:propranolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- propranolol | openfda_generic_name | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:propranolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
- propranolol | medicinalproduct | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:propranolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- propranolol | medicinalproduct | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:propranolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- propranolol | medicinalproduct | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:propranolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- propranolol | medicinalproduct | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:propranolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
- atenolol | openfda_generic_name | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:atenolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- atenolol | openfda_generic_name | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:atenolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- atenolol | openfda_generic_name | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:atenolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- atenolol | openfda_generic_name | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:atenolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
- atenolol | medicinalproduct | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:atenolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- atenolol | medicinalproduct | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:atenolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- atenolol | medicinalproduct | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:atenolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- atenolol | medicinalproduct | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:atenolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
- metoprolol | openfda_generic_name | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:metoprolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- metoprolol | openfda_generic_name | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:metoprolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- metoprolol | openfda_generic_name | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:metoprolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- metoprolol | openfda_generic_name | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:metoprolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
- metoprolol | medicinalproduct | 2022: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:metoprolol+AND+receivedate:[20220101+TO+20221231]&limit=1`
- metoprolol | medicinalproduct | 2023: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:metoprolol+AND+receivedate:[20230101+TO+20231231]&limit=1`
- metoprolol | medicinalproduct | 2024: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:metoprolol+AND+receivedate:[20240101+TO+20241231]&limit=1`
- metoprolol | medicinalproduct | 2025: `https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:metoprolol+AND+receivedate:[20250101+TO+20251231]&limit=1`
