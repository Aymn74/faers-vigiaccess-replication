# Methodology

## Question

Does the visible 2025 propranolol spike in VigiAccess also appear in the independent US FDA FAERS database?

This is a replication-style descriptive check. It is not a disproportionality analysis, incidence estimate, or causal safety assessment.

## Data Sources

### VigiAccess

The repository includes three supplied VigiAccess screenshots:

- `assets/vigiaccess/propranolol.jpeg`
- `assets/vigiaccess/atenolol.jpeg`
- `assets/vigiaccess/metoprolol.jpeg`

The visible propranolol annual table in the screenshot was manually transcribed into `data/vigiaccess_screenshot_observations.csv`.

### FAERS via OpenFDA

OpenFDA endpoint:

```text
https://api.fda.gov/drug/event.json
```

The script queries OpenFDA live and reads only `meta.results.total`. It does not paginate report records.

## Query Design

For each drug and year, the script runs one query on each field:

```text
patient.drug.openfda.generic_name:<drug> AND receivedate:[YYYY0101 TO YYYY1231]
patient.drug.medicinalproduct:<drug> AND receivedate:[YYYY0101 TO YYYY1231]
```

The drug token is intentionally unquoted. This follows the intended replication test and allows broader token matching such as salt forms.

The total FAERS baseline uses:

```text
receivedate:[YYYY0101 TO YYYY1231]
```

with no drug filter.

## Why `receivedate`?

`receivedate` is the date FDA received the report. For this specific cross-system comparison, it is the closest practical analog to a VigiAccess report-entry year. It does not necessarily equal adverse-event onset date, drug start date, or submission date from the original reporter.

## Primary and Sanity-Check Fields

Primary field:

```text
patient.drug.openfda.generic_name
```

This normalized OpenFDA field is easier to interpret but is absent when OpenFDA cannot map a report's drug name.

Sanity-check field:

```text
patient.drug.medicinalproduct
```

This is closer to reporter-entered free text. It can capture records missed by normalized fields, but it is noisier.

The gap between these fields is a data-quality signal, not a risk signal.

## Computed Metrics

The script computes:

- annual counts by drug, year, and field
- annual total FAERS baseline counts
- year-over-year growth
- 2025 vs 2024 multipliers
- 2025 vs 2023 multipliers
- excess 2025 growth versus total FAERS growth

Excess growth is:

```text
drug_2025_yoy_growth_pct - total_FAERS_2025_yoy_growth_pct
```

## Interpretation Rules

If propranolol rises sharply in both VigiAccess and FAERS, the spike is cross-system and could be consistent with stimulated reporting or broader utilization/reporting changes.

If VigiAccess rises sharply while FAERS is flat or down, the VigiAccess pattern is more consistent with a VigiAccess/VigiBase source-specific or reporting-process explanation, such as a national-center batch, migration, or reporting artifact.

Neither result proves or disproves clinical risk.

## Reproducibility

Run:

```bash
python src/faers_check.py
```

Outputs:

- `data/faers_betablocker_counts.csv`
- `data/faers_total_counts.csv`
- `data/faers_growth_metrics.csv`
- `data/openfda_query_log.csv`
- `data/run_metadata.json`
- `reports/faers_summary.md`

The exact OpenFDA URLs used in a run are saved in `data/openfda_query_log.csv` and repeated in the Markdown report.
