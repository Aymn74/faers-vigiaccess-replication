# Limitations and Guardrails

This repository intentionally stays narrow. It answers one descriptive replication question:

> Do raw annual propranolol report counts rise sharply in FAERS in 2025, similar to the supplied VigiAccess screenshot?

## What This Analysis Can Say

- Whether a raw-count pattern appears in both systems.
- Whether propranolol changed more than comparator beta-blockers in the same FAERS snapshot.
- Whether drug-specific FAERS changes exceed the total FAERS annual baseline trend.
- Whether normalized OpenFDA fields and free-text medicinal-product fields tell broadly similar stories.

## What This Analysis Cannot Say

- It cannot estimate adverse-event incidence.
- It cannot estimate patient-level risk.
- It cannot establish causality.
- It cannot adjust for drug exposure, prescription volume, or indication.
- It cannot remove duplicates or follow-up reports.
- It cannot determine whether a VigiAccess change came from one national center, one batch, or one reporting workflow without access to underlying VigiBase metadata.

## Why Counts Are Not Risk

Spontaneous-report counts are affected by:

- reporting awareness
- media or regulatory attention
- product utilization
- indication shifts
- duplicate reports
- follow-up reports
- database ingestion timing
- national-center reporting practices
- mapping from reporter-entered product text into normalized drug fields

For this reason, this project uses non-alarmist language and treats all findings as hypothesis-generating.

## Reporting Lag

Recent years can continue to change. The script records:

- the local snapshot date
- OpenFDA `meta.last_updated`

Those dates should be included whenever results are quoted.

## Field Mapping

The normalized OpenFDA field `patient.drug.openfda.generic_name` can miss reports that OpenFDA does not map. The free-text field `patient.drug.medicinalproduct` can behave differently because it is less normalized.

The difference between those two fields is a data-quality signal, not an epidemiologic conclusion.
