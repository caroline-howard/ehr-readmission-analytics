# Validation Outputs

This folder contains intentionally committed aggregate QA tables generated from local Synthea synthetic data. These files are small validation artifacts used to document the cohort-building workflow before descriptive statistics or modeling.

Included outputs:

- `cohort_attrition_counts.csv`
- `index_encounter_check.csv`
- `date_validity_checks.csv`
- `encounter_class_distribution.csv`
- `missingness_report.csv`
- `readmission_timing_validation.csv`
- `outpatient_followup_timing_validation.csv`

These tables do not contain real patient data or patient-level synthetic records. They are reproducible by placing Synthea CSVs in `data/raw/` and running the SQL scripts in `sql/` in order, ending with `sql/07_create_validation_outputs.sql`.
