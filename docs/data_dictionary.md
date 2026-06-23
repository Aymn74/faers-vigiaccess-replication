# Data Dictionary

## `data/faers_betablocker_counts.csv`

Tidy long-format FAERS counts.

| column | meaning |
| --- | --- |
| `drug` | `propranolol`, `atenolol`, or `metoprolol` |
| `year` | calendar year based on FAERS `receivedate` |
| `field` | `openfda_generic_name` or `medicinalproduct` |
| `count` | OpenFDA `meta.results.total` for that query |
| `snapshot_date` | date the script was run |
| `meta_last_updated` | OpenFDA `meta.last_updated` returned by the API |

## `data/faers_total_counts.csv`

Annual total FAERS baseline counts with no drug filter.

| column | meaning |
| --- | --- |
| `year` | calendar year based on FAERS `receivedate` |
| `total_faers_reports` | all FAERS reports returned by the annual `receivedate` query |
| `yoy_growth_pct` | year-over-year percentage growth |
| `snapshot_date` | date the script was run |
| `meta_last_updated` | OpenFDA `meta.last_updated` returned by the API |

## `data/faers_growth_metrics.csv`

Derived growth metrics for each drug and field.

| column | meaning |
| --- | --- |
| `drug` | drug name |
| `field` | OpenFDA drug field |
| `count_2023`, `count_2024`, `count_2025` | annual counts used for growth calculations |
| `yoy_2024_pct` | growth from 2023 to 2024 |
| `yoy_2025_pct` | growth from 2024 to 2025 |
| `multiplier_2025_vs_2024` | 2025 count divided by 2024 count |
| `multiplier_2025_vs_2023` | 2025 count divided by 2023 count |
| `total_faers_2025_yoy_pct` | total FAERS baseline growth from 2024 to 2025 |
| `excess_2025_yoy_vs_total_faers_pct` | drug 2025 YoY minus total FAERS 2025 YoY |

## `data/vigiaccess_screenshot_observations.csv`

Manual transcription of visible values from the supplied VigiAccess screenshots.

| column | meaning |
| --- | --- |
| `drug` | drug shown in the screenshot |
| `source_image` | screenshot path in this repository |
| `observation` | type of visible value transcribed |
| `year` | year if the value came from an annual table |
| `value` | transcribed value |
| `note` | provenance note |

## `data/openfda_query_log.csv`

Every OpenFDA URL used by the script.

| column | meaning |
| --- | --- |
| `drug` | drug filter, or `ALL_FAERS` for denominator queries |
| `field` | OpenFDA field used |
| `year` | query year |
| `url` | exact query URL |

## `data/run_metadata.json`

Machine-readable run metadata: snapshot date, OpenFDA update date, endpoint, years, drugs, fields, and scope statement.
