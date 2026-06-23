# FAERS Replication Test - Propranolol VigiAccess Spike

This repository is a small, reproducible OpenFDA/FAERS cross-check for a visible 2025 spike in VigiAccess adverse-event reports for **propranolol**, compared with **atenolol** and **metoprolol**.

It is a descriptive, hypothesis-generating raw-count comparison only. It does **not** estimate incidence, patient-level risk, or causality.

## Headline Result

Using snapshot date **2026-06-23** and OpenFDA `meta.last_updated = 2026-04-28`:

```text
Total FAERS: 2025 YoY -0.9%
propranolol: 2025 YoY -12.3% vs total FAERS -0.9%; excess -11.4%
atenolol: 2025 YoY -5.3% vs total FAERS -0.9%; excess -4.4%
metoprolol: 2025 YoY +2.3% vs total FAERS -0.9%; excess +3.2%
```

Neutral interpretation: the visible VigiAccess propranolol 2025 spike does **not** clearly replicate in this independent US FAERS raw-count sample. Propranolol falls in FAERS in 2025 while the total FAERS baseline is roughly flat.

## Why This Exists

The motivating observation was a sharp 2025 propranolol increase in VigiAccess:

- 2023: 2,183 reports
- 2024: 2,769 reports
- 2025: 6,589 reports

This project asks whether an independent spontaneous-reporting system, US FDA FAERS via OpenFDA, shows a similar 2025 pattern.

## Repository Structure

```text
.
|-- assets/
|   `-- vigiaccess/
|       |-- propranolol.jpeg
|       |-- atenolol.jpeg
|       `-- metoprolol.jpeg
|-- data/
|   |-- faers_betablocker_counts.csv
|   |-- faers_growth_metrics.csv
|   |-- faers_total_counts.csv
|   |-- openfda_query_log.csv
|   |-- run_metadata.json
|   `-- vigiaccess_screenshot_observations.csv
|-- docs/
|   |-- data_dictionary.md
|   |-- limitations.md
|   `-- methodology.md
|-- reports/
|   `-- faers_summary.md
|-- src/
|   `-- faers_check.py
|-- requirements.txt
`-- README.md
```

## Source Evidence

The supplied VigiAccess screenshots are stored as:

- `assets/vigiaccess/propranolol.jpeg`
- `assets/vigiaccess/atenolol.jpeg`
- `assets/vigiaccess/metoprolol.jpeg`

Manual transcriptions from the screenshots are stored in:

- `data/vigiaccess_screenshot_observations.csv`

## Method Summary

OpenFDA endpoint:

```text
https://api.fda.gov/drug/event.json
```

For each drug and year, the script queries:

```text
patient.drug.openfda.generic_name:<drug> AND receivedate:[YYYY0101 TO YYYY1231]
patient.drug.medicinalproduct:<drug> AND receivedate:[YYYY0101 TO YYYY1231]
```

The total FAERS baseline uses the same annual `receivedate` range with no drug filter.

The script reads `meta.results.total` only. It does not paginate individual reports.

For full details, see:

- `docs/methodology.md`
- `docs/data_dictionary.md`
- `docs/limitations.md`

## Install

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python src/faers_check.py
```

No OpenFDA API key is required for this small run. If OpenFDA returns HTTP 429, set `OPENFDA_API_KEY` and rerun.

Windows PowerShell:

```powershell
$env:OPENFDA_API_KEY="your_key_here"
python src/faers_check.py
```

macOS/Linux:

```bash
export OPENFDA_API_KEY="your_key_here"
python src/faers_check.py
```

## Outputs

The script writes:

- `data/faers_betablocker_counts.csv`: tidy drug x year x field counts
- `data/faers_total_counts.csv`: total FAERS baseline by year
- `data/faers_growth_metrics.csv`: YoY growth, multipliers, and excess growth
- `data/openfda_query_log.csv`: exact OpenFDA URLs used
- `data/run_metadata.json`: snapshot metadata
- `reports/faers_summary.md`: bilingual Arabic/English report

## GitHub Actions

The repository includes a manual workflow:

```text
.github/workflows/reproduce.yml
```

Use **Actions -> Reproduce FAERS Check -> Run workflow** to rerun the OpenFDA queries from GitHub. The workflow uploads regenerated CSV, JSON, and Markdown outputs as an artifact. It is manual by design so the public API is not queried on every push.

## Interpretation Guardrails

- Counts are raw spontaneous reports, not incidence rates.
- No exposed-patient denominator is available.
- FAERS and VigiAccess can be affected by reporting awareness, utilization changes, duplicates, follow-up reports, mapping differences, and database ingestion timing.
- Recent years can continue to change because of reporting lag.
- A lack of replication in FAERS does not prove absence of a safety issue; it only means this specific raw-count spike is not reproduced in this second system.

## Arabic Summary

هذا المشروع يفحص ما إذا كانت قفزة بلاغات **propranolol** الظاهرة في VigiAccess سنة 2025 تتكرر في قاعدة FAERS الأمريكية عبر OpenFDA.

النتيجة الحالية: لا تظهر القفزة نفسها بوضوح في FAERS. أعداد propranolol في FAERS تنخفض في 2025 مقارنة بـ 2024، بينما إجمالي FAERS شبه ثابت. هذه أعداد بلاغات خام وليست قياسا للخطر أو السببية.

## License

MIT License.
