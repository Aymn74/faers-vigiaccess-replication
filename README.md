# FAERS Replication Test - Propranolol VigiAccess Spike

This repository is a small, reproducible OpenFDA/FAERS cross-check for a visible 2025 spike in VigiAccess adverse-event reports for **propranolol**, compared with **atenolol** and **metoprolol**.

It is a hypothesis-generating raw-count comparison only. It does **not** estimate incidence, risk, or causality.

## What This Project Does

- Pulls annual FAERS report counts for propranolol, atenolol, and metoprolol for 2022-2025.
- Runs each drug on two fields:
  - `patient.drug.openfda.generic_name`
  - `patient.drug.medicinalproduct`
- Pulls total FAERS report counts by year as a baseline trend.
- Computes year-over-year growth and 2025 excess growth versus total FAERS.
- Stores supplied VigiAccess screenshots as source evidence.
- Writes a bilingual Arabic/English Markdown summary.

## Repository Structure

```text
.
├── assets/
│   └── vigiaccess/
│       ├── propranolol.jpeg
│       ├── atenolol.jpeg
│       └── metoprolol.jpeg
├── data/
│   ├── faers_betablocker_counts.csv
│   └── vigiaccess_screenshot_observations.csv
├── reports/
│   └── faers_summary.md
├── src/
│   └── faers_check.py
├── requirements.txt
└── README.md
```

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python src/faers_check.py
```

No OpenFDA API key is required for this small run. If OpenFDA returns HTTP 429, set:

```bash
set OPENFDA_API_KEY=your_key_here
```

On macOS/Linux:

```bash
export OPENFDA_API_KEY=your_key_here
```

## Outputs

- `data/faers_betablocker_counts.csv`
- `data/vigiaccess_screenshot_observations.csv`
- `reports/faers_summary.md`

## Current Snapshot Result

Using OpenFDA `meta.last_updated = 2026-04-28` and snapshot date `2026-06-23`:

```text
Total FAERS: 2025 YoY -0.9%
propranolol: 2025 YoY -12.3% vs total FAERS -0.9%; excess -11.4%
atenolol: 2025 YoY -5.3% vs total FAERS -0.9%; excess -4.4%
metoprolol: 2025 YoY +2.3% vs total FAERS -0.9%; excess +3.2%
```

Neutral interpretation: the VigiAccess propranolol 2025 spike does **not** clearly replicate in this independent US FAERS raw-count sample.

## Important Caveats

- FAERS and VigiAccess are spontaneous-reporting systems.
- Counts are raw report counts, not incidence rates.
- Reports can be stimulated by publicity, utilization changes, reporting practice, duplicate handling, or database migrations.
- Recent years can continue changing because of reporting lag.
- This project should not be used to infer individual clinical risk.

## Arabic Summary

هذا المشروع يفحص ما إذا كانت قفزة بلاغات propranolol الظاهرة في VigiAccess سنة 2025 تتكرر في FAERS الأمريكي عبر OpenFDA.

النتيجة الحالية: لا تظهر القفزة نفسها بوضوح في FAERS. أعداد propranolol في FAERS تنخفض في 2025 مقارنة بـ 2024، بينما إجمالي FAERS شبه ثابت. هذه أعداد بلاغات خام وليست قياسا للخطر أو السببية.
