# EHR Post-Discharge Utilization Analytics — V1 Descriptive Cohort Validation

## Release Status

Version 1.0 has been released as the descriptive cohort validation artifact for this synthetic EHR healthcare analytics portfolio project.

Main PDF report:

`report/ehr_post_discharge_utilization_v1_descriptive_validation_report.pdf`

GitHub Release: Version 1.0 — Descriptive Cohort Validation

## Project Overview

This repository preserves Version 1.0 of a synthetic EHR analytics workflow using Synthea data. V1 validates the data engineering and reporting foundation needed to define an adult inpatient index cohort, derive post-discharge utilization outcomes, and produce transparent descriptive outputs.

V1 focuses on descriptive cohort and outcome validation, not clinical evidence, causal inference, or predictive modeling.

## Validation Question

Can a SQL and Python workflow using synthetic EHR data reliably define an adult inpatient index cohort, derive 30-day post-discharge utilization outcomes, and produce transparent descriptive reporting outputs for healthcare analytics use cases?

## What V1 Demonstrates

- Adult inpatient index cohort construction.
- One-row-per-patient index hospitalization logic.
- 30-day post-discharge outcome definitions.
- Descriptive utilization reporting.
- Prior utilization stratification.
- Dashboard and reporting artifacts.
- Synthetic-data limitations and responsible interpretation.

## Key Descriptive Results

| Measure | Result |
| --- | ---: |
| Final analytic cohort | 255 adult patients |
| 30-day inpatient readmission | 13 patients, 5.1% |
| Outpatient follow-up within 30 days | 55 patients, 21.6% |
| ED revisit within 30 days | 2 patients, 0.8% |
| Any post-discharge encounter within 30 days | 96 patients, 37.6% |

Prior utilization burden showed the clearest descriptive pattern in the synthetic cohort.

Sparse-event modeling notes are preserved in `report/archive/v1_sparse_modeling_check.md` for transparency, but predictive modeling is not a main V1 finding.

## Main Report

- PDF report: `report/ehr_post_discharge_utilization_v1_descriptive_validation_report.pdf`
- Markdown report: `report/v1_descriptive_validation_report.md`
- Archived sparse modeling note: `report/archive/v1_sparse_modeling_check.md`

## Dashboard and Reporting Artifacts

The repository includes dashboard-style visuals and aggregate reporting outputs created from the descriptive validation workflow. These artifacts are portfolio and reporting examples only. They are not clinical decision tools, prediction tools, or operational deployment materials.

Selected reporting artifacts include:

- Workflow architecture visual.
- Post-discharge utilization dashboard example.
- Descriptive stratification and interpretation dashboard example.
- Aggregate validation and reporting tables under `outputs/validation/` and `outputs/bi/`.

## Technical Workflow

The V1 workflow uses SQL and Python to:

1. Profile Synthea synthetic EHR source files.
2. Define eligible adult inpatient encounters.
3. Select one index inpatient encounter per patient.
4. Derive 30-day readmission, outpatient follow-up, ED revisit, and any post-discharge encounter outcomes.
5. Validate temporal logic, missingness, and one-row-per-patient structure.
6. Produce aggregate descriptive tables, figures, dashboards, and a technical report.

## Skills Demonstrated

- SQL cohort construction.
- Python/pandas analytics workflow.
- Synthetic EHR data profiling.
- Temporal outcome engineering.
- Healthcare data validation and QA.
- Descriptive utilization reporting.
- Aggregate dashboard and reporting outputs.
- Responsible interpretation of sparse synthetic data.

## Repository Structure

```text
docs/       Project documentation, data dictionary, reproducibility notes, and limitations
data/       Local raw and processed Synthea data folders excluded from version control
sql/        SQL scripts for cohort construction, outcome derivation, and validation
notebooks/  Notebook-based profiling, descriptive analysis, and archived modeling checks
outputs/    Small aggregate validation tables, BI-ready tables, and static figures
report/     V1 descriptive validation report, PDF, and archived modeling note
app/        Lightweight portfolio demo app
scripts/    Command-line utilities for profiling and reproducible workflow support
```

## Responsible Use

This project uses synthetic data only. It contains no real patient data.

The V1 outputs are not clinical evidence, not a validated prediction model, and not intended for clinical decision-making, quality reporting, or operational deployment.

## Future Work Note

Future predictive risk stratification work will be developed separately from this V1 release using a larger synthetic cohort and stricter discharge-time feature design.
